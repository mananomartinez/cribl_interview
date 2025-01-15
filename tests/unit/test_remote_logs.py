import unittest
from unittest.mock import patch, mock_open, MagicMock
import requests

from parser import make_remote_call

class TestRemoteLogRequests(unittest.TestCase):

    @patch('requests.get')
    def test_remote_call(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'mocked data'}

        result = make_remote_call({
            "host": "test.com",
            "action": "parse"
        })

        self.assertEqual(result, {'data': 'mocked data'})

    @patch('requests.get')
    def test_remote_call_single_file(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'mocked data'}

        result = make_remote_call({
            "host": "test.com",
            "action": "log",
            "file_name": "file.log"
        })
        self.assertEqual(result, {'data': 'mocked data'})

    @patch('requests.get')
    def test_remote_call_search(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'mocked data'}

        result = make_remote_call({
            "host": "test.com",
            "action": "search",
            "keyword": "mocked"
        })
        self.assertEqual(result, {'data': 'mocked data'})

    @patch('requests.get')
    def test_remote_call_entries(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'mocked data'}

        result = make_remote_call({
            "host": "test.com",
            "action": "entries",
            "file_name": "file.log",
            "entries": 10
        })
        self.assertEqual(result, {'data': 'mocked data'})


    def test_remote_call_invalid_action(self):

        result = make_remote_call({
            "host": "test.com",
            "action": "invalid_action"
        })

        self.assertEqual(result["ERROR"], "Unknown action invalid_action")

    def test_remote_call_missing_values(self):
        
        result = make_remote_call({
            "host": "test.com",
            "action": "entries"
        })
        self.assertEqual(result["ERROR"], "Invalid parameters for entries.")

    @patch('requests.get')
    def test_remote_call_entries(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 400
        mock_response.json.return_value = {'data': 'mocked data'}

        result = make_remote_call({
            "host": "test.com",
            "action": "entries",
            "file_name": "file.log",
            "entries": 10
        })
        self.assertEqual(result["ERROR"], "Remote host (http://test.com) returned status 400")
        