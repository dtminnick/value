
import logging
import tkinter.messagebox as mb

class Messenger:

    """
    A utility class for displaying messages and logging output in a Tkinter application.

    Provides methods to show errors, warnings, and info dialogs using tkinter's messagebox,
    with optional logging and debug printing.

    Attributes
    ----------
    debug : bool
        If True, messages are printed to the console for debugging purposes.

    """

    def __init__(self, debug = False, log_file = None):

        """
        Initialize the Messenger.

        Parameters
        ----------
        debug : bool, optional
            Enable console debug output if True (default is False).

        log_file : str or None, optional
            If provided, enables logging to the specified file (default is None).

        """
        self.debug = debug

        if log_file:

            # Set up logging to a file, if specified

            logging.basicConfig(filename = log_file, level = logging.DEBUG)

    def show_error(self, title, message):

        """
        Display an error dialog and log the message.

        Parameters
        ----------
        title : str
            The title of the error dialog.

        message : str
            The error message to display.

        """
        mb.showerror(title, message)

        if self.debug:

            print(f"[Error] {title}: {message}")

        logging.error(f"{title}: {message}")

    def show_warning(self, title, message):

        """
        Display a warning dialog and log the message.

        Parameters
        ----------
        title : str
            The title of the warning dialog.

        message : str
            The warning message to display.

        """
        mb.showwarning(title, message)

        if self.debug:

            print(f"[Warning] {title}: {message}")

        logging.warning(f"{title}: {message}")

    def show_info(self, title, message):

        """
        Display an informational dialog and log the message.

        Parameters
        ----------
        title : str
            The title of the info dialog.

        message : str
            The informational message to display.

        """

        mb.showinfo(title, message)

        if self.debug:

            print(f"[Info] {title}: {message}")

        logging.info(f"{title}: {message}")

    def confirm_action(self, title, message):

        """
        Display a Yes/No confirmation dialog.

        Parameters
        ----------
        title : str
            The title of the confirmation dialog.

        message : str
            The confirmation prompt.

        Returns
        -------
        bool
            True if the user clicks 'Yes', False otherwise.

        """

        return mb.askyesno(title, message)

    def log_debug(self, message):

        """
        Log a debug message, with optional console output.

        Parameters
        ----------
        message : str
            The debug message to log.
            
        """

        if self.debug:
            
            print(f"[Debug] {message}")

        logging.debug(message)
