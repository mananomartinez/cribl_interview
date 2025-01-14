import unittest
from unittest.mock import patch, mock_open, MagicMock

from parser import read_single_file, read_n_log_entries

class TestParseLogs(unittest.TestCase):

    @patch('os.environ.get')
    @patch('builtins.open', new_callable=MagicMock)
    def test_read_file(self, mock_open, mock_environ):
        file_name = 'file.log'
        mock_environ = "/var/log"
        file_content = b'This is a log line.\nAnother log line.\nFinal log line.\n'
        current_position = len(file_content)

        mock_file_handle = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file_handle

        def read_side_effect(size=-1):
            nonlocal current_position
            if size == -1:
                size = len(file_content) - current_position
            end_position = current_position + size
            chunk = file_content[current_position:end_position]
            current_position = end_position
            return chunk

        def seek_side_effect(pos, whence=0):
            nonlocal current_position
            if whence == 0:
                current_position = pos
            elif whence == 1:
                current_position += pos
            elif whence == 2:
                current_position = len(file_content) + pos
            return current_position

        mock_file_handle.read = MagicMock(side_effect=read_side_effect)
        mock_file_handle.seek = MagicMock(side_effect=seek_side_effect)
        mock_file_handle.tell = MagicMock(side_effect=lambda: current_position)

        result = {}        
        read_single_file(file_name, result)

        expected = {f"{file_name}": ['Final log line.', 'Another log line.', 'This is a log line.']}
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=MagicMock)
    def test_read_n_entries(self, mock_open):
        file_name = 'file.log'
        file_content = b'This is a log line.\nAnother log line.\nFinal log line.\n'
        
        current_position = len(file_content)
        mock_file_handle = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file_handle

        def read_side_effect(size=-1):
            nonlocal current_position
            if size == -1:
                size = len(file_content) - current_position
            end_position = current_position + size
            chunk = file_content[current_position:end_position]
            current_position = end_position
            return chunk

        def seek_side_effect(pos, whence=0):
            nonlocal current_position
            if whence == 0:
                current_position = pos
            elif whence == 1:
                current_position += pos
            elif whence == 2:
                current_position = len(file_content) + pos
            return current_position

        mock_file_handle.read = MagicMock(side_effect=read_side_effect)
        mock_file_handle.seek = MagicMock(side_effect=seek_side_effect)
        mock_file_handle.tell = MagicMock(side_effect=lambda: current_position)

        n_entries = 1
        result = read_n_log_entries(file_name, n_entries)

        expected = ['Final log line.']
        self.assertEqual(result, expected)


    @patch('os.environ.get')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_empty_log_file(self, mock_open_fn, mock_environ):
        
        # Mock the return values
        mock_environ.return_value = '/var/log'
        mock_file_handle = mock_open_fn.return_value
        mock_file_handle.seek = MagicMock()
        mock_file_handle.tell = MagicMock(return_value=len(b''))

        result = {}        
        read_single_file("/var/log/empty_log.txt", result)

        # Assertions
        mock_open_fn.assert_called()
        self.assertEqual(len(result), 1)
        self.assertEqual(result["ERROR"], "There were no entries in /var/log/empty_log.txt.")