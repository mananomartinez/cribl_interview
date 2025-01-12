import unittest
from unittest.mock import patch, mock_open

from parser import read_log_file, read_all_log_files

class TestParseLogs(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='mocked log line')
    def test_read_file(self, mock_file):
        
        result = read_log_file('path/to/log_file.log')
        
        #Assertions
        mock_file.assert_called_once_with('path/to/log_file.log', 'r')
        self.assertEqual(result, ['mocked log line'])

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_read_empty_file(self, mock_file):
        
        result = read_log_file('path/to/log_file.log')
        
        #Assertions
        mock_file.assert_called_once_with('path/to/log_file.log', 'r')
        self.assertEqual(result, [])


    @patch('os.environ.get')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_read_all_log_files_success(self, mock_open_fn, mock_os_walk, mock_environ):
        
        # Mock the return values
        mock_environ.return_value = '/mock/log/directory'
        mock_os_walk.return_value = [('/mock/log/directory', [], ['log1.txt', 'log2.txt'])]
        mock_open_fn.return_value.read.return_value = '[{"log": "entry1"}]'
        
        # Run the function
        result = read_all_log_files()

        # Assertions
        self.assertEqual(len(result), 2)
        self.assertIn('/mock/log/directory/log1.txt', result)
        self.assertIn('/mock/log/directory/log2.txt', result)
        self.assertEqual(result['/mock/log/directory/log1.txt'], '[{"log": "entry1"}]')
        self.assertEqual(result['/mock/log/directory/log2.txt'], '[{"log": "entry1"}]')

        
    @patch('os.environ.get')
    @patch('os.walk')
    @patch('parser.parse_logs.read_log_file', return_value = [{"log": "entry1"}])
    def test_read_all_log_files_success(self, mock_read_log_file, mock_os_walk, mock_environ):

        # Mock the return values
        mock_environ.return_value = '/mock/log/directory'
        mock_os_walk.return_value = [
            ('/mock/log/directory', [], ['log1.txt', 'log2.txt']),
        ]

        result = read_all_log_files()

        # Assertions
        mock_read_log_file.assert_called()
        self.assertEqual(len(result), 2)
        self.assertIn('/mock/log/directory/log1.txt', result)
        self.assertIn('/mock/log/directory/log2.txt', result)
        self.assertEqual(result['/mock/log/directory/log1.txt'], '[{"log": "entry1"}]')
        self.assertEqual(result['/mock/log/directory/log2.txt'], '[{"log": "entry1"}]')


    @patch('os.environ.get')
    @patch('os.walk')
    @patch('parser.parse_logs.read_log_file', return_value = [])
    def test_empty_log_file(self, mock_read_log_file, mock_os_walk, mock_environ):
        
        # Mock the return values
        mock_environ.return_value = '/mock/log/directory'
        mock_os_walk.return_value = [
            ('/mock/log/directory', [], ['empty_log.txt']),
        ]

        result = read_all_log_files()

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertIn('/mock/log/directory/empty_log.txt', result)
        self.assertEqual(result['/mock/log/directory/empty_log.txt'], 'File is empty.')

    @patch('os.environ.get')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_with_invalid_json(self, mock_open_fn, mock_os_walk, mock_environ):

        # Mock the return values
        mock_environ.return_value = '/mock/log/directory'
        mock_os_walk.return_value = [
            ('/mock/log/directory', [], ['invalid_json_log.txt']),
        ]
        mock_open_fn.return_value.read.return_value = '{ log: "entry1" '  # Invalid JSON

        result = read_all_log_files()

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertIn('/mock/log/directory/invalid_json_log.txt', result)
        self.assertEqual(result['/mock/log/directory/invalid_json_log.txt'], 'File is empty.')
