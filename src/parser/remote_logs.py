import requests
import json

def make_remote_call(data: dict) -> dict:
    """
    Make requests to a remote server to obtain log information

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
        