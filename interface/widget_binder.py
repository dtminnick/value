
import tkinter as tk
from tkinter import ttk
from messenger import Messenger

msg_handler = Messenger()

class WidgetBinder:
    """
    A utility class for managing and synchronizing values across multiple Tkinter widgets,
    including Comboboxes with ID-title mapping, Entry widgets, Text widgets, and Checkbuttons.

    This class helps:
    - Maintain consistent data binding between widgets.
    - Map display values in Comboboxes to internal IDs.
    - Enable easy get/set logic for form data handling.
    """

    def __init__(self, root, is_testing = True):
        """
        Initialize the WidgetBinder with a Tkinter root or parent frame.

        Parameters
        ----------
        root : tk.Tk or tk.Frame
            The parent container for the widgets managed by this class.
        """
        self.root = root
        self.is_testing = is_testing  # Global setting for visibility control

        self.comboboxes = {}     # label -> (combobox, data_dict)
        self.combo_value_maps = {}  # combobox widget -> {title_to_id, id_to_title}
        self.selected_ids = {}   # label -> selected ID
        self.id_entries = {}     # label -> Entry widget to display selected ID

        self.msg_handler = msg_handler

    def add_combobox(self, label, data_dict, row, col, parent=None):
        """
        Create and register a Combobox bound to an ID-title dictionary.
        This method also creates a readonly Entry to display the selected ID.

        Parameters
        ----------
        label : str
            A logical name used to reference the combobox elsewhere.
        data_dict : dict
            A mapping from display names (titles) to their corresponding IDs.
        row : int
            The row index to place the widgets in the grid.
        col : int
            The column index to place the widgets in the grid.
        parent : widget, optional
            The parent widget to attach the combobox and entry to.
            Defaults to self.root if not provided.

        Returns
        -------
        ttk.Combobox
            The created Combobox widget.
        """
        try:
            label = label.lower()

            if parent is None:
                parent = self.root  # Default fallback if no parent provided

            combo_box = ttk.Combobox(parent, values = list(data_dict.keys()), state="readonly")

            combo_box.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            
            combo_box.bind("<<ComboboxSelected>>", lambda event, cb=combo_box, d=data_dict, l=label: self.on_select(cb, d, l))

            id_entry = ttk.Entry(parent, state="readonly", width=10)

            id_entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")  # (Notice: using col+1 for the ID field)

            if not self.is_testing:
                id_entry.grid_forget()  # Hide the ID entry widget in production

            # Store mappings
            self.comboboxes[label] = (combo_box, data_dict)
            self.id_entries[label] = id_entry
            self.combo_value_maps[combo_box] = {
                "title_to_id": data_dict,
                "id_to_title": {v: k for k, v in data_dict.items()}
            }

            return combo_box
        except Exception as e:
            self.msg_handler.show_error("Add Combobox Error", f"Error adding combobox: \n\n {e}")
    
    def get_id_entry_value(self, label):
        """
        Get the current ID value from the readonly Entry widget associated with a Combobox.

        Parameters
        ----------
        label : str
            The logical name used to reference the combobox/ID entry.

        Returns
        -------
        str or None
            The ID value as a string, or None if not available.
        """
        try:
            label = label.lower()
            id_entry = self.id_entries.get(label)

            if id_entry:
                return id_entry.get().strip()

            return None
        except Exception as e:
            self.msg_handler.show_error("Get Id Entry Value Error", f"Error getting id entry value: \n\n {e}")

    def on_select(self, combo_box, data_dict, label):
        """
        Handle the Combobox selection event and update internal state.

        Parameters
        ----------
        combo_box : ttk.Combobox
            The combobox being interacted with.
        data_dict : dict
            Mapping of titles to IDs.
        label : str
            The logical label used to identify the combobox.
        """
        try:
            label = label.lower()
            selected_name = combo_box.get()
            selected_id = data_dict.get(selected_name)

            self.selected_ids[label] = selected_id
            print(f"[{label}] Selected: {selected_name} (ID: {selected_id})")

            # Update associated readonly Entry with selected ID
            id_entry = self.id_entries.get(label)
            if id_entry:
                id_entry.config(state="normal")
                id_entry.delete(0, tk.END)
                id_entry.insert(0, str(selected_id))
                id_entry.config(state="readonly")
        except Exception as e:
            self.msg_handler.show_error("On Select Error", f"Error: \n\n {e}")

    def get_selected_ids(self):
        """
        Get a dictionary of all current selections by label.

        Returns
        -------
        dict
            Mapping from label to selected ID.
        """
        try: 
            return self.selected_ids
        except Exception as e:
            self.msg_handler.show_error("Get Selected Ids Error", f"Error: \n\n {e}")

    def get_selected_id(self, table_name):
        """
        Get the selected ID for a specific Combobox label.

        Parameters
        ----------
        table_name : str
            The label of the combobox (e.g., "Initiative").

        Returns
        -------
        int or None
            The selected ID, or None if not selected.
        """
        try: 
            return self.selected_ids.get(table_name.lower())
        except Exception as e:
            self.msg_handler.show_error("Get Selected Id Error", f"Error: \n\n {e}")

    def get_widget_value(self, widget):
        """
        Retrieve the value from a supported Tkinter widget.
        For Comboboxes, prefer the mapped ID if available.
        """
        try:
            if isinstance(widget, ttk.Combobox):
                selected_title = widget.get()
                id_value = self.combo_value_maps.get(widget, {}).get("title_to_id", {}).get(selected_title)
                return id_value

            elif isinstance(widget, tk.Text):
                return widget.get("1.0", "end-1c").strip()

            elif isinstance(widget, (ttk.Entry, tk.Entry)):
                return widget.get().strip()

            elif isinstance(widget, ttk.Checkbutton):
                var_name = widget.cget("variable")
                if var_name:
                    return bool(self.root.getvar(var_name))
                return None

            elif hasattr(widget, "get") and callable(getattr(widget, "get")):
                return widget.get()

            else:
                return None
        except Exception as e:
            self.msg_handler.show_error("Get Widget Value Error", f"Error: \n\n {e}")

    def set_widget_value(self, widget, value):
        """
        Set a value into a supported Tkinter widget.

        Parameters
        ----------
        widget : tk.Widget
            The widget to update.
        value : Any
            The value to set. For Comboboxes, this is expected to be an ID
            that maps to a title; for other widgets, the appropriate type.
        """
        try: 
            if isinstance(widget, ttk.Combobox):
                mapping = self.combo_value_maps.get(widget)
                if mapping:
                    title = mapping["id_to_title"].get(value)
                    if title:
                        widget.set(title)
                        return
                widget.set(str(value))  # fallback if no mapping

            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
                widget.insert("1.0", str(value))

            elif isinstance(widget, (ttk.Entry, tk.Entry)):
                widget.delete(0, tk.END)
                widget.insert(0, str(value))

            elif isinstance(widget, ttk.Checkbutton):
                var_name = widget.cget("variable")
                if var_name:
                    self.root.setvar(var_name, bool(value))

            elif hasattr(widget, "delete") and hasattr(widget, "insert"):
                widget.delete(0, tk.END)
                widget.insert(0, str(value))
        except Exception as e:
            self.msg_handler.show_error("Set Widget Value Error", f"Error: \n\n {e}")

    def add_entry_for_combobox(self, combobox, row, col, parent=None):
        """
        Create an Entry widget that corresponds to a Combobox for displaying the selected ID.
        The Entry widget is set to readonly mode to prevent direct user modification.
        
        This method also stores the link between the Combobox and the Entry widget.
        
        Parameters
        ----------
        combobox : ttk.Combobox
            The combobox widget for which the Entry widget is being created.
        row : int
            The row index to place the Entry widget in the grid.
        col : int
            The column index to place the Entry widget in the grid.
        parent : widget, optional
            The parent widget to attach the Entry widget to.
            Defaults to self.root if not provided.

        Returns
        -------
        ttk.Entry
            The created Entry widget that will be linked to the combobox.
        """
        try:
            # Fallback to self.root if no parent provided
            if parent is None:
                parent = self.root

            # Create the readonly Entry widget to display the selected ID
            id_entry = ttk.Entry(parent, state="readonly", width=10)
            id_entry.grid(row=row, column=col, padx=5, pady=5, sticky="w")

            # Store the combobox-Entry link in the entries dictionary
            combobox_label = combobox.get()  # You can use any logic to label the combobox
            self.entries[combobox_label] = {
                "combobox": combobox,
                "id_entry": id_entry
            }

            return id_entry

        except Exception as e:
            self.msg_handler.show_error("Add Entry Error", f"Error adding entry for combobox: \n\n {e}")
