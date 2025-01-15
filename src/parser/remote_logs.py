import requests
import json

def make_remote_call(data: dict) -> dict:
    """
    Constructs and sends an HTTP GET request to a remote host based on the action specified. 
    The method supports several predefined actions, each corresponding to different URIs and query parameters.
    It returns the JSON response from the remote host or an error message if the request fails.

    Parameters:
    - data (dict): A dictionary containing the following keys:
      - "host" (str): The base host for constructing the request URL.
      - "action" (str): The action to perform, which must be one of the predefined actions (`parse`, `search`, `log`, `entries`).
      - "file_name" (str, optional): The name of the file to parse.
      - "entries" (str, optional): The number of entries to obtain from a specific file.
      - "keyword" (str, optional): The keyword to search for in the logs directory.

    Returns:
        - dict: The JSON response from the remote host if the request is successful.
        - dict: An error message if the request fails or if the input data is invalid.
    """
    actions = {
        "parse": { 
            "uri": "/logs",
            "query": ""
        },
        "search": {
            "uri": "/search",
            "query": "?keyword="
        },
        "log": {
            "uri": "/log",
            "query": "?file="
        },
        "entries":{
            "uri": "/log/",
            "query": "?entries="
        }
    }

    # Process the received data
    base_host = data.get("host")

    if base_host: 
        base_host = "http://" + base_host
        # Get possible data payload.
        action = data.get("action")
        file_name = data.get("file_name")
        entries = data.get("entries")
        keyword = data.get("keyword")
        
        
        if action in actions.keys():
            uri = actions[action]["uri"]
            query = actions[action]["query"]

            # Build the URL to make the call
            if entries and file_name:
                url = base_host + uri + file_name + query + str(entries)
            elif file_name:
                url = base_host + uri + query + file_name
            elif keyword:
                url = base_host + uri + query + keyword
            elif action == "parse":
                url = base_host + uri
            else:
                return {"ERROR": f"Invalid parameters for {action}."}
            
            res = requests.get(url)

            if res.status_code == 200:
                return res.json()
            else:
                return {"ERROR": f"Remote host ({base_host}) returned status {res.status_code}"}
        else:
            return {"ERROR": f"Unknown action {action}"}
    else:
        return {"ERROR": f"Missing host value (required)."}
        