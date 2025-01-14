import unittest
from unittest.mock import MagicMock
from typing import List

from futils import FileManager, FileSystem, FileSelection, UserInterface

class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.file_selection = MagicMock(spec=FileSelection)
        self.file_system = MagicMock(spec=FileSystem)
        self.user_interface = MagicMock(spec=UserInterface)
        
        self.file_manager = FileManager(self.file_selection, self.file_system, self.user_interface)

    def test_copy_files(self):
        self.file_selection.get_and_reset.return_value = ["/path/to/file1.txt", "/path/to/file2.txt"]
        destination = "/path/to/destination"

        result = self.file_manager.copy_files(destination)

        self.assertEqual(result, 2)
        self.file_system.copy.assert_any_call("/path/to/file1.txt", destination)
        self.file_system.copy.assert_any_call("/path/to/file2.txt", destination)
        self.file_selection.get_and_reset.assert_called_once()

    def test_move_files(self):
        self.file_selection.get_and_reset.return_value = ["/path/to/file1.txt", "/path/to/file2.txt"]
        destination = "/path/to/destination"

        result = self.file_manager.move_files(destination)

        self.assertEqual(result, 2)
        self.file_system.move.assert_any_call("/path/to/file1.txt", destination)
        self.file_system.move.assert_any_call("/path/to/file2.txt", destination)
        self.file_selection.get_and_reset.assert_called_once()

    def test_delete_files(self):
        self.file_selection.get_and_reset.return_value = ["/path/to/file1.txt", "/path/to/file2.txt"]

        result = self.file_manager.delete_files()

        self.assertEqual(result, 2)
        self.file_system.delete.assert_any_call("/path/to/file1.txt")
        self.file_system.delete.assert_any_call("/path/to/file2.txt")
        self.file_selection.get_and_reset.assert_called_once()

if __name__ == "__main__":
    unittest.main()
