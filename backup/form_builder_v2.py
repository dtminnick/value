
import tkinter as tk
from tkinter import ttk
from database import Database
from tkcalendar import DateEntry

class FormBuilder:

    def __init__(self):
        self.db = Database()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill = "both", expand = True)
        self.entries = {}

    def fetch_form_data(self):

        sql = f"SELECT * FROM form_config;"

        result = self.db.execute_query(sql)

    def fetch_lookup_data(self, table, id_col, display_col):

        sql = f"SELECT {id_col}, {display_col} FROM {table}"

        result = self.db.execute_query(sql)

        return result

    def create_widget(self, field, parent_frame):

        label = ttk.Label(parent_frame, text = field['label_text'])
        
        label.grid(row = field['field_order'], column = 0, sticky = "w", padx = 5, pady = 5)

        field_type = field['field_type'].lower()

        if field_type == 'text':
            entry = ttk.Entry(parent_frame)
            entry.grid(row = field['field_order'], column = 1, sticky = "w", padx = 5, pady = 5)
            self.entries[field['field_name']] = entry

        elif field_type == 'combobox':
            values = [row[1] for row in self.fetch_lookup_data(
                field['lookup_table'], field['lookup_id_col'], field['lookup_display_col']
            )]
            combobox = ttk.Combobox(parent_frame, values = values)
            combobox.grid(row = field['field_order'], column = 1, sticky = "w", padx = 5, pady = 5)
            self.entries[field['field_name']] = combobox

        elif field_type == 'checkbox':
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(parent_frame, variable = var)
            checkbox.grid(row = field['field_order'], column = 1, sticky = "w", padx = 5, pady = 5)
            self.entries[field['field_name']] = var

        elif field_type == 'date':
            date_entry = DateEntry(parent_frame, date_pattern = "yyyy-mm-dd")
            date_entry.grid(row = field['field_order'], column = 1, sticky = "w", padx = 5, pady = 5)
            self.entries[field['field_name']] = date_entry
        
    def build_form(self, config_data):

        tabs = {}

        for field in config_data:
            tab_name = field['tab_display_name']

            if tab_name not in tabs:
                tab_frame = ttk.Frame(self.notebook)
                tab_frame.columnconfigure(1, weight = 1)
                self.notebook.add(tab_frame, text = tab_name)
                tabs[tab_name] = tab_name

            self.create_widget(field, tabs[tab_name])
