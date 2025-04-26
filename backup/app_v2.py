
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *

from downloader import Downloader
from messenger import Messenger
from tooltip import Tooltip
from database import Database
from form_builder import FormBuilder  # New import

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Value Measurement Database Application")

        self.db = Database()
        self.msg_handler = Messenger()
        self.downloader = Downloader(self.msg_handler)

        self.style = Style()
        self.style.configure('TNotebook.tab', width=18, padding=[10, 10])

        self.tables = [
            'initiative', 'event', 'metric', 'plan',
            'event_plan', 'global_metric_value',
            'plan_metric_value', 'user_query'
        ]

        self.frames = {}
        self.entries = {}
        self.trees = {}

        self._build_ui()

    def _build_ui(self):
        self._create_menu()
        self._create_notebook()
        self._create_table_tabs()
        self._create_query_tab()

    def _create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menu_bar.add_cascade(label="File", menu=file_menu)

        goto_menu = tk.Menu(menu_bar, tearoff=0)
        for table in self.tables + ["queries"]:
            goto_menu.add_command(
                label=table,
                command=lambda t=table: self.goto_tab(t)
            )
        menu_bar.add_cascade(label="Goto", menu=goto_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

    def _create_table_tabs(self):
        for table in self.tables:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=table)
            self.frames[table] = frame
            self._create_table_ui(frame, table)

    def _create_table_ui(self, frame, table):
        builder = FormBuilder(
            parent=frame,
            table_name=table,
            db=self.db,
            message_handler=self.msg_handler,
            downloader=self.downloader
        )
        builder.build()
        self.entries[table] = builder.entries
        self.trees[table] = builder.tree

    def _create_query_tab(self):
        query_frame = ttk.Frame(self.notebook)
        self.frames["queries"] = query_frame
        self.notebook.add(query_frame, text="queries")

        selection_frame = ttk.Frame(query_frame)
        selection_frame.pack(fill="x", padx=10, pady=10)

        predefined_queries = self.db.execute_query(
            "SELECT query_title, query_string FROM user_query ORDER BY query_title;"
        )

        self.title_to_query_map = {
            q['query_title']: q['query_string'] for q in predefined_queries
        }

        self.selected_query_title = tk.StringVar()
        titles = list(self.title_to_query_map.keys())

        ttk.Label(selection_frame, text="Select query:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ttk.Combobox(
            selection_frame,
            width=100,
            textvariable=self.selected_query_title,
            values=titles
        ).grid(row=0, column=1, padx=5, pady=2, sticky="w")

        button_frame = ttk.Frame(query_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Run Query", command=self.run_selected_query).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Download Result", command=self.download_query_result).grid(row=0, column=1, padx=5)

        output_frame = ttk.Frame(query_frame)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.query_output_table = ttk.Treeview(output_frame)
        self.query_output_table.pack(fill="both", expand=True)

    def run_selected_query(self):
        title = self.selected_query_title.get()
        query = self.title_to_query_map.get(title)
        if not query:
            self.msg_handler.show_error("No query selected or found.")
            return
        try:
            self.last_query_result = self.db.execute_query(query)
            self._populate_tree(self.query_output_table, self.last_query_result)
        except Exception as e:
            self.msg_handler.show_error(f"Failed to execute query: {e}")

    def _populate_tree(self, tree, data):
        tree.delete(*tree.get_children())
        if not data:
            return
        columns = list(data[0].keys())
        tree.config(columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for row in data:
            values = [row[col] for col in columns]
            tree.insert("", "end", values=values)

    def download_query_result(self):
        if not self.last_query_result:
            self.msg_handler.show_error("No query results to download.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        self.downloader.download_to_csv(self.last_query_result, file_path)

    def goto_tab(self, tab_name):
        index = self.tables.index(tab_name) if tab_name in self.tables else len(self.tables)
        self.notebook.select(index)

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Do you really want to quit?"):
            self.root.destroy()

    def show_about(self):
        about_text = (
            "Application Name: Value Measurement Database Application\n\n"
            "Description: A tool to measure and track initiative value across operations.\n\n"
            "Version: 1.0.0\n\n"
            "Developed by: Donnie Minnick, Transformation Office\n\n"
            "For more information: donnie.minnick@gmail.com"
        )
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
