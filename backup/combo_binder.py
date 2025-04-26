
import tkinter as tk
from tkinter import ttk

class ComboBinder:

    def __init__(self):

        # Create dictionary to store mappings between widgets and their 
        # associated metadata (entry, title-to-id map, id-to-title map).

        self.bindings = {}

    def bind(self, combo, entry, rows, id_key = "id", title_key = "name"):

        """
        Binds a combobox to a hidden entry, syncing an id with a visible label.

        Parameters
        ----------
        combo : ttk.Combobox
            The combobox that displays titles.

        entry : tk.Entry
            The hidden entry that stores the id.

        rows : list[dict]
            The records to populate the combobox.

        id_key : str
            The key in the row dict to use as the id.

        title_key : str
            The key in the row dict to use as the display title.
        
        """

        title_to_id = {row[title_key]: row[id_key] for row in rows}

        id_to_title = {row[id_key]: row[title_key] for row in rows}

        combo['values'] = list(title_to_id.keys())

        self.bindings[combo] = {
            "entry": entry,
            "title_to_id": title_to_id,
            "id_to_title": id_to_title
        }

        def on_select(event):

            selected_title = combo.get()

            selected_id = title_to_id.get(selected_title, "")

            entry.delete(0, tk.END)

            entry.insert(0, selected_id)
    
        combo.bind("<<ComboboxSelected>>", on_select)
    
    def set_selection(self, combo, id_value):

        """
        Sets the selection of a combobox and its hidden entry based on an id.

        Parameters
        ----------
        combo : ttk.Combobox
            The combobox to update.

        id_value : str or int
            The id to lookup and set.
        
        """

        binding = self.bindings.get(combo)

        if not binding:
            return
        
        id_to_title = binding["id_to_title"]

        entry = binding["entry"]

        title = id_to_title.get(id_value, "")

        combo.set(title)

        entry.delete(0, tk.END)

        entry.insert(0, id_value)

    def refresh_values(self, combo, new_rows, id_key = "id", title_key = "name"):

        """
        Refreshes the values in a combobox and updates its internal mappings.

        Parameters
        ----------
        combo : ttk.Combobox
            The combobox to refresh.

        new_rows : list[dict]
            A new list of rows with updated data.

        id_key : str
            The key to extract the ID from each row.
            
        title_key : str
            The key to extract the display text from each row.
        """

        id_to_title = {row[id_key]: row[title_key] for row in new_rows}

        title_to_id = {row[title_key]: row[id_key] for row in new_rows}

        # Update stored maps

        if combo in self.bindings:

            self.bindings[combo]["id_to_title"] = id_to_title

            self.bindings[combo]["title_to_id"] = title_to_id

        # Update visible values

        combo["values"] = list(title_to_id.keys())
