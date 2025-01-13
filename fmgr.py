import os
import shutil
import unittest
from unittest.mock import patch, MagicMock

class FileSelector:
    def __init__(self):
        self.selected_files = []
        self.current_directory_contents = []

    def load_directory_contents(self, directory_path):
        """Load the contents of a directory"""
        try:
            self.current_directory_contents = os.listdir(directory_path)
            return self.current_directory_contents
        except Exception as e:
            print(f"Error loading directory contents: {e}")
            return []

    def select_files_by_indices(self, indices, directory_path):
        """Select files based on indices"""
        try:
            selected_indices = [int(i.strip()) for i in indices.split(',')]
            self.selected_files.clear()
            for index in selected_indices:
                if 0 <= index < len(self.current_directory_contents):
                    full_path = os.path.join(directory_path, self.current_directory_contents[index])
                    self.selected_files.append(full_path)
            return self.selected_files
        except ValueError:
            print("Invalid input. Please enter valid indices.")
            return []
        except Exception as e:
            print(f"Error selecting files: {e}")
            return []

    def get_selected_files(self):
        """Return the list of currently selected files"""
        return self.selected_files

    def clear_selection(self):
        """Clear the current file selection"""
        self.selected_files.clear()

class FileManager:
    def __init__(self):
        self.current_path = os.path.expanduser('~')
        self.file_selector = FileSelector()

    def display_directory_contents(self):
        """Display contents of the current directory"""
        try:
            contents = self.file_selector.load_directory_contents(self.current_path)
            return contents
        except Exception as e:
            print(f"Error: {e}")
            return []

    def navigate(self, index):
        """Navigate to a subdirectory"""
        try:
            contents = os.listdir(self.current_path)
            selected_element = contents[index]
            full_path = os.path.join(self.current_path, selected_element)
            if os.path.isdir(full_path):
                self.current_path = full_path
                return full_path
            else:
                print(f"Cannot open file {selected_element}")
                return None
        except Exception as e:
            print(f"Navigation error: {e}")
            return None

    def go_to_parent_directory(self):
        """Move to the parent directory"""
        self.current_path = os.path.dirname(self.current_path)
        return self.current_path

    def copy_files(self, destination):
        """Copy selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if os.path.exists(file):
                    shutil.copy2(file, destination)
            self.file_selector.clear_selection()
            return len(selected_files)
        except Exception as e:
            print(f"Copy error: {e}")
            return 0

    def move_files(self, destination):
        """Move selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if os.path.exists(file):
                    shutil.move(file, destination)
            self.file_selector.clear_selection()
            return len(selected_files)
        except Exception as e:
            print(f"Move error: {e}")
            return 0

    def delete_files(self):
        """Delete selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if os.path.isfile(file):
                    os.remove(file)
                elif os.path.isdir(file):
                    shutil.rmtree(file)
            self.file_selector.clear_selection()
            return len(selected_files)
        except Exception as e:
            print(f"Delete error: {e}")
            return 0

class TestFileManager(unittest.TestCase):
    @patch('os.listdir')
    def test_display_directory_contents(self, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'folder1']
        file_manager = FileManager()
        contents = file_manager.display_directory_contents()
        self.assertEqual(contents, ['file1.txt', 'file2.txt', 'folder1'])

    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_navigate(self, mock_isdir, mock_listdir):
        mock_listdir.return_value = ['folder1']
        mock_isdir.return_value = True
        file_manager = FileManager()
        new_path = file_manager.navigate(0)
        self.assertIn('folder1', new_path)

    def test_go_to_parent_directory(self):
        file_manager = FileManager()
        initial_path = file_manager.current_path
        parent_path = file_manager.go_to_parent_directory()
        self.assertEqual(parent_path, os.path.dirname(initial_path))

    @patch('shutil.copy2')
    @patch('os.path.exists')
    def test_copy_files(self, mock_exists, mock_copy):
        mock_exists.return_value = True
        file_manager = FileManager()
        file_manager.file_selector.selected_files = ['/path/to/file1.txt']
        count = file_manager.copy_files('/destination')
        self.assertEqual(count, 1)
        mock_copy.assert_called_once()

    @patch('shutil.move')
    @patch('os.path.exists')
    def test_move_files(self, mock_exists, mock_move):
        mock_exists.return_value = True
        file_manager = FileManager()
        file_manager.file_selector.selected_files = ['/path/to/file1.txt']
        
        count = file_manager.move_files('/destination') 
        
        self.assertEqual(count, 1)
        mock_move.assert_called_once_with('/path/to/file1.txt', '/destination')  
        
    @patch('os.remove')
    @patch('os.path.isfile')
    def test_delete_files(self, mock_isfile, mock_remove):
        mock_isfile.return_value = True
        file_manager = FileManager()
        file_manager.file_selector.selected_files = ['/path/to/file1.txt']
        count = file_manager.delete_files()
        self.assertEqual(count, 1)
        mock_remove.assert_called_once()

if __name__ == '__main__':
    unittest.main()
