import unittest
from unittest.mock import patch, mock_open

from parser import read_log_file, read_all_log_files

class TestParseLogs(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='mocked log line')
    def test_read_file(self, mock_file):
        all_log_entries = {}
        read_log_file('/mock/log/log_file.log', all_log_entries)
        
        #Assertions
        mock_file.assert_called_once_with('/mock/log/log_file.log', 'r')
        self.assertEqual(all_log_entries['/mock/log/log_file.log'], ['mocked log line'])

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_read_empty_file(self, mock_file):

        all_log_entries = {}
        read_log_file('/mock/log/log_file.log', all_log_entries)
        
        #Assertions
        mock_file.assert_called_once_with('/mock/log/log_file.log', 'r')
        self.assertEqual(all_log_entries, {})

    @patch('os.environ.get')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"log": "entry1"}]')
    def test_read_all_log_files_success(self, mock_open_fn, mock_os_walk, mock_environ):
        
        # Mock the return values
        mock_environ.return_value = '/mock/log/directory'
        mock_os_walk.return_value = [
            ('/mock/log/directory', [], ['log1.txt', 'log2.txt']),
        ]
        
        # Run the function
        result = read_all_log_files()

        # Assertions
        self.assertEqual(len(result), 2)
        self.assertIn('/mock/log/directory/log1.txt', result)
        self.assertIn('/mock/log/directory/log2.txt', result)
        self.assertEqual(result['/mock/log/directory/log1.txt'], ['[{"log": "entry1"}]'])
        self.assertEqual(result['/mock/log/directory/log2.txt'], ['[{"log": "entry1"}]'])

    @patch('os.environ.get')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_empty_log_file(self, mock_open_fn, mock_os_walk, mock_environ):
        
        # Mock the return values
        mock_environ.return_value = '/mock/log/directory'
        mock_os_walk.return_value = [
            ('/mock/log/directory', [], ['empty_log.txt']),
        ]

        result = read_all_log_files()

        # Assertions
        mock_open_fn.assert_called()
        self.assertEqual(len(result), 0)
        self.assertNotIn('/mock/log/directory/empty_log.txt', result)
