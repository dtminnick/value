import csv
from datetime import datetime
from messenger import Messenger
from tkinter import filedialog

msg_handler = Messenger()

class Downloader:

    """
    A utility class that handles the downloading of query results to a csv file.

    This class provides functionality to export a list of dictionaries
    (query results) to a csv file using a standard file dialog.  It 
    supports dynamic file naming based on the selected query title
    and current date and uses a message handler for user notifications.

    Parameters
    ----------
    msg_handler : object
        An object responsible for displaying messages to the user.
        Must have methods 'show_warning', 'show_info' and 'show_error' that
        accept (title, message).

    Methods
    -------
    download(query_result, query_title)
        Prompts the user to save the query result as a csv file.

    """

    def __init__(self, msg_handler):

        """
        Initialize the downloader with a message handler.

        Parameters
        ----------
        msg_handler : object
            Message handler with 'show_warning', 'show_info' and 'show_error' methods.

        """

        self.msg_handler = msg_handler

    def download(self, query_result, query_title):

        """
        Download the given query result to a csv file.

        Parameters
        ----------
        query_result : list of dict
            The data to be saved, where each dictionary represents a row of the query result.

        query_title : str
            The title of the query, used to generate the default file name.

        Returns
        -------
        None

        """

        if not query_result:

            self.msg_handler.show_warning("Error", "No query result to download.")

            return
        
        title = query_title.strip().replace(" ", "_")

        date_str = datetime.now().strftime("%Y-%m-%d")

        default_file_name = f"{title}_{date_str}.csv"

        file_path = filedialog.asksaveasfilename(
            defaultextension = ".csv",
            filetypes = [("CSV files", "*.csv")],
            initialfile = default_file_name,
            title = "Save Query Result as..."
        )

        if not file_path:

            self.msg_handler.show_warning("Download Error", "No file path specified for download.")

            return
        
        try:

            with open(file_path, "w", newline = "", encoding = "utf-8") as csv_file:

                writer = csv.DictWriter(csv_file, fieldnames = query_result[0].keys())

                writer.writeheader()

                writer.writerows(query_result)

                self.msg_handler.show_info("Result Saved", f"Result saved to: \n\n {file_path}")

        except Exception as e:

            self.msg_handler.show_error("Download Error", f"Error saving file: \n\n {e}")
            