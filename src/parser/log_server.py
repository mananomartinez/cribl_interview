import os
from flask import Flask, request, make_response
from parser import read_single_file, search_directory, read_n_log_entries, read_all_log_files, make_remote_call

app = Flask(__name__)

@app.route("/")
def index():
    """
    Endpoint that returns a simple message about this server.

    
    Returns: Message about this server's purpose.
    
    """    
    return "This is a log-reading server as part of the interview process for Cribl."

@app.route('/logs')
def get_all_logs():
    """
    Endpoint to navigate the /var/log directory, parse the log entries for each log file found
    and return these entries associated per file of origin.

    
    Returns: A hashmap that has all log entries in each file with the key 
             being the name of the file and an array with the entries for that file.
    
    """    
    results = read_all_log_files()
    if results:
        return results
    else:
        return make_response("No readable log files found.", 404)

@app.route('/log')
def get_single_log_file():
    """
    Endpoint to parse the entries in a single log file and return the
    entries and the file of origin.

    Query parameter: file_name
        - The name of the file to parse the entries from.

    Returns: A hashmap that has all log entries in the file with the key 
             being the name of the file and an array with the entries for that file.
    
    """
    file_name = request.args.get('file')
    if not file_name:
        return make_response("No file name provided.", 400)
    
    # Remove quotes from the file_name, if any. 
    file_name = file_name.replace('"', '').replace("'", "")
    log_directory = os.environ.get('LOG_DIRECTORY', '/var/log')

    # Check if the log_directory is already defined in the file_name
    if (file_name.find(log_directory) == -1):
        file_path = log_directory + "/" + file_name
    else: 
        file_path = file_name

    results = {}
    read_single_file(file_path, results)
    
    if results:
        return results
    else:
        return make_response(f"File '{file_name}' not found.", 404)

@app.route('/search')

def search_logs():
    """
    Endpoint to search all files and return the entries that contain the keyword 
    and the files where it was found.

    Query parameter: keyword
        - A word or words to search for across all files in the /var/log directory

    Returns: A hashmap that has all log entries that contain the keyword value, 
             with the key being the name of the file and an array with the entries for that file.
    
    """      
    keyword = request.args.get('keyword')
    if not keyword:
        return make_response("No keyword provided.", 400)
    
    # Remove quotes from the keyword, if any. 
    keyword = keyword.replace('"', '').replace("'", "")
    results = search_directory(keyword)
    
    if results["ERROR"]:
        return make_response(results, 404)
    else:
        return results 
        
    

@app.route('/log/<file>')
def read_number_of_entries(file: str):
    """
    Endpoint to retrieve n-number of entries in a specific log file.

    Method: GET
    URI path parameter: file name
        - The name of the file to retrieve n-number of entries

    Query parameter: entries 
        - A positive integer that indicates the number of entries to retrieve
          from the specified file.

    Returns: A hashmap that has n-number of entries with the key being the name of 
             the file and an array with the entries for that file.
    
    """       
    try: 
        entries = int(request.args.get('entries'))

        if not entries:
            return make_response("No number of entries provided.", 400)
        elif entries <= 0:
            return make_response("Invalid number of entries provided. Must be a positive integer.", 400)
        
        # Remove quotes from the keyword, if any. 
        results = read_n_log_entries(file, entries)
        
        if type(results) == dict:
            return results 
        else:
            return make_response(results, 404)
    except Exception as e:
        return make_response(e, 500)

@app.route('/remote', methods=['POST'])
def receive_data():
    """
    Endpoint to access a remote instance of this server 
    to obtain log information from that host.

    Method: POST
    Payload: 
      - Required values:
        - host: The host IP or domain name with port, if not 80
        - action: what functionality to access in remote instance
          - 'parse', 'log', 'entries', or 'search'.
      - Action values:
        - file_name: Required for single 'log' and 'entries' actions
        - entries: Positive integer for number of entries to retrieve from a log file
        - keyword: Word or text to search in the remote server instance

    Returns: A hashmap that has n-number of entries with the keys being the name of 
             the file and an array with the entries for that file.
    
    """    
    data = request.get_json()

    # Process the received data
    if data:
        resp = make_remote_call(data)
        if "ERROR" in resp:
            return make_response(f"Error making request to host {data.get("host")}: { resp['ERROR']}", 400)
    else:
        return make_response("Invalid payload.", 400)
    # Return a response
    return resp