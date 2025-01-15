import requests
from concurrent.futures import ThreadPoolExecutor

def make_remote_call(data: dict) -> dict:

    all_log_entries = {}
    tasks = []
    
    base_host_list = data.keys()
    
    # Create a thread per host to connect to
    with ThreadPoolExecutor() as executor:
        for base_host in base_host_list:
            data_per_host = data.get(base_host)
            task = executor.submit(_make_remote_call_per_file, base_host, data_per_host, all_log_entries)
            tasks.append(task)

        # Wait for each file search task to complete
        for task in tasks:
            task.result()
    return all_log_entries
    

def _make_remote_call_per_file(base_host: str, data: dict, all_log_entries: dict) -> dict:
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
        "logs": { 
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


    if not base_host.startswith("http"):
        base_host = "http://" + base_host
    
    # Get possible data payload.
    action = data.get("action")
    file_name = data.get("file_name")
    entries = data.get("entries")
    keyword = data.get("keyword")
    
    url = None
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
        elif action == "logs":
            url = base_host + uri
        else:
            result = {"ERROR": f"Invalid parameters for {action}."}
        
        if url:
            res = requests.get(url)

            if res.status_code == 200:
                result = res.json()
            else:
                result = {"ERROR": f"Remote host ({base_host}) returned status {res.status_code}"}

    else:
        result = {"ERROR": f"Unknown action {action}"}
    
    all_log_entries[base_host] = result
