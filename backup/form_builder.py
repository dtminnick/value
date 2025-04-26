
import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry

class FormBuilder:
    def __init__(self, parent, table_name, db, message_handler, downloader, db_config):
        self.parent = parent  # Accept parent argument
        self.table_name = table_name
        self.db = db
        self.message_handler = message_handler
        self.downloader = downloader
        self.db_config = db_config
        self.root = tk.Tk()
        self.root.title("Dynamic Form with Tabs")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        self.entries = {}

    def fetch_form_config(self):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM form_configuration ORDER BY field_tab, field_order")
        form_config = cursor.fetchall()

        conn.close()
        return form_config

    def fetch_lookup_data(self, table, id_col, display_col):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        cursor.execute(f"SELECT {id_col}, {display_col} FROM {table}")
        lookup_data = cursor.fetchall()

        conn.close()
        return lookup_data

    def _create_widget(self, field, parent_frame):
        label = ttk.Label(parent_frame, text=field['field_label'])
        label.grid(row=field['field_order'], column=0, sticky='w', padx=5, pady=5)

        field_type = field['field_type'].lower()

        if field_type == 'entry':
            entry = ttk.Entry(parent_frame)
            entry.grid(row=field['field_order'], column=1, sticky='ew', padx=5, pady=5)
            self.entries[field['field_name']] = entry

        elif field_type == 'combobox':
            values = [row[1] for row in self.fetch_lookup_data(
                field['lookup_table'], field['lookup_id_column'], field['lookup_display_column']
            )]
            combobox = ttk.Combobox(parent_frame, values=values)
            combobox.grid(row=field['field_order'], column=1, sticky='ew', padx=5, pady=5)
            self.entries[field['field_name']] = combobox

        elif field_type == 'checkbox':
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(parent_frame, variable=var)
            checkbox.grid(row=field['field_order'], column=1, sticky='w', padx=5, pady=5)
            self.entries[field['field_name']] = var

        elif field_type == 'date':
            date_entry = DateEntry(parent_frame, date_pattern="yyyy-mm-dd")
            date_entry.grid(row=field['field_order'], column=1, sticky='w', padx=5, pady=5)
            self.entries[field['field_name']] = date_entry

    def build_form(self, config_data):
        tabs = {}

        for field in config_data:
            tab_name = field['field_tab']

            if tab_name not in tabs:
                tab_frame = ttk.Frame(self.notebook)
                tab_frame.columnconfigure(1, weight=1)
                self.notebook.add(tab_frame, text=tab_name)
                tabs[tab_name] = tab_frame

            self._create_widget(field, tabs[tab_name])

    def run(self):
        config_data = self.fetch_form_config()
        self.build_form(config_data)
        self.root.mainloop()

if __name__ == '__main__':
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'McM1093x!',
        'database': 'value'
    }
    form_builder = FormBuilder(db_config)
    form_builder.run()
