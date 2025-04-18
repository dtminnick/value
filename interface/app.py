
from downloader import Downloader
from messenger import Messenger
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from tooltip import Tooltip
from value_db import Database
from PIL import Image, ImageTk


db = Database()

msg_handler = Messenger()

downloader = Downloader(msg_handler)

def exit_app():

    if messagebox.askokcancel("Exit", "Do you really want to quit?"):
        root.destroy()

def show_about():

    about_text = (
        "Application Name: Value Measurement Database Application\n\n"
        "Description: A tool to measure and track initiative value across operations.\n\n"
        "Version: 1.0.0\n\n"
        "Developed by: Donnie Minnick, Transformation Office\n\n"
        "For more information: donnie.minnick@gmail.com"
    )

    messagebox.showinfo("About", about_text)

class App:

    """
    A GUI application for interacting with the Value Measurement MySQL database.

    Features
    --------

    
    """

    def __init__(self, root):
        
        """
        Initializing application, creates tab for each table and 
        dynamicallty generates UI components.
        
        """

        self.root = root

        self.root.title("Value Measurement Database Application")

        self.root.geometry("1200x700")

        # Create notebook for tabbed UI.

        self.notebook = ttk.Notebook(root)

        self.notebook.pack(expand = True, fill = "both")

        style = ttk.Style()

        style.theme_use('default')

        style.configure('TNotebook.tab', width = 18, padding = [5, 5])

        self.tables = ['initiative', 
                       'event',
                       'metric',
                       'plan',
                       'event_plan',
                       'global_metric_value',
                       'plan_metric_value',
                       'user_query']
        
        # Store frames for each table, fields per table and treeview widgets per table.

        self.frames = {}

        self.entries = {}

        self.trees = {}

        # Create a tab and UI for each table.

        for table in self.tables:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text = table)
            self.frames[table] = frame
            self.create_table_ui(frame, table)

        # Create queries tab for predefined and custom queries.

        query_frame = ttk.Frame(self.notebook)

        # Create query selection frame.

        query_selection_frame = ttk.Frame(query_frame)

        query_selection_frame.pack(fill = "x", padx = 10, pady = 5)

        predefined_queries = db.execute_query("SELECT query_title, query_string FROM user_query ORDER BY query_title;")

        self.title_to_query_map = {q['query_title']: q['query_string'] for q in predefined_queries}

        self.selected_query_title = tk.StringVar()

        titles = list(self.title_to_query_map.keys())

        query_dropdown_label = ttk.Label(query_selection_frame, text = "Select query:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        query_dropdown = ttk.Combobox(query_selection_frame,
                                      width = 100,
                                      textvariable = self.selected_query_title,
                                      values = titles).grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")
        
        # Create query selection button frame.

        query_button_frame = ttk.Frame(query_frame)

        # run_image = Image.open("G:/My Drive/Personal/IIT/Relation Database Implementation and Applications/Project/Icons/icon_run_20.png")

        # run_image.resize((10, 10), Image.Resampling.LANCZOS)

        # run_icon = ImageTk.PhotoImage(run_image)

        # root.run_image = run_icon

        execute_query_btn = ttk.Button(query_button_frame,
                                       command = self.run_selected_query,
                                       # image = run_icon,
                                       text = "Run Query")
        
        execute_query_btn.grid(row = 0, column = 0, padx = 5)

        download_btn = ttk.Button(query_button_frame, 
                                  command = self.download_query_result,
                                  text = "Download Result")
        
        download_btn.grid(row = 0, column = 1, padx = 5)

        query_button_frame.pack(fill = "x", padx = 10, pady = 5)

        # Create query output frame.

        self.last_query_result = []

        query_output_frame = ttk.Frame(query_frame)

        query_output_frame.pack(fill = "both", expand = True, padx = 10, pady = 5)

        self.query_output_table = ttk.Treeview(query_output_frame)

        self.query_output_table.pack(fill = "both", expand = True)

        query_frame.pack()

        self.notebook.add(query_frame, text = "queries")

        self.frames["queries"] = query_frame

        # Create a menu bar.

        menu_bar = tk.Menu(root)

        # Create a File menu and add items.

        file_menu = tk.Menu(menu_bar, tearoff = 0)

        file_menu.add_command(label = "New")

        file_menu.add_separator()

        file_menu.add_command(label = "Exit", command = exit_app)

        menu_bar.add_cascade(label = "File", menu = file_menu)

        # Create Goto menu.
        
        goto_menu = tk.Menu(menu_bar, tearoff=0)

        # Combine self.tables and 'queries' tab

        all_tabs = self.tables + ["queries"]

        for table in all_tabs:
            goto_menu.add_command(
                label = table,
                command = lambda t = table: self.goto_tab(t)
            )

        menu_bar.add_cascade(label = "Goto", menu = goto_menu)

        # Create a Help menu.

        help_menu = tk.Menu(menu_bar, tearoff = 0)

        help_menu.add_command(label = "About", command = show_about)

        menu_bar.add_cascade(label = "Help", menu = help_menu)

        # Attach the menu bar to the root window.

        root.config(menu = menu_bar)

        # Add tooltips.

        Tooltip(execute_query_btn, widget_id = "execute_query_btn")

        Tooltip(download_btn, widget_id = "download_btn")

    def create_table_ui(self, parent, table_name):

        """
        
        
        """

        frame = parent

        columns = db.get_columns(table_name)

        if not columns:
            return
        
        self.entries[table_name] = {}

        # Input fields.

        form_frame = ttk.Frame(frame)

        form_frame.pack(fill = "x", padx = 10, pady = 5)

        for i, col in enumerate(columns):
            ttk.Label(form_frame, text = f"{col}:").grid(row = i, column = 0, padx = 5, pady = 2, sticky = "w")

            if table_name == "user_query" and i == len(columns) - 1:

                # Use a text widget for the last field, i.e. query_string.

                entry = tk.Text(form_frame, height = 10, width = 100, wrap = "word", font = ("TkDefaultFont", 10))

                entry.grid(row = i, column = 1, padx = 5, pady = 2, sticky = "w")

                # Add vertical scrollbar to Text widget.

                scrollbar = ttk.Scrollbar(form_frame, orient = "vertical", command = entry.yview)

                scrollbar.grid(row = i, column = 2, sticky = "ns", padx = 5, pady = 2)

                # Link the Text widget with the scrollbar.

                entry.configure(yscrollcommand = scrollbar.set)

            else:

                entry = ttk.Entry(form_frame, width = 100)

                entry.grid(row = i, column = 1, padx = 5, pady = 2, sticky = "ew")

            self.entries[table_name][col] = entry

        # Add CRUD buttons.

        button_frame = ttk.Frame(frame)

        button_frame.pack(fill = "x", padx = 10, pady = 5)

        ttk.Button(button_frame, 
                   text = "Add", 
                   command = lambda t = table_name: self.add_record(t)).grid(row = 0, column = 0, padx = 5)
        
        ttk.Button(button_frame, 
                   text = "Update", 
                command = lambda t = table_name: self.update_record(t)).grid(row = 0, column = 1, padx = 5)
        
        ttk.Button(button_frame, 
                   text = "Delete", 
                   command = lambda t = table_name: self.delete_record(t)).grid(row = 0, column = 2, padx = 5)
        
        ttk.Button(button_frame, 
                   text = "Refresh", 
                   command = lambda t = table_name: self.refresh_records(t)).grid(row = 0, column = 3, padx = 5)
        
        # Add data display to see the data in tables.

        tree_frame = ttk.Frame(frame)

        tree_frame.pack(fill = "both", expand = True, padx = 10, pady = 5)

        scrollbar = ttk.Scrollbar(tree_frame, orient = "vertical")

        self.trees[table_name] = ttk.Treeview(tree_frame, columns = columns, show = "headings", yscrollcommand = scrollbar.set)

        scrollbar.config(command = self.trees[table_name].yview)

        scrollbar.pack(side = "right", fill = "y")

        for col in columns:
            self.trees[table_name].heading(col, text = col)
            self.trees[table_name].column(col, width = 120, anchor = "w")

        self.trees[table_name].pack(fill = "both", expand = True)

        self.trees[table_name].bind("<<TreeviewSelect>>", lambda event, t = table_name: self.select_record(t))

        self.refresh_records(table_name) 

    def add_record(self, table):

        """
        Inserts a new record into the table. Allows empty fields (NULL values).

        """

        if table not in self.entries:
            messagebox.showerror("Error", f"value_app: add_record: error: Entries for {table} not found")
            return
        
        try:
            data = {col: self.get_widget_value(self.entries[table][col]) or None for col in self.entries[table]}
            db.insert(table, data)
            self.clear_fields(table)
            self.refresh_records(table)
        except Exception as e:
            msg_handler.show_error("Error", {e})

    def update_record(self, table):

        """ 
        Updates the selected record in the table. Only updates fields that are changed.

        """

        selected_item = self.trees[table].selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Select a record to update.")
            return  # Add return here to stop the function if no item is selected

        selected_values = self.trees[table].item(selected_item)["values"]

        columns = db.get_columns(table)

        primary_keys = [columns[0]] if table != "event_plan" else ["event_id", "plan_id"]

        conditions = {key: selected_values[i] for i, key in enumerate(primary_keys) if selected_values[i] is not None}

        updated_data = {}

        for col in self.entries[table]:
            if col in primary_keys:
                continue

            widget = self.entries[table][col]
            value = self.get_widget_value(widget)

            if value:
                updated_data[col] = value

        if not updated_data:
            msg_handler.show_warning("Warning", "No fields to update.")
            return

        db.update(table, updated_data, conditions)

        self.clear_fields(table)

        self.refresh_records(table)

    def delete_record(self, table):

        """
        Deletes the selected record from the table.
        
        """

        selected_item = self.trees[table].selection()

        if not selected_item:
            msg_handler.show_warning("Warning", "Select a record to delete.")
            return
        
        selected_values = self.trees[table].item(selected_item)["values"]

        columns = db.get_columns(table)

        primary_key = columns[0]

        conditions = {primary_key: selected_values[0]}

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")

        if confirm:
            db.delete(table, conditions)
            self.clear_fields(table)
            self.refresh_records(table)

    def refresh_records(self, table):

        """
        Fetches and displays all records in the given table.  Converts NULL values to 
        empty strings for display.
        
        """

        for row in self.trees[table].get_children():
            self.trees[table].delete(row)

        for record in db.fetch_all(table):
            cleaned_record = tuple("" if v is None else v for v in record.values())
            self.trees[table].insert("", "end", values = cleaned_record)

    def select_record(self, table):

        """
        Populates input fields with the selected record for editing.
        
        """

        selected_item = self.trees[table].selection()

        if not selected_item:
            return
        
        values = self.trees[table].item(selected_item)["values"]

        columns = list(self.entries[table].keys())

        for i, col in enumerate(columns):
            widget = self.entries[table][col]
            value = values[i] if values[i] is not None else ""
            self.set_widget_value(widget, value)

    def clear_fields(self, table):

        """
        Clears input fields after an operation.

        """

        for col in self.entries[table]:
            self.set_widget_value(self.entries[table][col], "")

    def run_selected_query(self):

        """
        Executes the selected query and populates the result in the table.

        This method retrieves the title of the selected query from the UI and looks up
        the corresponding SQL query from a map. It then executes the query using the 
        `db.execute_query()` function and populates the result into the Treeview widget 
        via `populate_table()`. If the query title is empty or not found, the user is 
        notified with a warning.

        Parameters
        ----------
        None

        Raises
        ------
        - User Error: If no query is selected, a warning is shown.
        - Database Error: If an error occurs during query execution or table population,
        an error message is displayed.

        Side Effects
        ------------
        - Executes a database query.
        - Populates the Treeview with the query result.
        - Updates `last_query_result` with the latest query result.

        """

        title = self.selected_query_title.get()

        if not title:
            msg_handler.show_warning("User Error", "Must select a query to run.")
            return

        query = self.title_to_query_map.get(title)

        if query:
            try:
                result = db.execute_query(query)
                # print(f"Query returned {len(result)} rows")
                self.populate_table(result)
                self.last_query_result = result
            except Exception as e:
                msg_handler.show_error("Database Error", {e})

    def populate_table(self, data):

        """
        Populates the Treeview widget with tabular data.

        This method clears any existing data in the Treeview and repopulates it with
        new rows based on the provided list of dictionaries. Each dictionary is assumed
        to represent a row, with keys corresponding to column names.

        If `data` is empty or `None`, the method shows a user warning and exits early.

        Parameters
        ----------
        data : List[Dict[str, Any]]
            A list of dictionaries containing the data to display. Each dictionary
            must have the same keys (column names).

        Raises
        ------
        Displays an error dialog if any exception is encountered while populating the table.

        Side Effects
        ------------
        - Clears and rebuilds the columns and rows in the Treeview widget.
        - Displays a warning if no data is provided.
        - Displays an error if data cannot be rendered (e.g., inconsistent structure).

        """

        if not data:
            msg_handler.show_warning("User Error", "No query results to download.")
            return
        
        try:
            self.query_output_table.delete(*self.query_output_table.get_children())
        
            columns = list(data[0].keys())

            self.query_output_table["columns"] = columns

            self.query_output_table["show"] = "headings"

            for col in columns:
                self.query_output_table.heading(col, text = col)
                self.query_output_table.column(col, anchor = "w")

            for row in data:
                values = [row[col] for col in columns]
                self.query_output_table.insert("", "end", values = values)

        except Exception as e:
                msg_handler.show_error("Database Error", {e})
        
    def get_widget_value(self, widget):

        """
        Retrieves the cleaned text from a Tkinter input widget (either `Entry` or `Text`),
        handling each widget type appropriately to return the user input.

        - For `tk.Entry` widgets (single-line input), returns the text content.
        - For `tk.Text` widgets (multi-line input), retrieves the text from the start to the end, excluding the trailing newline.

        Parameters
        ----------
        widget : tk.Widget)
            The Tkinter input widget (either `tk.Entry` or `tk.Text`) from which the value is retrieved.

        Returns
        -------
        str
            The cleaned text content from the widget, with leading/trailing whitespace removed.

        """

        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c").strip()
        else:
            return widget.get().strip()
        
    def set_widget_value(self, widget, value):

        """
        Sets the given value into a Tkinter input widget (either `Entry` or `Text`).

        - For `tk.Entry` widgets (single-line input), sets the provided value as the widget's text.
        - For `tk.Text` widgets (multi-line input), clears the existing text and inserts the new value.

        Parameters
        ----------
        widget : tk.Widget
            The Tkinter input widget (either `tk.Entry` or `tk.Text`) to which the value will be set.

        value : str
            The value to be inserted into the widget.

        Returns
        -------
        None

        """

        if isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)
            widget.insert("1.0", value)

        else:
            widget.delete(0, tk.END)
            widget.insert(0, value)

    def get_treeview_data(self):

        """
        Extracts and returns the current data from the Treeview widget.

        This method reads the visible contents of the Treeview (used to display query results),
        capturing both the column headers and the row data. It returns the data as a list of
        dictionaries, where each dictionary represents a row and maps column names to values.

        Steps
        -----
            1. Retrieves column headers from the Treeview widget.
            2. Iterates over each row in the Treeview.
            3. For each row, creates a dictionary pairing column names with cell values.
            4. Collects all row dictionaries into a list.

        Returns
        -------
        List[Dict[str, Any]]
            A list of dictionaries, one per row in the Treeview.

        """

        columns = self.query_output_table["columns"]

        data = []

        for row_id in self.query_output_table.get_children():
            row = self.query_output_table.item(row_id)["values"]
            row_dict = dict(zip(columns, row))
            data.append(row_dict)

        return data

    def download_query_result(self):

        """
        Downloads the current query result displayed in the treeview.

        This method retrieves the data currently shown in the application's treeview,
        gets the title of the selected query, and passes both to a download utility 
        function that handles saving or exporting the data (e.g., to a file).

        Steps
        -----
            1. Extracts data from the treeview widget via `get_treeview_data()`.
            2. Retrieves the title of the selected query from the UI.
            3. Calls the `downloader.download()` function with the data and title.

        Assumes
        -------
            - `get_treeview_data()` returns a list or table-like structure.
            - `selected_query_title` is a `tk.StringVar` or similar, holding a string.
            - `downloader.download()` is defined in a class file and handles the export.

        Returns
        -------
        None
        """

        data = self.get_treeview_data()

        title = self.selected_query_title.get()

        downloader.download(data, title)

    def goto_tab(self, table_name):

        """
        Switches the notebook view to the tab associated with the given table.

        Parameters
        ----------
        table_name : str
            The name of the table/tab to navigate to.
        """
        frame = self.frames.get(table_name)

        if frame:
            tab_index = self.notebook.index(frame)
            self.notebook.select(tab_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

