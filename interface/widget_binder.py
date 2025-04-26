
import tkinter as tk
from tkinter import ttk

class WidgetBinder:
    """
    A utility class for managing and synchronizing values across multiple Tkinter widgets,
    including Comboboxes with ID-title mapping, Entry widgets, Text widgets, and Checkbuttons.

    This class helps:
    - Maintain consistent data binding between widgets.
    - Map display values in Comboboxes to internal IDs.
    - Enable easy get/set logic for form data handling.
    """

    def __init__(self, root):
        """
        Initialize the WidgetBinder with a Tkinter root or parent frame.

        Parameters
        ----------
        root : tk.Tk or tk.Frame
            The parent container for the widgets managed by this class.
        """
        self.root = root
        self.comboboxes = {}     # label -> (combobox, data_dict)
        self.combo_value_maps = {}  # combobox widget -> {title_to_id, id_to_title}
        self.selected_ids = {}   # label -> selected ID
        self.id_entries = {}     # label -> Entry widget to display selected ID

    def add_combobox(self, label, data_dict):
        """
        Create and register a Combobox bound to an ID-title dictionary.

        This method also creates a readonly Entry to display the selected ID.

        Parameters
        ----------
        label : str
            A logical name used to reference the combobox elsewhere.
        data_dict : dict
            A mapping from display names (titles) to their corresponding IDs.

        Returns
        -------
        ttk.Combobox
            The created Combobox widget.
        """
        label = label.lower()

        combo_box = ttk.Combobox(self.root, values=list(data_dict.keys()), state="readonly")
        combo_box.pack(pady=5)
        combo_box.bind("<<ComboboxSelected>>", lambda event, cb=combo_box, d=data_dict, l=label: self.on_select(cb, d, l))

        # Readonly entry to show the selected ID
        id_entry = ttk.Entry(self.root, state="readonly", width=10)
        id_entry.pack(pady=5)

        # Store mappings and widgets
        self.comboboxes[label] = (combo_box, data_dict)
        self.id_entries[label] = id_entry
        self.combo_value_maps[combo_box] = {
            "title_to_id": data_dict,
            "id_to_title": {v: k for k, v in data_dict.items()}
        }

        return combo_box

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

    def get_selected_ids(self):
        """
        Get a dictionary of all current selections by label.

        Returns
        -------
        dict
            Mapping from label to selected ID.
        """
        return self.selected_ids

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
        return self.selected_ids.get(table_name.lower())

    def get_widget_value(self, widget):
        """
        Retrieve the value from a supported Tkinter widget.

        Parameters
        ----------
        widget : tk.Widget
            The widget to extract the value from.

        Returns
        -------
        Any
            The value of the widget:
            - Combobox: mapped ID or selected title.
            - Entry/Text: text content.
            - Checkbutton: Boolean state.
        """
        if isinstance(widget, ttk.Combobox):
            selected_title = widget.get().strip()
            mapping = self.combo_value_maps.get(widget)
            if mapping:
                return mapping["title_to_id"].get(selected_title)
            return selected_title

        elif isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c").strip()

        elif isinstance(widget, (ttk.Entry, tk.Entry)):
            return widget.get().strip()

        elif isinstance(widget, ttk.Checkbutton):
            var_name = widget.cget("variable")
            if var_name:
                return bool(self.root.getvar(var_name))

        elif hasattr(widget, "get"):
            return widget.get()

        return None

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
