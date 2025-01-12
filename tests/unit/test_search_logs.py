import unittest
from unittest.mock import patch, mock_open
from src.parser.search_logs import search_in_file, search_directory

class TestSearchLogs(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='This is a test line with keyword\nAnother line without')
    def test_search_in_file_found(self, mock_file):
        results = {}
        
        search_in_file('dummy_path', 'keyword', results)
        
        # Assertions
        mock_file.assert_called_once_with('dummy_path', 'r')
        self.assertIn('dummy_path', results)
        self.assertEqual(results['dummy_path'], ['This is a test line with keyword'])

    @patch('builtins.open', new_callable=mock_open, read_data='This is a test line\nAnother line without')
    def test_search_in_file_not_found(self, mock_file):
        results = {}
        
        search_in_file('dummy_path', 'keyword', results)

        # Assertions
        mock_file.assert_called_once_with('dummy_path', 'r')
        self.assertNotIn('dummy_path', results)

    @patch('os.environ.get')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='This is a test line with keyword\nAnother line without')
    def test_search_directory(self, mock_file, mock_os_walk, mock_environ):
        
        # Mock the return values
        mock_environ.return_value = '/mock/log/directory'
        mock_os_walk.return_value = [
            ('/mock/directory', [], ['file1.txt', 'file2.txt'])
        ]
        
        results = search_directory('keyword')
        
        # Assertions
        self.assertIn('/mock/directory/file1.txt', results) 
        self.assertIn('/mock/directory/file2.txt', results)
        self.assertEqual(results['/mock/directory/file1.txt'], ['This is a test line with keyword'])
        self.assertEqual(results['/mock/directory/file2.txt'], ['This is a test line with keyword'])
