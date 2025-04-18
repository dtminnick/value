
import unittest
from unittest.mock import Mock, patch, mock_open
from downloader import Downloader

class TestDownloader(unittest.TestCase):
    def setUp(self):
        # Create a mock Messenger with expected methods
        self.mock_msg_handler = Mock()
        self.mock_msg_handler.show_warning = Mock()
        self.mock_msg_handler.show_info = Mock()
        self.mock_msg_handler.show_error = Mock()
        self.downloader = Downloader(self.mock_msg_handler)

    @patch("downloader.filedialog.asksaveasfilename")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_successful(self, mock_file_open, mock_asksaveasfilename):
        # Arrange
        query_result = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        mock_asksaveasfilename.return_value = "test_output.csv"

        # Act
        self.downloader.download(query_result, "Test Query")

        # Assert
        mock_file_open.assert_called_once_with("test_output.csv", "w", newline="", encoding="utf-8")
        self.mock_msg_handler.show_info.assert_called_once()
        self.mock_msg_handler.show_warning.assert_not_called()
        self.mock_msg_handler.show_error.assert_not_called()

    def test_download_empty_query(self):
        # Act
        self.downloader.download([], "Empty Query")

        # Assert
        self.mock_msg_handler.show_warning.assert_called_once_with("Error", "No query result to download.")
        self.mock_msg_handler.show_info.assert_not_called()
        self.mock_msg_handler.show_error.assert_not_called()

    @patch("downloader.filedialog.asksaveasfilename", return_value="")
    def test_download_no_file_path_selected(self, mock_asksaveasfilename):
        # Act
        self.downloader.download([{"id": 1}], "Query With No File")

        # Assert
        self.mock_msg_handler.show_warning.assert_called_once_with("Error", "No file path specified for download.")

    @patch("downloader.filedialog.asksaveasfilename", return_value="test_error.csv")
    @patch("builtins.open", side_effect=IOError("Disk error"))
    def test_download_file_write_error(self, mock_file_open, mock_asksaveasfilename):
        # Act
        self.downloader.download([{"id": 1}], "Error Query")

        # Assert
        self.mock_msg_handler.show_error.assert_called_once()
        self.mock_msg_handler.show_info.assert_not_called()

if __name__ == "__main__":
    unittest.main()
