
import tkinter as tk
from messenger import Messenger
from database import Database

class Tooltip:

    """
    A utility class to create and manage tooltips for Tkinter widgets, 
    fetching the tooltip text from a MySQL database.

    Attributes
    ----------
    widget : tk.Widget
        The widget to attach the tooltip to.

    widget_id : str
        The unique identifier of the widget; used to fetch the tooltip from the database.

    db : Database
        The database connection instance used to fetch the tooltip text.

    text : str
        The tooltip text retrieved from the database.

    tooltip : tk.Toplevel
        The toplevel window that displays the tooltip.

    """

    def __init__(self, widget, widget_id):
        
        """
        Initializes the Tooltip object.

        Parameters
        ----------
        widget : tk.Widget
            The widget to attach the tooltip to.

        widget_id : str
            The unique identifier of the widget.

        msg_handler : object
            Message handler with 'show_warning', 'show_info' and 'show_error' methods.

        """

        self.widget = widget

        self.widget_id = widget_id

        self.db = Database()

        self.tooltip = None

        # Fetch tooltip text from the database.

        self.text = self.get_tooltip_from_db()

        # Bind events to show and hide the tooltip.

        self.widget.bind("<Enter>", self.show_tooltip)

        self.widget.bind("<Leave>", self.hide_tooltip)

    def get_tooltip_from_db(self):

        """
        Fetch the tooltip text for the given widget id from the database.

        Returns
        -------
        str
            The tooltip text for the widget or a default message if not found.
        
        """

        try:
            result = self.db.fetch_all("tooltip")
            for row in result:
                if row['widget_id'] == self.widget_id:
                    return row['tooltip_text']
                
            # Return default message if no tooltip is found.

            return "No tooltip available."
        
        except Exception as e:
            raise Exception("Error", f"Error retrieving tooltip: {e}")

    def show_tooltip(self, event):

        """
        Create and display the tooltip when the mouse enters the widget.

        Parameters
        ----------
        event : tk.Event
            The event triggered when the mouse enters the widget.
        
        """
        try: 
            self.tooltip = tk.Toplevel(self.widget)

            self.tooltip.wm_overrideredirect(True)

            self.tooltip.wm_geometry(f"+{self.widget.winfo_rootx() + 20}+{self.widget.winfo_rooty() + 20}")

            label = tk.Label(self.tooltip, text = self.text, background = "lightyellow", relief = "solid", borderwidth = 1)

            label.pack()

        except Exception as e:
            raise Exception("Error", f"Error generating tooltip: {e}")

    def hide_tooltip(self, event):

        """
        Destroy the tooltip when the mouse leaves the widget.

        Parameters
        ----------
        event : tk.Event
            The event triggered when the mouse enters the widget.
        
        """
        try:
            if self.tooltip:
                self.tooltip.destroy()
                self.tooltip = None

        except Exception as e:
            raise Exception("Error", f"Error gdestroying tooltip: {e}")
