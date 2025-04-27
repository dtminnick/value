
from downloader import Downloader
from messenger import Messenger
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from tooltip import Tooltip
from database import Database
from tkcalendar import DateEntry
from widget_binder import WidgetBinder
import tkinter.font as tkfont


# import ttkbootstrap as tb
# from ttkbootstrap.constants import *

db = Database()

msg_handler = Messenger()

downloader = Downloader(msg_handler)

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

        binder = WidgetBinder(self.root)

        self.root.title("Value Measurement Database Application")

        self.root.geometry("1200x800")

        # ------------------------------------------
        # Create notebook for tabbed user interface.
        # ------------------------------------------

        self.notebook = ttk.Notebook(root)

        self.notebook.pack(expand = True, fill = "both")

        style = ttk.Style()

        style.configure('TNotebook.tab', width = 18, padding = [10, 10])

        # self.tables = ['initiative', 
        #                'event',
        #                'metric',
        #                'plan',
        #                'event_plan',
        #                'global_metric_value',
        #                'plan_metric_value',
        #                'user_query']
        
        # Store frames for each table, fields per table and treeview widgets per table.

        self.frames = {}

        self.entries = {}

        self.trees = {}

        # Create a tab and UI for each table.

        # for table in self.tables:
        #     frame = ttk.Frame(self.notebook)
        #     self.notebook.add(frame, text = table)
        #     self.frames[table] = frame
        #     self.create_table_ui(frame, table)

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

        metr_initiative_id_label = ttk.Label(metr_entry_frame,
                                  width = 20,
                                  text = "Initiative Id:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        self.metr_initiative_id_entry = ttk.Entry(metr_entry_frame)

        self.metr_initiative_id_entry.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

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

        evnt_initiative_id_entry = ttk.Entry(evnt_entry_frame)

        evnt_initiative_id_entry.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

        # Event title.

        evnt_event_title_label = ttk.Label(evnt_entry_frame,
                                  width = 20,
                                  text = "Event Title:"
                                  ).grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")

        evnt_event_title_entry = ttk.Entry(evnt_entry_frame)

        evnt_event_title_entry.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

        # Event description.

        evnt_event_description_label = ttk.Label(evnt_entry_frame,
                                  width = 20,
                                  text = "Description:"
                                  ).grid(row = 3, column = 0, padx = 5, pady = 2, sticky = "w")

        evnt_event_description_entry = ttk.Entry(evnt_entry_frame)

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

        # Bind entry frame.

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
            "initiative_id": evnt_initiative_id_entry,
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
        
        ep_plan_id_entry = ttk.Entry(ep_entry_frame, width = 20)

        ep_plan_id_entry.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        # Event id.

        ep_event_id_label = ttk.Label(ep_entry_frame,
                                  width = 20,
                                  text = "Event Id:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")

        ep_event_id_entry = ttk.Entry(ep_entry_frame)

        ep_event_id_entry.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

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
            "event_id": ep_event_id_entry,
            "plan_id": ep_plan_id_entry
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
        
        gmv_metric_id_entry = ttk.Entry(gmv_entry_frame, width = 20)

        gmv_metric_id_entry.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

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
            "metric_id": gmv_metric_id_entry,
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
        
        pmv_metric_id_entry = ttk.Entry(pmv_entry_frame, width = 20)

        pmv_metric_id_entry.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

        # Plan id.

        pmv_plan_id_label = ttk.Label(pmv_entry_frame,
                                  width = 20,
                                  text = "Plan Id:"
                                  ).grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")
        
        pmv_plan_id_entry = ttk.Entry(pmv_entry_frame, width = 20)

        pmv_plan_id_entry.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

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
            "metric_id": pmv_metric_id_entry,
            "plan_id": pmv_plan_id_entry,
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

        uq_entry_frame.pack(fill = "x", padx = 10, pady = 10)
        
        # Query id.

        uq_query_id_label = ttk.Label(uq_entry_frame,
                                  width = 20,
                                  text = "Query Id:"
                                  ).grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")
        
        uq_query_id_entry = ttk.Entry(uq_entry_frame, width = 20)

        uq_query_id_entry.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

        # Query title.

        uq_query_title_label = ttk.Label(uq_entry_frame,
                                  width = 20,
                                  text = "Query Title:"
                                  ).grid(row = 1, column = 0, padx = 5, pady = 2, sticky = "w")
        
        uq_query_title_entry = ttk.Entry(uq_entry_frame, width = 100)

        uq_query_title_entry.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "w")

        # Query description.

        uq_query_description_label = ttk.Label(uq_entry_frame,
                                  width = 20,
                                  text = "Query Description:"
                                  ).grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")
        
        uq_query_description_entry = ttk.Entry(uq_entry_frame, width = 100)

        uq_query_description_entry.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

        # Query purpose.

        uq_query_purpose_label = ttk.Label(uq_entry_frame,
                                  width = 20,
                                  text = "Query Purpose:"
                                  ).grid(row = 3, column = 0, padx = 5, pady = 2, sticky = "w")
        
        uq_query_purpose_entry = ttk.Entry(uq_entry_frame, width = 100)

        uq_query_purpose_entry.grid(row = 3, column = 1, padx = 5, pady = 2, sticky = "w")

        # Query string.

        uq_query_string_label = ttk.Label(uq_entry_frame,
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
        
        uq_query_string_entry = tk.Text(uq_entry_frame, height = 10, width = 100, wrap = "word", font = entry_font)

        uq_query_string_entry.grid(row = 4, column = 1, padx = 5, pady = 2, sticky = "w")

        # Set operation.

        uq_set_operation_var = tk.BooleanVar()

        uq_space1_label = ttk.Label(uq_entry_frame,
                                    width = 10,
                                    text = ""
                                    ).grid(row = 0, column = 3, padx = 5, pady = 2, sticky = "w")

        uq_set_operation_label = ttk.Label(uq_entry_frame,
                                    width = 20,
                                    text = "Set Operation:"
                                    ).grid(row = 0, column = 4, padx = 5, pady = 2, sticky = "w")

        uq_set_operation_check = ttk.Checkbutton(uq_entry_frame, variable=uq_set_operation_var)

        uq_set_operation_check.grid(row = 0, column = 5, padx = 5, pady = 2, sticky = "w")

        # Set membership.

        uq_set_membership_var = tk.BooleanVar()

        uq_space2_label = ttk.Label(uq_entry_frame,
                                    width = 10,
                                    text = ""
                                    ).grid(row = 1, column = 3, padx = 5, pady = 2, sticky = "w")

        uq_set_membership_label = ttk.Label(uq_entry_frame,
                                    width = 20,
                                    text = "Set Membership:"
                                    ).grid(row = 1, column = 4, padx = 5, pady = 2, sticky = "w")

        uq_set_membership_check = ttk.Checkbutton(uq_entry_frame, variable=uq_set_membership_var)

        uq_set_membership_check.grid(row = 1, column = 5, padx = 5, pady = 2, sticky = "w")

        # Set comparison.

        uq_set_comparison_var = tk.BooleanVar()

        uq_space3_label = ttk.Label(uq_entry_frame,
                                    width = 10,
                                    text = ""
                                    ).grid(row = 2, column = 3, padx = 5, pady = 2, sticky = "w")

        uq_set_comparison_label = ttk.Label(uq_entry_frame,
                                    width = 20,
                                    text = "Set Comparison:"
                                    ).grid(row = 2, column = 4, padx = 5, pady = 2, sticky = "w")

        uq_set_comparison_check = ttk.Checkbutton(uq_entry_frame, variable=uq_set_comparison_var)

        uq_set_comparison_check.grid(row = 2, column = 5, padx = 5, pady = 2, sticky = "w")

        # Subquery.

        uq_subquery_var = tk.BooleanVar()

        uq_space4_label = ttk.Label(uq_entry_frame,
                                    width = 10,
                                    text = ""
                                    ).grid(row = 3, column = 3, padx = 5, pady = 2, sticky = "w")

        uq_subquery_label = ttk.Label(uq_entry_frame,
                                    width = 20,
                                    text = "Subquery:"
                                    ).grid(row = 3, column = 4, padx = 5, pady = 2, sticky = "w")

        uq_subquery_check = ttk.Checkbutton(uq_entry_frame, variable=uq_subquery_var)

        uq_subquery_check.grid(row = 3, column = 5, padx = 5, pady = 2, sticky = "w")

        # CTE.

        uq_cte_var = tk.BooleanVar()

        uq_space5_label = ttk.Label(uq_entry_frame,
                                    width = 10,
                                    text = ""
                                    ).grid(row = 4, column = 3, padx = 5, pady = 2, sticky = "w")

        uq_cte_label = ttk.Label(uq_entry_frame,
                                    width = 20,
                                    text = "CTE:"
                                    ).grid(row = 4, column = 4, padx = 5, pady = 2, sticky = "w")

        uq_cte_check = ttk.Checkbutton(uq_entry_frame, variable=uq_cte_var)

        uq_cte_check.grid(row = 4, column = 5, padx = 5, pady = 2, sticky = "w")

        # Aggregate function.

        uq_aggregate_function_var = tk.BooleanVar()

        uq_space6_label = ttk.Label(uq_entry_frame,
                                    width = 10,
                                    text = ""
                                    ).grid(row = 5, column = 3, padx = 5, pady = 2, sticky = "w")

        uq_aggregate_function_label = ttk.Label(uq_entry_frame,
                                    width = 20,
                                    text = "Aggregate Function:"
                                    ).grid(row = 5, column = 4, padx = 5, pady = 2, sticky = "w")

        uq_aggregate_function_check = ttk.Checkbutton(uq_entry_frame, variable=uq_aggregate_function_var)

        uq_aggregate_function_check.grid(row = 5, column = 5, padx = 5, pady = 2, sticky = "w")

        # window function.

        uq_window_function_var = tk.BooleanVar()

        uq_space7_label = ttk.Label(uq_entry_frame,
                                    width = 10,
                                    text = ""
                                    ).grid(row = 6, column = 3, padx = 5, pady = 2, sticky = "w")

        uq_window_function_label = ttk.Label(uq_entry_frame,
                                    width = 20,
                                    text = "Window Function:"
                                    ).grid(row = 6, column = 4, padx = 5, pady = 2, sticky = "w")

        uq_window_function_check = ttk.Checkbutton(uq_entry_frame, variable=uq_window_function_var)

        uq_window_function_check.grid(row = 6, column = 5, padx = 5, pady = 2, sticky = "w")

        # OLAP.

        uq_olap_var = tk.BooleanVar()

        uq_space8_label = ttk.Label(uq_entry_frame,
                                    width = 10,
                                    text = ""
                                    ).grid(row = 7, column = 3, padx = 5, pady = 2, sticky = "w")

        uq_olap_label = ttk.Label(uq_entry_frame,
                                    width = 20,
                                    text = "OLAP:"
                                    ).grid(row = 7, column = 4, padx = 5, pady = 2, sticky = "w")

        uq_olap_check = ttk.Checkbutton(uq_entry_frame, variable=uq_olap_var)

        uq_olap_check.grid(row = 7, column = 5, padx = 5, pady = 2, sticky = "w")

        # Create button frame and widgets.

        uq_button_frame = ttk.Frame(uq_frame)

        uq_add_btn = ttk.Button(uq_button_frame,
                                        command = lambda: self.add_record("user_query"),
                                        text = "Add")
        
        uq_add_btn.grid(row = 0, column = 0, padx = 5)

        uq_update_btn = ttk.Button(uq_button_frame,
                                           command = lambda: self.update_record("user_query"),
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
            "query_string": uq_query_string_entry,
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

        form_frame.pack(fill = "x", padx = 20, pady = 20)

        for i, col in enumerate(columns):
            ttk.Label(form_frame, text = f"{col}:").grid(row = i, column = 0, padx = 5, pady = 5, sticky = "w")

            if table_name == "user_query" and i == len(columns) - 1:

                # Use a text widget for the last field, i.e. query_string.

                entry = tk.Text(form_frame, height = 10, width = 100, wrap = "word", font = ("TkDefaultFont", 10))

                entry.grid(row = i, column = 1, padx = 5, pady = 5, sticky = "w")

                # Add vertical scrollbar to Text widget.

                scrollbar = ttk.Scrollbar(form_frame, orient = "vertical", command = entry.yview)

                scrollbar.grid(row = i, column = 2, sticky = "ns", padx = 5, pady = 5)

                # Link the Text widget with the scrollbar.

                entry.configure(yscrollcommand = scrollbar.set)

            else:

                entry = ttk.Entry(form_frame, width = 100)

                entry.grid(row = i, column = 1, padx = 5, pady = 5, sticky = "ew")

            self.entries[table_name][col] = entry

        # Add CRUD buttons.

        button_frame = ttk.Frame(frame)

        button_frame.pack(fill = "x", padx = 20, pady = 20)

        add_btn = ttk.Button(button_frame, 
                   text = "Add Record", 
                   command = lambda t = table_name: self.add_record(t))
        
        add_btn.grid(row = 0, column = 0, padx = 10)

        update_btn = ttk.Button(button_frame, 
                   text = "Update Record", 
                command = lambda t = table_name: self.update_record(t))
        
        update_btn.grid(row = 0, column = 1, padx = 10)

        delete_btn = ttk.Button(button_frame, 
                   text = "Delete Record", 
                   command = lambda t = table_name: self.delete_record(t))
        
        delete_btn.grid(row = 0, column = 2, padx = 10)

        refresh_btn = ttk.Button(button_frame, 
                   text = "Refresh Records", 
                   command = lambda t = table_name: self.refresh_records(t))
        
        refresh_btn.grid(row = 0, column = 3, padx = 10)

        # Add tooltips.

        Tooltip(add_btn, widget_id = "add_btn")

        Tooltip(update_btn, widget_id = "update_btn")

        Tooltip(delete_btn, widget_id = "delete_btn")
        
        Tooltip(refresh_btn, widget_id = "refresh_btn")

        # Add data display to see the data in tables.

        tree_frame = ttk.Frame(frame)

        tree_frame.pack(fill = "both", expand = True, padx = 20, pady = 20)

        Tooltip(tree_frame, widget_id = "tree_frame")

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

            # if table in self.hidden_ids:
            #     for id_field, widget in self.hidden_ids[table].items():
            #         data[id_field] = widget.get() or None

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
        Retrieves the value from a Tkinter input widget, handling each widget type appropriately.

        - For `tk.Entry` widgets (single-line input), returns the text content.
        - For `tk.Text` widgets (multi-line input), retrieves the text from the start to the end, excluding the trailing newline.
        - For `ttk.Combobox` widgets, retrieves the corresponding ID based on the selected title.

        Parameters
        ----------
        widget : tk.Widget
            The Tkinter input widget (either `tk.Entry`, `tk.Text`, or `ttk.Combobox`) from which the value is retrieved.

        Returns
        -------
        str or None
            The cleaned text content from the widget, or the corresponding ID for a combobox.
        """
        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c").strip()

        elif isinstance(widget, ttk.Combobox):
            selected_title = widget.get().strip()  # Get the selected title from the combobox
            combo_maps = self.combo_value_maps.get(widget)
            if combo_maps:
                title_to_id = combo_maps.get("title_to_id")
                if title_to_id:
                    # Return the corresponding ID for the selected title
                    return title_to_id.get(selected_title, None)
            return selected_title  # Return title if no mapping exists

        elif isinstance(widget, ttk.Checkbutton):
            var_name = widget.cget("variable")
            if var_name:
                return bool(self.root.getvar(var_name))

        elif hasattr(widget, "get"):
            return widget.get().strip()

        return None

    def set_widget_value(self, widget, value):
        """
        Sets the given value into a Tkinter input widget, handling each widget type appropriately.

        - For `tk.Entry` widgets (single-line input), sets the provided value as the widget's text.
        - For `tk.Text` widgets (multi-line input), clears the existing text and inserts the new value.
        - For `ttk.Combobox` widgets, sets the display value based on a mapping from ID to title.

        Parameters
        ----------
        widget : tk.Widget
            The Tkinter input widget (either `tk.Entry`, `tk.Text`, or `ttk.Combobox`) to which the value will be set.

        value : str or int
            The value to be inserted into the widget. For `ttk.Combobox`, this is the ID (which will be mapped to the title).

        Returns
        -------
        None
        """
        if isinstance(widget, (tk.Entry, ttk.Entry)):
            self._set_entry_value(widget, value)
        elif isinstance(widget, ttk.Combobox):
            self._set_combobox_value(widget, value)
        elif isinstance(widget, ttk.Checkbutton):
            self._set_checkbutton_value(widget, value)
        elif isinstance(widget, tk.Text):
            self._set_text_value(widget, value)
        elif hasattr(widget, "delete") and hasattr(widget, "insert"):
            self._set_generic_value(widget, value)
        else:
            print(f"Unsupported widget type: {type(widget)}")


    def _set_entry_value(self, widget, value):
        """Set value for Entry widgets."""
        widget.delete(0, tk.END)
        widget.insert(0, value)


    def _set_combobox_value(self, widget, value):
        """Set value for Combobox widgets."""
        combo_maps = self.combo_value_maps.get(widget)
        if combo_maps:
            id_to_title = combo_maps.get("id_to_title")
            if id_to_title:
                # Convert ID to the corresponding title and set it in the combobox
                display_value = id_to_title.get(value, "")
                widget.set(display_value)
            else:
                # If no mapping exists, just set the value directly (fallback)
                widget.set(value)
        else:
            # If no mapping, directly set the value (fallback)
            widget.set(value)


    def _set_checkbutton_value(self, widget, value):
        """Set value for Checkbutton widgets."""
        var_name = widget.cget("variable")
        if var_name:
            try:
                self.root.setvar(var_name, bool(value))
            except Exception as e:
                print(f"Error setting checkbutton variable: {e}")


    def _set_text_value(self, widget, value):
        """Set value for Text widgets."""
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, value)


    def _set_generic_value(self, widget, value):
        """Set value for generic widgets with delete and insert methods."""
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

    def register_combobox(self, widget, id_to_title_map):
        """
        Register a combobox with ID-to-title and title-to-ID mappings.

        Parameters
        ----------
        widget : ttk.Combobox
            The combobox widget to register.

        id_to_title_map : dict
            Dictionary mapping from ID to title.
        """
        title_to_id = {v: k for k, v in id_to_title_map.items()}

        # Save both directions for later use
        self.combo_value_maps[widget] = {
            "id_to_title": id_to_title_map,
            "title_to_id": title_to_id
        }

        # Update the combobox values
        widget['values'] = list(title_to_id.keys())


    def update_combobox_from_treeview(self, widget, selected_id):
        """
        Update the combobox based on a selected ID
        """
        combo_maps = self.combo_value_maps.get(widget)
        if combo_maps:
            id_to_title = combo_maps.get("id_to_title")
            if id_to_title:
                # Set the combobox to display the corresponding title
                title = id_to_title.get(selected_id, "")
                widget.set(title)

    def setup_widgets(self):
        """
        Set up widgets for different tables.
        Example: for 'metric' and 'initiative' tables, each may have multiple comboboxes.
        """
        # For example, set up comboboxes for the 'metric' and 'initiative' tables
        self.setup_combobox_for_table("metric", ["metric_column_1", "metric_column_2"])
        self.setup_combobox_for_table("initiative", ["initiative_column_1", "initiative_column_2"])

    def setup_combobox_for_table(self, table_name, columns):
        """
        Set up multiple comboboxes for a specific table, bind them to hidden entries, and add widgets to the layout.
        Each combobox corresponds to a specific column.
        """
        for column in columns:
            # Fetch rows for each column (e.g., 'metric_column_1', 'metric_column_2')
            rows = db.execute_query(f"SELECT {table_name}_id, {column} FROM {table_name}")

            # Create combobox and hidden entry widget
            combobox = ttk.Combobox(self.root, values=[row[1] for row in rows])  # Titles for the combobox
            entry = tk.Entry(self.root)  # Hidden entry widget to store the selected ID

            # Store widgets in dictionaries for future reference
            combobox_key = f"{table_name}_{column}_combobox"
            entry_key = f"{table_name}_{column}_entry"
            self.comboboxes[combobox_key] = combobox
            self.entries[entry_key] = entry

            # Bind the combobox to the hidden entry (use helper function)
            # bind_combobox_to_entry(combobox, entry, rows, id_key=f"{table_name}_id", title_key=column)

            # Add the combobox and entry widgets to the UI layout
            combobox.grid(row=columns.index(column), column=0)
            entry.grid(row=columns.index(column), column=1)

    def bind_comboboxes_for_table(self, table, combo_entry_map):
        """
        Bind comboboxes and entry widgets for each table dynamically.
        
        - `table`: The name of the table (e.g., 'initiative').
        - `combo_entry_map`: A dictionary mapping comboboxes to entry widgets for each field in the table.
        """
        try:
            # Fetch rows from the database based on the table
            query = f"SELECT * FROM {table}"
            rows = db.execute_query(query)
            
            for combo, entry in combo_entry_map.items():
                # Assuming each combobox and entry pair corresponds to one field in the table
                # For example, initiative_id and initiative_title in the 'initiative' table
                
                # Here, `combo` is the combobox and `entry` is the hidden entry widget
                if combo and entry:
                    # Bind the combobox to the entry widget with the correct title-to-id mapping
                    id_key = f"{table}_id"  # Assume the ID field in the table is the table name followed by '_id'
                    title_key = f"{table}_title"  # Assume the title field follows a similar convention
                    
                    self.combo_binder.bind(combo, entry, rows, id_key=id_key, title_key=title_key)
        except Exception as e:
            messagebox.showerror("Error", f"Error binding comboboxes for {table}: {e}")



if __name__ == "__main__":
    # root = tb.Window(themename = "value")
    root = tk.Tk()
    app = App(root)
    root.minsize(800, 600)
    root.mainloop()

