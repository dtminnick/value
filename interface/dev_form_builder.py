
import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkcalendar import DateEntry

def fetch_form_config():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='value',
            user='root',
            password='McM1093x!'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM form_config ORDER BY tab_order, field_order;")
        return cursor.fetchall()
    except Error as e:
        print("Error while connecting to MySQL:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_lookup_data(lookup_table, lookup_id_col, lookup_display_col):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='value',
            user='root',
            password='McM1093x!'
        )
        cursor = connection.cursor()
        cursor.execute(f"SELECT {lookup_id_col}, {lookup_display_col} FROM {lookup_table};")
        return [str(item[1]) for item in cursor.fetchall()]
    except Error as e:
        print("Error fetching lookup data:", e)
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_dynamic_form(config_data):
    root = tk.Tk()
    root.title("Dynamic Form with Tabs")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab_data = {}

    for row in config_data:
        form_name = row['form_name']
        tab_order = row['tab_order']
        tab_display_name = row['tab_display_name'] or form_name

        if tab_order not in tab_data:
            tab_data[tab_order] = {'tab_name': tab_display_name, 'fields': []}

        tab_data[tab_order]['fields'].append(row)

    for tab_order, tab in tab_data.items():
        tab_name = tab['tab_name']
        frame = tk.Frame(notebook)
        notebook.add(frame, text=tab_name)

        for idx, field in enumerate(sorted(tab['fields'], key=lambda x: x['field_order'])):
            label = tk.Label(frame, text=field['label_text'])
            label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")

            widget = None
            field_width = field['field_width'] or 20

            if field['field_type'] == 'text':
                widget = tk.Entry(frame, width = field_width)

            elif field['field_type'] == 'combobox' and field['lookup_table']:
                options = fetch_lookup_data(
                    field['lookup_table'],
                    field['lookup_id_col'],
                    field['lookup_display_col']
                )
                widget = ttk.Combobox(frame, values=options, width = field_width)
                if options:
                    widget.current(0)

            elif field['field_type'] == 'checkbox':
                var = tk.BooleanVar()
                widget = tk.Checkbutton(frame, variable=var, width = field_width)

            elif field['field_type'] == 'date':
                widget = DateEntry(frame, 
                                   width=field_width, 
                                   background='darkblue', 
                                   foreground='white', 
                                   borderwidth=2)

            if widget:
                widget.grid(row=idx, column=1, padx=5, pady=5, sticky="w")

    root.mainloop()

if __name__ == "__main__":
    data = fetch_form_config()
    create_dynamic_form(data)
