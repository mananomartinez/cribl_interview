import unittest
from unittest.mock import patch, mock_open
from src.parser.search_logs import search_in_file, search_directory

class TestSearchLogs(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='This is a test line with keyword\nAnother line without')
    def test_search_in_file_found(self, mock_file):
        results = {}
        
        search_in_file('/var/log/dummy_file', 'keyword', results)
        
        # Assertions
        mock_file.assert_called_once_with('/var/log/dummy_file', 'r')
        self.assertIn('/var/log/dummy_file', results)
        self.assertEqual(results['/var/log/dummy_file'], ['This is a test line with keyword'])

    @patch('os.environ.get')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='This is a test line with keyword\nAnother line without')
    def test_search_directory(self, mock_file, mock_os_walk, mock_environ):
        
        # Mock the return values
        mock_environ.return_value = '/var/log'
        mock_os_walk.return_value = [
            ('/var/log', [], ['file1.txt', 'file2.txt'])
        ]
        
        results = search_directory('keyword')
        
        # Assertions
        self.assertIn('/var/log/file1.txt', results) 
        self.assertIn('/var/log/file2.txt', results)
        self.assertEqual(results['/var/log/file1.txt'], ['This is a test line with keyword'])
        self.assertNotEqual(results['/var/log/file2.txt'], ['Another line without'])

    @patch('builtins.open', new_callable=mock_open, read_data='This is a test line\nAnother line without')
    def test_search_in_file_not_found(self, mock_file):
        results = {}
        search_in_file('/var/log/dummy_file', 'keyword', results)

        # Assertions
        mock_file.assert_called_once_with('/var/log/dummy_file', 'r')
        self.assertNotIn('/var/log/dummy_file', results)