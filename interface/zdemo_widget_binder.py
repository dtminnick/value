
import tkinter as tk
from tkinter import ttk
from widget_binder import WidgetBinder  # Assumes WidgetBinder is in a separate file

def main():
    # ---------------------------
    # App Initialization
    # ---------------------------
    root = tk.Tk()
    root.title("WidgetBinder UI Demo")
    root.geometry("400x400")

    # Initialize the binder
    binder = WidgetBinder(root)

    # ---------------------------
    # Sample Data Dictionaries
    # ---------------------------
    initiative_dict = {
        "Initiative A": 101,
        "Initiative B": 102,
        "Initiative C": 103
    }

    status_dict = {
        "Not Started": 0,
        "In Progress": 1,
        "Complete": 2
    }

    # ---------------------------
    # Create Widgets
    # ---------------------------

    # Entry Widget
    tk.Label(root, text="Name").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Text Widget
    tk.Label(root, text="Description").pack()
    desc_text = tk.Text(root, height=4, width=30)
    desc_text.pack()

    # Checkbutton
    active_var = tk.BooleanVar()
    active_check = ttk.Checkbutton(root, text="Active?", variable=active_var)
    active_check.pack()

    # Combobox for Initiatives
    tk.Label(root, text="Initiative").pack()
    initiative_cb = binder.add_combobox("initiative", initiative_dict)

    # Combobox for Status
    tk.Label(root, text="Status").pack()
    status_cb = binder.add_combobox("status", status_dict)

    # ---------------------------
    # Set Initial Values
    # ---------------------------
    binder.set_widget_value(name_entry, "John Doe")
    binder.set_widget_value(desc_text, "Initial project description.")
    binder.set_widget_value(active_check, True)
    binder.set_widget_value(initiative_cb, 102)  # Sets to "Initiative B"
    binder.set_widget_value(status_cb, 1)        # Sets to "In Progress"

    # ---------------------------
    # Button Callback to Collect Values
    # ---------------------------
    def submit():
        values = {
            "name": binder.get_widget_value(name_entry),
            "description": binder.get_widget_value(desc_text),
            "active": binder.get_widget_value(active_check),
            "initiative_id": binder.get_widget_value(initiative_cb),
            "status_id": binder.get_widget_value(status_cb)
        }
        print("Form Values:", values)

    # Submit Button
    tk.Button(root, text="Submit", command=submit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
