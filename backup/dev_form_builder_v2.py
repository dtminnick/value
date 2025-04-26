
# dev_form_builder.py
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector

class FormConfigFetcher:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'your_username',
            'password': 'your_password',
            'database': 'your_database'
        }

    def fetch_config(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM form_config ORDER BY tab_order, field_order")
            config_data = cursor.fetchall()
            cursor.close()
            conn.close()
            return config_data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def fetch_lookup_data(self, table, id_col, display_col):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute(f"SELECT {id_col}, {display_col} FROM {table}")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return [row[1] for row in data]
        except mysql.connector.Error as err:
            print(f"Error fetching lookup data: {err}")
            return []

class DynamicFormApp:
    def __init__(self, config_data):
        self.config_data = config_data
        self.root = tk.Tk()
        self.root.title("Dynamic Form")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)
        self.tab_frames = {}
        self.widgets = {}
        self.fetcher = FormConfigFetcher()

    def build_form(self):
        for field in self.config_data:
            tab_name = field['tab_name']
            if tab_name not in self.tab_frames:
                frame = ttk.Frame(self.notebook)
                self.notebook.add(frame, text=tab_name)
                self.tab_frames[tab_name] = frame

            frame = self.tab_frames[tab_name]
            label = ttk.Label(frame, text=field['label_text'])
            label.grid(row=field['field_order'], column=0, sticky='w', padx=5, pady=5)

            widget = self.create_widget(frame, field)
            widget.grid(row=field['field_order'], column=1, padx=5, pady=5)
            self.widgets[field['field_name']] = widget

        submit_button = ttk.Button(self.root, text="Submit", command=self.submit_form)
        submit_button.pack(pady=10)

    def create_widget(self, parent, field):
        if field['input_type'] == 'text':
            return ttk.Entry(parent)
        elif field['input_type'] == 'combobox':
            values = self.fetcher.fetch_lookup_data(
                field['lookup_table'], field['lookup_id_col'], field['lookup_display_col']
            )
            combo = ttk.Combobox(parent, values=values)
            return combo
        elif field['input_type'] == 'checkbox':
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(parent, variable=var)
            self.widgets[field['field_name'] + '_var'] = var
            return cb
        elif field['input_type'] == 'date':
            return DateEntry(parent)
        else:
            return ttk.Entry(parent)

    def submit_form(self):
        values = {}
        for name, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Combobox):
                values[name] = widget.get()
            elif isinstance(widget, DateEntry):
                values[name] = widget.get_date().isoformat()
            elif isinstance(widget, ttk.Checkbutton):
                var = self.widgets.get(name + '_var')
                values[name] = var.get() if var else False
        print("Form values submitted:", values)

    def run(self):
        self.root.mainloop()


# app.py
from dev_form_builder import FormConfigFetcher, DynamicFormApp

def create_dynamic_ui():
    fetcher = FormConfigFetcher()
    config = fetcher.fetch_config()
    app = DynamicFormApp(config)
    app.build_form()
    app.run()

if __name__ == "__main__":
    create_dynamic_ui()
