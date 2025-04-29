
from downloader import Downloader
from messenger import Messenger
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from tooltip import Tooltip
from database import Database
from tkcalendar import DateEntry
from widget_binder import WidgetBinder
import tkinter.font as tkfont

db = Database()

msg_handler = Messenger()

downloader = Downloader(msg_handler)

class App:

    """
    A GUI application for interacting with the Value Measurement MySQL database.

    """

    def __init__(self, root):
        
        """
        Initializes application, creates tab for each table and generates UI components.

        This constructor sets up the tabs and UI elements for managing initiatives. For each tab, 
        the constructor performs the following steps:

        1. Creates a frame for the tab and adds it to the notebook.
        2. Constructs entry widgets for user input (e.g., initiative ID, title, description, dates).
        3. Adds labels, entry fields, and date pickers, arranging them in a grid layout.
        4. Configures buttons for performing CRUD operations (Add, Update, Delete, Refresh).
        5. Sets up a treeview to display records from the associated table.
        6. Initializes relevant event handlers for selecting, updating, and deleting records.

        The `self.entries` dictionary is populated with references to the input fields for easy access 
        during data collection and updates.
        
        Additionally, the `self.trees` dictionary is used to store the treeview widget for the "Initiatives" 
        tab for record management and display.

        Notes:
            - The structure is designed to allow easy addition of more tabs in the future, following the same pattern.

        """

        self.root = root

        self.binder = WidgetBinder(root, is_testing = True)

        self.root.title("Value Measurement Database Application")

        self.root.geometry("1200x800")

        # ------------------------------------------
        # Create notebook for tabbed user interface.
        # ------------------------------------------

        self.notebook = ttk.Notebook(root)

        self.notebook.pack(expand = True, fill = "both")

        style = ttk.Style()

        style.configure('TNotebook.tab', width = 18, padding = [10, 10])
        
        # Store frames for each table, fields per table and treeview widgets per table.

        self.frames = {}

        self.entries = {}

        self.trees = {}

        # Create combo dictionaries for initiatives, events, plans and metrics.

        self.init_list = db.execute_query("SELECT initiative_title, initiative_id FROM initiative;")

        self.init_dict = {row['initiative_title']: row['initiative_id'] for row in self.init_list}

        self.evnt_list = db.execute_query("SELECT event_title, event_id FROM event;")

        self.evnt_dict = {row['event_title']: row['event_id'] for row in self.evnt_list}

        self.plan_list = db.execute_query("SELECT plan_name, plan_id FROM plan;")

        self.plan_dict = {row['plan_name']: row['plan_id'] for row in self.plan_list}

        self.metr_list = db.execute_query("SELECT metric_name, metric_id FROM metric;")

        self.metr_dict = {row['metric_name']: row['metric_id'] for row in self.metr_list}

        # ------------------------
        # Create Initiatives Frame
        # ------------------------

        init_frame = ttk.Frame(self.notebook)

        # Create data entry frame and widgets.

        init_entry_frame = ttk.Frame(init_frame)

        init_entry_frame.pack(fill = "x", padx = 10, pady = 10)

        init_initiative_id_label = ttk.Label(init_entry_frame, width = 20, text = "Initiative Id:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        init_initiative_id_entry = ttk.Entry(init_entry_frame, width = 20)
        
        init_initiative_id_entry.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        init_initiative_title_label = ttk.Label(init_entry_frame, width = 20, text = "Initiative Title:").grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        init_initiative_title_entry = ttk.Entry(init_entry_frame, width = 100)
        
        init_initiative_title_entry.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

        init_initiative_description_label= ttk.Label(init_entry_frame, width = 20, text = "Description:").grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")

        init_initiative_description_entry = ttk.Entry(init_entry_frame, width = 100)
        
        init_initiative_description_entry.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

        init_initiative_owner_label = ttk.Label(init_entry_frame, width = 20, text = "Initiative Owner:").grid(row = 3, column = 0, padx = 5, pady = 2, sticky = "w")

        init_initiative_owner_entry = ttk.Entry(init_entry_frame, width = 50)
        
        init_initiative_owner_entry.grid(row = 3, column = 1, padx = 5, pady = 2, sticky = "w")

        init_planned_start_date_label = ttk.Label(init_entry_frame, width = 20, text = "Planned Start Date:").grid(row = 4, column = 0, padx = 5, pady = 2, sticky = "w")

        init_planned_start_date_entry = DateEntry(init_entry_frame, width = 20, date_pattern = "yyyy-mm-dd")
        
        init_planned_start_date_entry.grid(row = 4, column = 1, padx = 5, pady = 2, sticky = "w")

        init_planned_end_date_label = ttk.Label(init_entry_frame, width = 20, text = "Planned End Date:").grid(row = 5, column = 0, padx = 5, pady = 2, sticky = "w")

        init_planned_end_date_entry = DateEntry(init_entry_frame, width = 20, date_pattern = "yyyy-mm-dd")
        
        init_planned_end_date_entry.grid(row = 5, column = 1, padx = 5, pady = 2, sticky = "w")

        init_actual_start_date_label = ttk.Label(init_entry_frame, width = 20, text = "Actual Start Date:").grid(row = 6, column = 0, padx = 5, pady = 2, sticky = "w")

        init_actual_start_date_entry = DateEntry(init_entry_frame, width = 20, date_pattern = "yyyy-mm-dd")
        
        init_actual_start_date_entry.grid(row = 6, column = 1, padx = 5, pady = 2, sticky = "w")

        init_actual_end_date_label = ttk.Label(init_entry_frame, width = 20, text = "Actual End Date:").grid(row = 7, column = 0, padx = 5, pady = 2, sticky = "w")

        init_actual_end_date_entry = DateEntry(init_entry_frame, width = 20, date_pattern = "yyyy-mm-dd")
        
        init_actual_end_date_entry.grid(row = 7, column = 1, padx = 5, pady = 2, sticky = "w")

        # Create button frame and widgets.

        init_button_frame = ttk.Frame(init_frame)

        init_add_btn = ttk.Button(init_button_frame,
                                        command = lambda: self.add_record("initiative"),
                                        text = "Add")
        
        init_add_btn.grid(row = 0, column = 0, padx = 5)

        init_update_btn= ttk.Button(init_button_frame,
                                           command = lambda: self.update_record("initiative"),
                                           text = "Update")
        
        init_update_btn.grid(row = 0, column = 1, padx = 5)

        init_delete_btn = ttk.Button(init_button_frame,
                                           command = lambda: self.delete_record("initiative"),
                                           text = "Delete")
        
        init_delete_btn.grid(row = 0, column = 2, padx = 5)

        init_refresh_btn = ttk.Button(init_button_frame,
                                           command = lambda: self.refresh_records("initiative"),
                                           text = "Refresh")
        
        init_refresh_btn.grid(row = 0, column = 3, padx = 5)

        init_button_frame.pack(fill = "x", padx = 10, pady = 10)

        # Create treeview frame.

        columns = (
            "initiative_id", 
            "initiative_title", 
            "initiative_description", 
            "initiative_owner",
            "planned_start_date", 
            "planned_end_date", 
            "actual_start_date", 
            "actual_end_date"
        )

        init_tree_frame = ttk.Frame(init_frame)

        init_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        init_tree_frame.rowconfigure(1, weight=1)

        init_tree_frame.columnconfigure(0, weight=1)

        init_table_label = ttk.Label(init_tree_frame, width = 20, text = "Initiative Records:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.init_output_table = ttk.Treeview(init_tree_frame, columns = columns, show = "headings")

        for col in columns:
            self.init_output_table.heading(col, text=col.replace("_", " ").title())
            self.init_output_table.column(col, width=100)

        self.init_output_table.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "nsew")

        init_table_sbar = ttk.Scrollbar(init_tree_frame, orient="vertical", command=self.init_output_table.yview)

        self.init_output_table.configure(yscrollcommand=init_table_sbar.set)

        init_table_sbar.grid(row=1, column=1, sticky="ns")

        self.init_output_table.bind("<<TreeviewSelect>>", lambda e: self.select_record("initiative"))

        self.trees["initiative"] = self.init_output_table

        self.notebook.add(init_frame, text = "Initiatives")

        self.frames["Initiatives"] = init_frame

        # Create initiative entries.

        self.entries["initiative"] = {
            "initiative_id": init_initiative_id_entry,
            "initiative_title": init_initiative_title_entry,
            "initiative_description": init_initiative_description_entry,
            "initiative_owner": init_initiative_owner_entry,
            "planned_start_date": init_planned_start_date_entry,
            "planned_end_date": init_planned_end_date_entry,
            "actual_start_date": init_actual_start_date_entry,
            "actual_end_date": init_actual_end_date_entry
        }

        self.refresh_records("initiative") 

        # -------------------
        # Create Metric Frame
        # -------------------

        metr_frame = ttk.Frame(self.notebook)

        # Create data entry frame and widgets.

        metr_entry_frame = ttk.Frame(metr_frame)

        metr_entry_frame.pack(fill = "x", padx = 10, pady = 10)

        # Metric id.

        metr_metric_id_label = ttk.Label(metr_entry_frame,
                                  width = 20,
                                  text = "Metric Id:"
                                  ).grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")
        
        metr_metric_id_entry = ttk.Entry(metr_entry_frame, width = 20)

        metr_metric_id_entry.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        # Initiative id.

        metr_initiative_id_label = ttk.Label(metr_entry_frame,
                                  width = 20,
                                  text = "Initiative Id:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        self.metr_initiative_id_entry = self.binder.add_combobox("metr_init_id", 
                                                                 self.init_dict, 
                                                                 1, 
                                                                 1,
                                                                 50,
                                                                 parent = metr_entry_frame)

        metr_metric_name_label = ttk.Label(metr_entry_frame,
                                    width = 20,
                                    text = "Metric Name:"
                                    ).grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")
        
        metr_metric_name_entry = ttk.Entry(metr_entry_frame, width = 100)

        metr_metric_name_entry.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

        metr_metric_definition_label = ttk.Label(metr_entry_frame,
                                    width = 20,
                                    text = "Definition:"
                                    ).grid(row = 3, column = 0, padx = 5, pady = 2, sticky = "w")
        
        metr_metric_definition_entry = ttk.Entry(metr_entry_frame, width = 100)

        metr_metric_definition_entry.grid(row = 3, column = 1, padx = 5, pady = 2, sticky = "w")

        metr_is_plan_level_var = tk.BooleanVar()

        metr_is_plan_level_label = ttk.Label(metr_entry_frame,
                                    width = 20,
                                    text = "Is Plan  Level:"
                                    ).grid(row = 4, column = 0, padx = 5, pady = 2, sticky = "w")

        metr_is_plan_level_check = ttk.Checkbutton(metr_entry_frame, variable=metr_is_plan_level_var)
        
        metr_is_plan_level_check.grid(row = 4, column = 1, padx = 5, pady = 2, sticky = "w")

        metr_collection_frequency_label = ttk.Label(metr_entry_frame,
                                    width = 20,
                                    text = "Collection Frequency:"
                                    ).grid(row = 5, column = 0, padx = 5, pady = 2, sticky = "w")
        
        metr_collection_frequency_entry = ttk.Entry(metr_entry_frame, width = 30)

        metr_collection_frequency_entry.grid(row = 5, column = 1, padx = 5, pady = 2, sticky = "w")

        self.notebook.add(metr_frame, text = "Metrics")

        self.frames["Metrics"] = metr_frame

        # Create button frame and widgets.

        metr_button_frame = ttk.Frame(metr_frame)

        metr_add_btn = ttk.Button(metr_button_frame,
                                        command = lambda: self.add_record("metric"),
                                        text = "Add")
        
        metr_add_btn.grid(row = 0, column = 0, padx = 5)

        metr_update_btn = ttk.Button(metr_button_frame,
                                           command = lambda: self.update_record("metric"),
                                           text = "Update")
        
        metr_update_btn.grid(row = 0, column = 1, padx = 5)

        metr_delete_btn = ttk.Button(metr_button_frame,
                                           command = lambda: self.delete_record("metric"),
                                           text = "Delete")
        
        metr_delete_btn.grid(row = 0, column = 2, padx = 5)

        metr_refresh_btn= ttk.Button(metr_button_frame,
                                           command = lambda: self.refresh_records("metric"),
                                           text = "Refresh")
        
        metr_refresh_btn.grid(row = 0, column = 3, padx = 5)

        metr_button_frame.pack(fill = "x", padx = 10, pady = 10)

        # Create treeview frame.

        columns = (
            "metric_id",
            "initiative_id", 
            "metric_name", 
            "metric_definition", 
            "is_plan_level",
            "collection_frequency"
        )

        metr_tree_frame = ttk.Frame(metr_frame)

        metr_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        metr_tree_frame.rowconfigure(1, weight=1)

        metr_tree_frame.columnconfigure(0, weight=1)

        metr_output_label = ttk.Label(metr_tree_frame, width = 20, text = "Metric Records:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.metr_output_table = ttk.Treeview(metr_tree_frame, columns = columns, show = "headings")

        for col in columns:
            self.metr_output_table.heading(col, text=col.replace("_", " ").title())
            self.metr_output_table.column(col, width=100)

        self.metr_output_table.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "nsew")

        metr_table_sbar = ttk.Scrollbar(metr_tree_frame, orient="vertical", command=self.metr_output_table.yview)

        self.metr_output_table.configure(yscrollcommand=metr_table_sbar.set)

        metr_table_sbar.grid(row=1, column=1, sticky="ns")

        self.metr_output_table.bind("<<TreeviewSelect>>", lambda e: self.select_record("metric"))

        self.trees["metric"] = self.metr_output_table

        self.notebook.add(metr_frame, text = "Metrics")

        self.frames["Metrics"] = metr_frame

        # Create metric entries.

        init_id = self.binder.get_selected_id("metr_initiative_id_entry")

        self.entries["metric"] = {
            "metric_id": metr_metric_id_entry,
            "initiative_id": self.metr_initiative_id_entry,
            "metric_name": metr_metric_name_entry,
            "metric_definition": metr_metric_definition_entry,
            "is_plan_level": metr_is_plan_level_check,
            "collection_frequency": metr_collection_frequency_entry
        }

        self.refresh_records("metric") 

        # ------------------
        # Create Event Frame
        # ------------------

        evnt_frame = ttk.Frame(self.notebook)

        # Create data entry frame and widgets.

        evnt_entry_frame = ttk.Frame(evnt_frame)

        evnt_entry_frame.pack(fill = "x", padx = 10, pady = 10)

        # Event id.

        evnt_event_id_label = ttk.Label(evnt_entry_frame,
                                  width = 20,
                                  text = "Event Id:"
                                  ).grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")
        
        evnt_event_id_entry = ttk.Entry(evnt_entry_frame, width = 20)

        evnt_event_id_entry.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        # Initiative id.

        evnt_initiative_id_label = ttk.Label(evnt_entry_frame,
                                  width = 20,
                                  text = "Initiative Id:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        self.evnt_initiative_id_entry = self.binder.add_combobox("evnt_init_id", 
                                                                 self.init_dict, 
                                                                 1, 
                                                                 1, 
                                                                 50,
                                                                 parent = evnt_entry_frame)

        # Event title.

        evnt_event_title_label = ttk.Label(evnt_entry_frame,
                                  width = 20,
                                  text = "Event Title:"
                                  ).grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")

        evnt_event_title_entry = ttk.Entry(evnt_entry_frame, width = 100)

        evnt_event_title_entry.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

        # Event description.

        evnt_event_description_label = ttk.Label(evnt_entry_frame,
                                  width = 20,
                                  text = "Description:"
                                  ).grid(row = 3, column = 0, padx = 5, pady = 2, sticky = "w")

        evnt_event_description_entry = ttk.Entry(evnt_entry_frame, width = 100)

        evnt_event_description_entry.grid(row = 3, column = 1, padx = 5, pady = 2, sticky = "w")

        # Event date.

        evnt_event_date_label = ttk.Label(evnt_entry_frame, width = 20, text = "Event Date:").grid(row = 4, column = 0, padx = 5, pady = 2, sticky = "w")

        evnt_event_date_entry = DateEntry(evnt_entry_frame, width = 20, date_pattern = "yyyy-mm-dd")
        
        evnt_event_date_entry.grid(row = 4, column = 1, padx = 5, pady = 2, sticky = "w")

        # Activation id.

        evnt_activation_id_label = ttk.Label(evnt_entry_frame,
                                  width = 20,
                                  text = "Activation Id:"
                                  ).grid(row = 5, column = 0, padx = 5, pady = 2, sticky = "w")

        evnt_activation_id_entry = ttk.Entry(evnt_entry_frame)

        evnt_activation_id_entry.grid(row = 5, column = 1, padx = 5, pady = 2, sticky = "w")

        self.notebook.add(evnt_frame, text = "Events")

        self.frames["Events"] = evnt_frame

        # Create button frame and widgets.

        evnt_button_frame = ttk.Frame(evnt_frame)

        evnt_add_btn = ttk.Button(evnt_button_frame,
                                        command = lambda: self.add_record("event"),
                                        text = "Add")
        
        evnt_add_btn.grid(row = 0, column = 0, padx = 5)

        evnt_update_btn = ttk.Button(evnt_button_frame,
                                           command = lambda: self.update_record("event"),
                                           text = "Update")
        
        evnt_update_btn.grid(row = 0, column = 1, padx = 5)

        evnt_delete_btn = ttk.Button(evnt_button_frame,
                                           command = lambda: self.delete_record("event"),
                                           text = "Delete")
        
        evnt_delete_btn.grid(row = 0, column = 2, padx = 5)

        evnt_refresh_btn= ttk.Button(evnt_button_frame,
                                           command = lambda: self.refresh_records("event"),
                                           text = "Refresh")
        
        evnt_refresh_btn.grid(row = 0, column = 3, padx = 5)

        evnt_button_frame.pack(fill = "x", padx = 10, pady = 10)

        # Create treeview frame.

        columns = (
            "event_id",
            "initiative_id", 
            "event_title", 
            "event_description", 
            "event_date",
            "activation_id"
        )

        evnt_tree_frame = ttk.Frame(evnt_frame)

        evnt_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        evnt_tree_frame.rowconfigure(1, weight=1)

        evnt_tree_frame.columnconfigure(0, weight=1)

        evnt_output_label = ttk.Label(evnt_tree_frame, width = 20, text = "Event Records:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.evnt_output_table = ttk.Treeview(evnt_tree_frame, columns = columns, show = "headings")

        for col in columns:
            self.evnt_output_table.heading(col, text=col.replace("_", " ").title())
            self.evnt_output_table.column(col, width=100)

        self.evnt_output_table.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "nsew")

        evnt_table_sbar = ttk.Scrollbar(evnt_tree_frame, orient="vertical", command=self.evnt_output_table.yview)

        self.evnt_output_table.configure(yscrollcommand=evnt_table_sbar.set)

        evnt_table_sbar.grid(row=1, column=1, sticky="ns")

        self.evnt_output_table.bind("<<TreeviewSelect>>", lambda e: self.select_record("event"))

        self.trees["event"] = self.evnt_output_table

        self.notebook.add(evnt_frame, text = "Events")

        self.frames["Events"] = evnt_frame

        # Create event entries.

        self.entries["event"] = {
            "event_id": evnt_event_id_entry,
            "initiative_id": self.evnt_initiative_id_entry,
            "event_title": evnt_event_title_entry,
            "event_description": evnt_event_description_entry,
            "event_date": evnt_event_date_entry,
            "activation_id": evnt_activation_id_entry
        }

        self.refresh_records("event") 

        # -----------------
        # Create Plan Frame
        # -----------------

        plan_frame = ttk.Frame(self.notebook)

        # Create data entry frame and widgets.

        plan_entry_frame = ttk.Frame(plan_frame)

        plan_entry_frame.pack(fill = "x", padx = 10, pady = 10)

        # Plan id.

        plan_plan_id_label = ttk.Label(plan_entry_frame,
                                  width = 20,
                                  text = "Plan Id:"
                                  ).grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")
        
        plan_plan_id_entry = ttk.Entry(plan_entry_frame, width = 20)

        plan_plan_id_entry.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        # Plan name.

        plan_plan_name_label = ttk.Label(plan_entry_frame,
                                  width = 20,
                                  text = "Plan Name:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        plan_plan_name_entry = ttk.Entry(plan_entry_frame)

        plan_plan_name_entry.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

        # Create button frame and widgets.

        plan_button_frame = ttk.Frame(plan_frame)

        plan_add_btn = ttk.Button(plan_button_frame,
                                        command = lambda: self.add_record("plan"),
                                        text = "Add")
        
        plan_add_btn.grid(row = 0, column = 0, padx = 5)

        plan_update_btn = ttk.Button(plan_button_frame,
                                           command = lambda: self.update_record("plan"),
                                           text = "Update")
        
        plan_update_btn.grid(row = 0, column = 1, padx = 5)

        plan_delete_btn = ttk.Button(plan_button_frame,
                                           command = lambda: self.delete_record("plan"),
                                           text = "Delete")
        
        plan_delete_btn.grid(row = 0, column = 2, padx = 5)

        plan_refresh_btn= ttk.Button(plan_button_frame,
                                           command = lambda: self.refresh_records("plan"),
                                           text = "Refresh")
        
        plan_refresh_btn.grid(row = 0, column = 3, padx = 5)

        plan_button_frame.pack(fill = "x", padx = 10, pady = 10)

        # Create treeview frame.

        columns = (
            "plan_id",
            "plan_name"
        )

        plan_tree_frame = ttk.Frame(plan_frame)

        plan_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        plan_tree_frame.rowconfigure(1, weight=1)

        plan_tree_frame.columnconfigure(0, weight=1)

        plan_output_label = ttk.Label(plan_tree_frame, width = 20, text = "Plan Records:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.plan_output_table = ttk.Treeview(plan_tree_frame, columns = columns, show = "headings")

        for col in columns:
            self.plan_output_table.heading(col, text=col.replace("_", " ").title())
            self.plan_output_table.column(col, width=100)

        self.plan_output_table.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "nsew")

        plan_table_sbar = ttk.Scrollbar(plan_tree_frame, orient="vertical", command=self.plan_output_table.yview)

        self.plan_output_table.configure(yscrollcommand=plan_table_sbar.set)

        plan_table_sbar.grid(row=1, column=1, sticky="ns")

        self.plan_output_table.bind("<<TreeviewSelect>>", lambda e: self.select_record("plan"))

        self.trees["plan"] = self.plan_output_table

        self.notebook.add(plan_frame, text = "Plans")

        self.frames["Plans"] = plan_frame

        # Create plan entries.

        self.entries["plan"] = {
            "plan_id": plan_plan_id_entry,
            "plan_name": plan_plan_name_entry
        }

        self.refresh_records("plan") 

        # -------------------------
        # Create Events Plans Frame
        # -------------------------

        ep_frame = ttk.Frame(self.notebook)

        # Create data entry frame and widgets.

        ep_entry_frame = ttk.Frame(ep_frame)

        ep_entry_frame.pack(fill = "x", padx = 10, pady = 10)

        # Plan id.

        ep_plan_id_label = ttk.Label(ep_entry_frame,
                                  width = 20,
                                  text = "Plan Id:"
                                  ).grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.ep_plan_id_entry = self.binder.add_combobox("ep_plan_id", 
                                                          self.plan_dict, 
                                                          0, 
                                                          1, 
                                                          50,
                                                          parent = ep_entry_frame)

        # Event id.

        ep_event_id_label = ttk.Label(ep_entry_frame,
                                  width = 20,
                                  text = "Event Id:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        self.ep_event_id_entry = self.binder.add_combobox("ep_event_id", 
                                                          self.evnt_dict, 
                                                          1, 
                                                          1, 
                                                          70,
                                                          parent = ep_entry_frame)

        # Create button frame and widgets.

        ep_button_frame = ttk.Frame(ep_frame)

        ep_add_btn = ttk.Button(ep_button_frame,
                                        command = lambda: self.add_record("event_plan"),
                                        text = "Add")
        
        ep_add_btn.grid(row = 0, column = 0, padx = 5)

        ep_update_btn = ttk.Button(ep_button_frame,
                                           command = lambda: self.update_record("event_plan"),
                                           text = "Update")
        
        ep_update_btn.grid(row = 0, column = 1, padx = 5)

        ep_delete_btn = ttk.Button(ep_button_frame,
                                           command = lambda: self.delete_record("event_plan"),
                                           text = "Delete")
        
        ep_delete_btn.grid(row = 0, column = 2, padx = 5)

        ep_refresh_btn= ttk.Button(ep_button_frame,
                                           command = lambda: self.refresh_records("event_plan"),
                                           text = "Refresh")
        
        ep_refresh_btn.grid(row = 0, column = 3, padx = 5)

        ep_button_frame.pack(fill = "x", padx = 10, pady = 10)

        # Create treeview frame.

        columns = (
            "event_id",
            "plan_id"
        )

        ep_tree_frame = ttk.Frame(ep_frame)

        ep_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ep_tree_frame.rowconfigure(1, weight=1)

        ep_tree_frame.columnconfigure(0, weight=1)

        ep_output_label = ttk.Label(ep_tree_frame, width = 20, text = "Event Plan Records:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.ep_output_table = ttk.Treeview(ep_tree_frame, columns = columns, show = "headings")

        for col in columns:
            self.ep_output_table.heading(col, text=col.replace("_", " ").title())
            self.ep_output_table.column(col, width=100)

        self.ep_output_table.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "nsew")

        ep_table_sbar = ttk.Scrollbar(ep_tree_frame, orient="vertical", command=self.ep_output_table.yview)

        self.ep_output_table.configure(yscrollcommand=ep_table_sbar.set)

        ep_table_sbar.grid(row=1, column=1, sticky="ns")

        self.ep_output_table.bind("<<TreeviewSelect>>", lambda e: self.select_record("event_plan"))

        self.trees["event_plan"] = self.ep_output_table

        self.notebook.add(ep_frame, text = "Events Plans")

        self.frames["Events Plans"] = ep_frame

        # Create event plan entries.

        self.entries["event_plan"] = {
            "event_id": self.ep_event_id_entry,
            "plan_id": self.ep_plan_id_entry
        }

        self.refresh_records("event_plan") 

        # --------------------------------
        # Create Global Metric Value Frame
        # --------------------------------

        gmv_frame = ttk.Frame(self.notebook)

        # Create data entry frame and widgets.

        gmv_entry_frame = ttk.Frame(gmv_frame)

        gmv_entry_frame.pack(fill = "x", padx = 10, pady = 10)

        # Global value id.

        gmv_global_value_id_label = ttk.Label(gmv_entry_frame,
                                  width = 20,
                                  text = "Value Id:"
                                  ).grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")
        
        gmv_global_value_id_entry = ttk.Entry(gmv_entry_frame, width = 20)

        gmv_global_value_id_entry.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        # Metric id.

        gmv_metric_id_label = ttk.Label(gmv_entry_frame,
                                  width = 20,
                                  text = "Metric Id:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        self.gmv_metric_id_entry = self.binder.add_combobox("gmv_metric_id", 
                                                          self.metr_dict, 
                                                          1, 
                                                          1, 
                                                          50,
                                                          parent = gmv_entry_frame)

        # Metric date.

        gmv_metric_date_label = ttk.Label(gmv_entry_frame, width = 20, text = "Metric Date:").grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")

        gmv_metric_date_entry = DateEntry(gmv_entry_frame, width = 20, date_pattern = "yyyy-mm-dd")
        
        gmv_metric_date_entry.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

        # Actual value.

        gmv_actual_value_label = ttk.Label(gmv_entry_frame,
                                  width = 20,
                                  text = "Actual Value:"
                                  ).grid(row = 3, column = 0, padx = 5, pady = 2, sticky = "w")
        
        gmv_actual_value_entry = ttk.Entry(gmv_entry_frame, width = 20)

        gmv_actual_value_entry.grid(row = 3, column = 1, padx = 5, pady = 2, sticky = "w")

        # Create button frame and widgets.

        gmv_button_frame = ttk.Frame(gmv_frame)

        gmv_add_btn = ttk.Button(gmv_button_frame,
                                        command = lambda: self.add_record("global_metric_value"),
                                        text = "Add")
        
        gmv_add_btn.grid(row = 0, column = 0, padx = 5)

        gmv_update_btn = ttk.Button(gmv_button_frame,
                                           command = lambda: self.update_record("global_metric_value"),
                                           text = "Update")
        
        gmv_update_btn.grid(row = 0, column = 1, padx = 5)

        gmv_delete_btn = ttk.Button(gmv_button_frame,
                                           command = lambda: self.delete_record("global_metric_value"),
                                           text = "Delete")
        
        gmv_delete_btn.grid(row = 0, column = 2, padx = 5)

        gmv_refresh_btn= ttk.Button(gmv_button_frame,
                                           command = lambda: self.refresh_records("global_metric_value"),
                                           text = "Refresh")
        
        gmv_refresh_btn.grid(row = 0, column = 3, padx = 5)

        gmv_button_frame.pack(fill = "x", padx = 10, pady = 10)

        # Create treeview frame.

        columns = (
            "global_value_id",
            "metric_id",
            "metric_date",
            "actual_value"
        )

        gmv_tree_frame = ttk.Frame(gmv_frame)

        gmv_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        gmv_tree_frame.rowconfigure(1, weight=1)

        gmv_tree_frame.columnconfigure(0, weight=1)

        gmv_output_label = ttk.Label(gmv_tree_frame, width = 20, text = "Global Value Records:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.gmv_output_table = ttk.Treeview(gmv_tree_frame, columns = columns, show = "headings")

        for col in columns:
            self.gmv_output_table.heading(col, text=col.replace("_", " ").title())
            self.gmv_output_table.column(col, width=100)

        self.gmv_output_table.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "nsew")

        gmv_table_sbar = ttk.Scrollbar(gmv_tree_frame, orient="vertical", command=self.gmv_output_table.yview)

        self.gmv_output_table.configure(yscrollcommand=gmv_table_sbar.set)

        gmv_table_sbar.grid(row=1, column=1, sticky="ns")

        self.gmv_output_table.bind("<<TreeviewSelect>>", lambda e: self.select_record("global_metric_value"))

        self.trees["global_metric_value"] = self.gmv_output_table

        self.notebook.add(gmv_frame, text = "Global Metric Values")

        self.frames["Global Metric Values"] = gmv_frame

        # Create global metric value entries.

        self.entries["global_metric_value"] = {
            "global_value_id": gmv_global_value_id_entry,
            "metric_id": self.gmv_metric_id_entry,
            "metric_date": gmv_metric_date_entry,
            "actual_value": gmv_actual_value_entry
        }

        self.refresh_records("global_metric_value") 

        # ------------------------------
        # Create Plan Metric Value Frame
        # ------------------------------

        pmv_frame = ttk.Frame(self.notebook)

        # Create data entry frame and widgets.

        pmv_entry_frame = ttk.Frame(pmv_frame)

        pmv_entry_frame.pack(fill = "x", padx = 10, pady = 10)

        # Plan value id.

        pmv_global_value_id_label = ttk.Label(pmv_entry_frame,
                                  width = 20,
                                  text = "Value Id:"
                                  ).grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")
        
        pmv_global_value_id_entry = ttk.Entry(pmv_entry_frame, width = 20)

        pmv_global_value_id_entry.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        # Metric id.

        pmv_metric_id_label = ttk.Label(pmv_entry_frame,
                                  width = 20,
                                  text = "Metric Id:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        self.pmv_metric_id_entry = self.binder.add_combobox("pmv_metric_id", 
                                                          self.metr_dict, 
                                                          1, 
                                                          1, 
                                                          50,
                                                          parent = pmv_entry_frame)

        # Plan id.

        pmv_plan_id_label = ttk.Label(pmv_entry_frame,
                                  width = 20,
                                  text = "Plan Id:"
                                  ).grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")

        self.pmv_plan_id_entry = self.binder.add_combobox("pmv_plan_id", 
                                                          self.plan_dict, 
                                                          2, 
                                                          1, 
                                                          50,
                                                          parent = pmv_entry_frame)

        # Metric date.

        pmv_metric_date_label = ttk.Label(pmv_entry_frame, width = 20, text = "Metric Date:").grid(row = 3, column = 0, padx = 5, pady = 2, sticky = "w")

        pmv_metric_date_entry = DateEntry(pmv_entry_frame, width = 20, date_pattern = "yyyy-mm-dd")
        
        pmv_metric_date_entry.grid(row = 3, column = 1, padx = 5, pady = 2, sticky = "w")

        # Actual value.

        pmv_actual_value_label = ttk.Label(pmv_entry_frame,
                                  width = 20,
                                  text = "Actual Value:"
                                  ).grid(row = 4, column = 0, padx = 5, pady = 2, sticky = "w")
        
        pmv_actual_value_entry = ttk.Entry(pmv_entry_frame, width = 20)

        pmv_actual_value_entry.grid(row = 4, column = 1, padx = 5, pady = 2, sticky = "w")

        # Create button frame and widgets.

        pmv_button_frame = ttk.Frame(pmv_frame)

        pmv_add_btn = ttk.Button(pmv_button_frame,
                                        command = lambda: self.add_record("plan_metric_value"),
                                        text = "Add")
        
        pmv_add_btn.grid(row = 0, column = 0, padx = 5)

        pmv_update_btn = ttk.Button(pmv_button_frame,
                                           command = lambda: self.update_record("plan_metric_value"),
                                           text = "Update")
        
        pmv_update_btn.grid(row = 0, column = 1, padx = 5)

        pmv_delete_btn = ttk.Button(pmv_button_frame,
                                           command = lambda: self.delete_record("plan_metric_value"),
                                           text = "Delete")
        
        pmv_delete_btn.grid(row = 0, column = 2, padx = 5)

        pmv_refresh_btn= ttk.Button(pmv_button_frame,
                                           command = lambda: self.refresh_records("plan_metric_value"),
                                           text = "Refresh")
        
        pmv_refresh_btn.grid(row = 0, column = 3, padx = 5)

        pmv_button_frame.pack(fill = "x", padx = 10, pady = 10)

        # Create treeview frame.

        columns = (
            "plan_value_id",
            "metric_id",
            "plan_id",
            "metric_date",
            "actual_value"
        )

        pmv_tree_frame = ttk.Frame(pmv_frame)

        pmv_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        pmv_tree_frame.rowconfigure(1, weight=1)

        pmv_tree_frame.columnconfigure(0, weight=1)

        pmv_output_label = ttk.Label(pmv_tree_frame, width = 20, text = "Plan Value Records:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.pmv_output_table = ttk.Treeview(pmv_tree_frame, columns = columns, show = "headings")

        for col in columns:
            self.pmv_output_table.heading(col, text=col.replace("_", " ").title())
            self.pmv_output_table.column(col, width=100)

        self.pmv_output_table.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "nsew")

        pmv_table_sbar = ttk.Scrollbar(pmv_tree_frame, orient="vertical", command=self.pmv_output_table.yview)

        self.pmv_output_table.configure(yscrollcommand=pmv_table_sbar.set)

        pmv_table_sbar.grid(row=1, column=1, sticky="ns")

        self.pmv_output_table.bind("<<TreeviewSelect>>", lambda e: self.select_record("plan_metric_value"))

        self.trees["plan_metric_value"] = self.pmv_output_table

        self.notebook.add(pmv_frame, text = "Plan Metric Values")

        self.frames["Plan Metric Values"] = pmv_frame

        # Create plan metric value entries.

        self.entries["plan_metric_value"] = {
            "plan_value_id": pmv_global_value_id_entry,
            "metric_id": self.pmv_metric_id_entry,
            "plan_id": self.pmv_plan_id_entry,
            "metric_date": pmv_metric_date_entry,
            "actual_value": pmv_actual_value_entry
        }

        self.refresh_records("plan_metric_value") 

        # -----------------------
        # Create User Query Frame
        # -----------------------

        uq_frame = ttk.Frame(self.notebook)

        # Create data entry frame and widgets.

        uq_entry_frame = ttk.Frame(uq_frame)
        
        uq_entry_frame.pack(fill="x", padx=10, pady=10)

        # Create left and right frames inside uq_entry_frame.

        uq_left_frame = ttk.Frame(uq_entry_frame)

        uq_left_frame.pack(side="left", fill="y")

        uq_right_frame = ttk.Frame(uq_entry_frame)

        uq_right_frame.pack(side="left", fill="both", expand=True)
        
        # Query id.

        uq_query_id_label = ttk.Label(uq_left_frame,
                                  width = 20,
                                  text = "Query Id:"
                                  ).grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")
        
        uq_query_id_entry = ttk.Entry(uq_left_frame, width = 20)

        uq_query_id_entry.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        # Query title.

        uq_query_title_label = ttk.Label(uq_left_frame,
                                  width = 20,
                                  text = "Query Title:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")
        
        uq_query_title_entry = ttk.Entry(uq_left_frame, width = 100)

        uq_query_title_entry.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

        # Query description.

        uq_query_description_label = ttk.Label(uq_left_frame,
                                  width = 20,
                                  text = "Query Description:"
                                  ).grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")
        
        uq_query_description_entry = ttk.Entry(uq_left_frame, width = 100)

        uq_query_description_entry.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

        # Query purpose.

        uq_query_purpose_label = ttk.Label(uq_left_frame,
                                  width = 20,
                                  text = "Query Purpose:"
                                  ).grid(row = 3, column = 0, padx = 5, pady = 2, sticky = "w")
        
        uq_query_purpose_entry = ttk.Entry(uq_left_frame, width = 100)

        uq_query_purpose_entry.grid(row = 3, column = 1, padx = 5, pady = 2, sticky = "w")

        # Query string.

        uq_query_string_label = ttk.Label(uq_left_frame,
                                  width = 20,
                                  text = "Query String:"
                                  ).grid(row = 4, column = 0, padx = 5, pady = 2, sticky = "w")
        
        style = ttk.Style()

        entry_font_name = style.lookup('TEntry', 'font')

        # Fallback if style lookup doesn't return a font name

        if not entry_font_name:
            entry_font_name = 'TkDefaultFont'

        # Create a font object using the ttk.Entry font

        entry_font = tkfont.nametofont(entry_font_name)
        
        self.uq_query_string_entry = tk.Text(uq_left_frame, height = 10, width = 100, wrap = "word", font = entry_font)

        self.uq_query_string_entry.grid(row = 4, column = 1, padx = 5, pady = 2, sticky = "w")

        # Checkbox frame.

        uq_checkbox_frame = ttk.Frame(uq_right_frame)

        uq_checkbox_frame.pack(anchor="center")

        # Set operation.

        uq_set_operation_var = tk.BooleanVar()

        uq_set_operation_label = ttk.Label(uq_checkbox_frame,
                                    width = 20,
                                    text = "Set Operation:"
                                    ).grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        uq_set_operation_check = ttk.Checkbutton(uq_checkbox_frame, variable=uq_set_operation_var)

        uq_set_operation_check.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        # Set membership.

        uq_set_membership_var = tk.BooleanVar()

        uq_set_membership_label = ttk.Label(uq_checkbox_frame,
                                    width = 20,
                                    text = "Set Membership:"
                                    ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        uq_set_membership_check = ttk.Checkbutton(uq_checkbox_frame, variable=uq_set_membership_var)

        uq_set_membership_check.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

        # Set comparison.

        uq_set_comparison_var = tk.BooleanVar()

        uq_set_comparison_label = ttk.Label(uq_checkbox_frame,
                                    width = 20,
                                    text = "Set Comparison:"
                                    ).grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")

        uq_set_comparison_check = ttk.Checkbutton(uq_checkbox_frame, variable=uq_set_comparison_var)

        uq_set_comparison_check.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

        # Subquery.

        uq_subquery_var = tk.BooleanVar()

        uq_subquery_label = ttk.Label(uq_checkbox_frame,
                                    width = 20,
                                    text = "Subquery:"
                                    ).grid(row = 3, column = 0, padx = 5, pady = 2, sticky = "w")

        uq_subquery_check = ttk.Checkbutton(uq_checkbox_frame, variable=uq_subquery_var)

        uq_subquery_check.grid(row = 3, column = 1, padx = 5, pady = 2, sticky = "w")

        # CTE.

        uq_cte_var = tk.BooleanVar()

        uq_cte_label = ttk.Label(uq_checkbox_frame,
                                    width = 20,
                                    text = "CTE:"
                                    ).grid(row = 4, column = 0, padx = 5, pady = 2, sticky = "w")

        uq_cte_check = ttk.Checkbutton(uq_checkbox_frame, variable=uq_cte_var)

        uq_cte_check.grid(row = 4, column = 1, padx = 5, pady = 2, sticky = "w")

        # Aggregate function.

        uq_aggregate_function_var = tk.BooleanVar()

        uq_aggregate_function_label = ttk.Label(uq_checkbox_frame,
                                    width = 20,
                                    text = "Aggregate Function:"
                                    ).grid(row = 5, column = 0, padx = 5, pady = 2, sticky = "w")

        uq_aggregate_function_check = ttk.Checkbutton(uq_checkbox_frame, variable=uq_aggregate_function_var)

        uq_aggregate_function_check.grid(row = 5, column = 1, padx = 5, pady = 2, sticky = "w")

        # window function.

        uq_window_function_var = tk.BooleanVar()

        uq_window_function_label = ttk.Label(uq_checkbox_frame,
                                    width = 20,
                                    text = "Window Function:"
                                    ).grid(row = 6, column = 0, padx = 5, pady = 2, sticky = "w")

        uq_window_function_check = ttk.Checkbutton(uq_checkbox_frame, variable=uq_window_function_var)

        uq_window_function_check.grid(row = 6, column = 1, padx = 5, pady = 2, sticky = "w")

        # OLAP.

        uq_olap_var = tk.BooleanVar()

        uq_olap_label = ttk.Label(uq_checkbox_frame,
                                    width = 20,
                                    text = "OLAP:"
                                    ).grid(row = 7, column = 0, padx = 5, pady = 2, sticky = "w")

        uq_olap_check = ttk.Checkbutton(uq_checkbox_frame, variable=uq_olap_var)

        uq_olap_check.grid(row = 7, column = 1, padx = 5, pady = 2, sticky = "w")

        # Create button frame and widgets.

        uq_button_frame = ttk.Frame(uq_frame)

        uq_add_btn = ttk.Button(uq_button_frame,
                                        command = lambda: self.validate_and_add("user_query"),
                                        text = "Add")
        
        uq_add_btn.grid(row = 0, column = 0, padx = 5)

        uq_update_btn = ttk.Button(uq_button_frame,
                                           command = lambda: self.validate_and_update("user_query"),
                                           text = "Update")
        
        uq_update_btn.grid(row = 0, column = 1, padx = 5)

        uq_delete_btn = ttk.Button(uq_button_frame,
                                           command = lambda: self.delete_record("user_query"),
                                           text = "Delete")
        
        uq_delete_btn.grid(row = 0, column = 2, padx = 5)

        uq_refresh_btn= ttk.Button(uq_button_frame,
                                           command = lambda: self.refresh_records("user_query"),
                                           text = "Refresh")
        
        uq_refresh_btn.grid(row = 0, column = 3, padx = 5)

        uq_button_frame.pack(fill = "x", padx = 10, pady = 10)

        # Create treeview frame.

        columns = (
            "query_id",
            "query_title",
            "query_description",
            "query_purpose",
            "query_string",
            "set_operation",
            "set_membership",
            "set_comparison",
            "subquery",
            "cte",
            "aggregate_function",
            "window_function",
            "olap"
        )

        uq_tree_frame = ttk.Frame(uq_frame)

        uq_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        uq_tree_frame.rowconfigure(1, weight=1)

        uq_tree_frame.columnconfigure(0, weight=1)

        uq_output_label = ttk.Label(uq_tree_frame, width = 20, text = "User Query Records:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.uq_output_table = ttk.Treeview(uq_tree_frame, columns = columns, show = "headings")

        for col in columns:
            self.uq_output_table.heading(col, text=col.replace("_", " ").title())
            self.uq_output_table.column(col, width=100)

        self.uq_output_table.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "nsew")

        uq_table_sbar = ttk.Scrollbar(uq_tree_frame, orient="vertical", command=self.uq_output_table.yview)

        self.uq_output_table.configure(yscrollcommand=uq_table_sbar.set)

        uq_table_sbar.grid(row=1, column=1, sticky="ns")

        self.uq_output_table.bind("<<TreeviewSelect>>", lambda e: self.select_record("user_query"))

        self.trees["user_query"] = self.uq_output_table

        self.notebook.add(uq_frame, text = "User Queries")

        self.frames["User Queries"] = uq_frame

        # Create user query entries.

        self.entries["user_query"] = {
            "query_id": uq_query_id_entry,
            "query_title": uq_query_title_entry,
            "query_description": uq_query_description_entry,
            "query_purpose": uq_query_purpose_entry,
            "query_string": self.uq_query_string_entry,
            "set_operation": uq_set_operation_check,
            "set_membership": uq_set_membership_check,
            "set_comparison": uq_set_comparison_check,
            "subquery": uq_subquery_check,
            "cte": uq_cte_check,
            "aggregate_function": uq_aggregate_function_check,
            "window_function": uq_window_function_check,
            "olap": uq_olap_check
        }

        self.refresh_records("user_query") 

        # ----------------------
        # Create Run Query Frame
        # ----------------------

        query_frame = ttk.Frame(self.notebook)

        # Create query selection frame.

        query_selection_frame = ttk.Frame(query_frame)

        query_selection_frame.pack(fill = "x", padx = 10, pady = 10)

        predefined_queries = db.execute_query("SELECT query_title, query_string FROM user_query ORDER BY query_title;")

        self.title_to_query_map = {q['query_title']: q['query_string'] for q in predefined_queries}

        self.selected_query_title = tk.StringVar()

        titles = list(self.title_to_query_map.keys())

        query_dropdown_label = ttk.Label(query_selection_frame, text = "Select Query:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        query_dropdown = ttk.Combobox(query_selection_frame,
                                      width = 100,
                                      textvariable = self.selected_query_title,
                                      values = titles).grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")
        
        # Create query selection button frame.

        query_button_frame = ttk.Frame(query_frame)

        execute_query_btn = ttk.Button(query_button_frame,
                                       command = self.run_selected_query,
                                       # image = run_icon,
                                       text = "Run Query")
        
        execute_query_btn.grid(row = 0, column = 0, padx = 5)

        download_btn = ttk.Button(query_button_frame, 
                                  command = self.download_query_result,
                                  text = "Download Result")
        
        download_btn.grid(row = 0, column = 1, padx = 5)

        query_button_frame.pack(fill = "x", padx = 10, pady = 10)

        # Create query output frame.

        self.last_query_result = []

        query_output_frame = ttk.Frame(query_frame)

        query_output_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        lbl_query_output = ttk.Label(query_output_frame, width = 20, text = "Query Result:").grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

        self.query_output_table = ttk.Treeview(query_output_frame)

        self.query_output_table.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "nsew")

        query_output_frame.grid_rowconfigure(1, weight=1)

        query_output_frame.grid_columnconfigure(0, weight=1)

        query_frame.pack()

        self.notebook.add(query_frame, text = "Run Queries")

        self.frames["Run Queries"] = query_frame

    def collect_form_data(self, table_name):

        """
        Collects the current values from form input fields for the specified table.

        This method iterates through the widgets (or direct values) defined in 
        `self.entries[table_name]`, retrieves the current value for each field, 
        and returns a dictionary suitable for use in insert or update operations.

        Parameters:
            table_name (str): The name of the table whose form data should be collected.

        Returns:
            dict: A dictionary mapping field names to their current values.

        Behavior:
            - If the table is not found in `self.entries`, a warning is printed and an 
            empty dictionary is returned.
            - For widgets (Tkinter objects), values are retrieved using `self.binder.get_widget_value()`.
            - For non-widget values (e.g., previously resolved IDs), the value is used as-is.
            - Supports flexible data definitions that may mix widgets and pre-bound values.

        Notes:
            - This method assumes that all widgets in `self.entries[table_name]` are either 
            standard Tkinter widgets or already-resolved values.
            - No type conversion or validation is performed here; consumers of the data are 
            expected to handle that as needed.
        """

        if table_name not in self.entries:
            print(f"Warning: Table '{table_name}' not found in entries.")
            return {}

        form_data = {}
        for field_name, widget_or_value in self.entries[table_name].items():
            if hasattr(widget_or_value, "winfo_exists"):  # It's a Tkinter widget
                value = self.binder.get_widget_value(widget_or_value)
            else:
                # Assume already a direct value (like initiative_id)
                value = widget_or_value

            form_data[field_name] = value
        return form_data

    def add_record(self, table):

        """
        Inserts a new record into the specified table, allowing NULL values in empty fields.

        This method gathers form data from entry widgets associated with the given table, 
        optionally resolves linked identifiers (e.g., initiative ID), and inserts the data 
        into the database. After insertion, it clears the form and refreshes the treeview 
        to reflect the newly added record.

        Parameters:
            table (str): The name of the table into which the new record should be inserted.

        Behavior:
            - If the table is not found in `self.entries`, an error message is displayed and the 
            operation is aborted.
            - Uses `collect_form_data()` to gather values from the input widgets.
            - For the 'metric' table, retrieves the `initiative_id` from a bound entry via 
            `self.binder.get_id_entry_value()`. (This value is currently unused.)
            - Attempts to insert the collected data using `db.insert()`.
            - On success, clears the form and refreshes the record display.
            - On failure, displays an error dialog with exception details.

        Notes:
            - Handles exceptions gracefully with user-facing error messages.
            - Assumes input validation (if any) is handled upstream or within `collect_form_data()`.
            - Allows insertion of records with empty fields (which are treated as NULL).
        """

        if table not in self.entries:
            messagebox.showerror("Error", f"value_app: add_record: error: Entries for {table} not found")
            return
        
        try:

            data = self.collect_form_data(table)

            initiative_title = self.entries["metric"]["initiative_id"]

            # print(f"Selected initiative title: {initiative_title}")

            initiative_id = self.binder.get_id_entry_value("metr_init_id")

            # print(f"Resolved initiative_id: {initiative_id}")

            db.insert(table, data)
            self.clear_fields(table)
            self.refresh_records(table)
        except Exception as e:
            msg_handler.show_error("Error", {e})

    def validate_and_add(self, table_name):

        """
        Validates a user-defined query string before adding a new record to the specified table.

        This method retrieves the input from a Tkinter Text widget, validates it via the 
        database layer, and—if the query is valid—proceeds to add the new record. If validation 
        fails, an error message is displayed and the add operation is aborted.

        Parameters:
            table_name (str): The name of the table to which the new record will be added.

        Behavior:
            - Retrieves query text from `self.uq_query_string_entry`.
            - Uses `db.validate_query()` to validate the syntax and structure of the query.
            - Displays an error dialog if the query is invalid.
            - Calls `self.add_record(table_name)` to insert the record if validation passes.

        Notes:
            - Assumes `db.validate_query()` will raise an exception if the query is invalid.
            - Assumes `add_record()` handles field extraction, validation, and persistence.
        """

        query_text = self.uq_query_string_entry.get("1.0", tk.END).strip()

        try: 
            db.validate_query(query_text)
        except Exception as e:
            msg_handler.show_error("Invalid Query String", {e})
            return

        self.add_record(table_name)

    def update_record(self, table):

        """
        Updates the selected record in the specified table with any modified field values.

        This method compares the current form inputs against the selected record in the treeview 
        and constructs an update only for fields that have non-empty values and are not primary keys. 
        It supports single and composite primary keys (e.g., in the 'event_plan' table), builds a 
        condition dictionary to identify the target record, and then performs the update through the 
        database interface.

        Parameters:
            table (str): The name of the table in which the record is to be updated.

        Behavior:
            - If no record is selected, a warning is displayed and the operation is aborted.
            - Only fields with non-empty values are included in the update payload.
            - Primary key fields are excluded from updates.
            - After updating, the form is cleared and the treeview is refreshed.

        Notes:
            - Assumes the first column (or first two for 'event_plan') form the primary key(s).
            - Relies on `self.binder.get_widget_value()` to retrieve widget values.
            - Relies on `db.update()` to persist changes to the database.
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
            value = self.binder.get_widget_value(widget)

            if value:
                updated_data[col] = value

        if not updated_data:
            msg_handler.show_warning("Warning", "No fields to update.")
            return

        db.update(table, updated_data, conditions)

        self.clear_fields(table)

        self.refresh_records(table)

    def validate_and_update(self, table_name):

        """
        Validates a user-defined query string before updating a record in the specified table.

        This method retrieves the query text from a text widget, attempts to validate it using 
        the database layer, and—if validation passes—proceeds to update the record. If the query 
        is invalid, an error message is displayed and the update is aborted.

        Parameters:
            table_name (str): The name of the table in which the record should be updated.

        Behavior:
            - Retrieves the query from a Tkinter Text widget (`self.uq_query_string_entry`).
            - Uses `db.validate_query()` to ensure the query is syntactically valid.
            - If validation fails, shows an error dialog with the exception message.
            - If validation passes, invokes `self.update_record(table_name)`.

        Notes:
            - Assumes `db.validate_query()` raises an exception on invalid input.
            - Assumes `update_record()` handles the actual persistence logic.
        """

        query_text = self.uq_query_string_entry.get("1.0", tk.END).strip()

        try: 
            db.validate_query(query_text)
        except Exception as e:
            msg_handler.show_error("Invalid Query String", {e})
            return

        self.update_record(table_name)

    def delete_record(self, table):

        """
        Deletes the selected record from the specified table and updates the UI.

        This method retrieves the selected record from the treeview associated with the given table,
        identifies the record using its primary key, prompts the user for confirmation, and deletes
        it from the database. After deletion, it clears the input fields and refreshes the treeview
        to reflect the change.

        Parameters:
            table (str): The name of the table from which the record should be deleted.

        Behavior:
            - If no record is selected, a warning message is shown and the operation is canceled.
            - Assumes the first column returned by `db.get_columns(table)` is the primary key.
            - Prompts the user for confirmation before performing the deletion.

        Notes:
            - The UI is updated by calling `clear_fields()` and `refresh_records()` after deletion.
            - NULL-safe and assumes consistent record-key alignment between UI and database schema.
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
        Refreshes the treeview display by fetching and loading all records from the specified table.

        This method clears any existing rows in the treeview and repopulates it with fresh data 
        retrieved from the database. It ensures that NULL values from the database are converted 
        to empty strings for a cleaner display in the UI.

        Parameters:
            table (str): The name of the table whose records should be fetched and displayed.

        Notes:
            - Assumes `self.trees[table]` refers to the treeview widget associated with the table.
            - Uses `db.fetch_all(table)` to retrieve data as dictionaries.
            - Record values are inserted in the order returned by `record.values()`.
        """

        for row in self.trees[table].get_children():
            self.trees[table].delete(row)

        for record in db.fetch_all(table):
            cleaned_record = tuple("" if v is None else v for v in record.values())
            self.trees[table].insert("", "end", values = cleaned_record)

    def select_record(self, table):

        """
        Populates input widgets with data from the selected record in the treeview.

        When a user selects a row in the treeview associated with the given table, 
        this method retrieves the record's values and populates the corresponding 
        input fields to allow for editing. It assumes that the order of columns 
        in the treeview matches the order of keys in the entries dictionary.

        Parameters:
            table (str): The name of the table whose treeview and input fields are being used.

        Notes:
            - If no item is selected, the method exits without making any changes.
            - None values from the treeview are converted to empty strings before populating fields.
        """

        selected_item = self.trees[table].selection()

        if not selected_item:
            return
        
        values = self.trees[table].item(selected_item)["values"]

        columns = list(self.entries[table].keys())

        for i, col in enumerate(columns):
            widget = self.entries[table][col]
            value = values[i] if values[i] is not None else ""
            self.binder.set_widget_value(widget, value)

    def clear_fields(self, table):

        """
        Clears all input widgets associated with a specific database table.

        This method iterates over all input fields (e.g., Entry, Text, Combobox) 
        registered for the given table and resets their values to an empty string. 
        It is typically called after operations like add, update, or delete 
        to reset the form state for the next input.

        Parameters:
            table (str): The name of the table whose input fields should be cleared.

        """

        for col in self.entries[table]:
            self.binder.set_widget_value(self.entries[table][col], "")

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
    root.minsize(800, 600)
    root.mainloop()
