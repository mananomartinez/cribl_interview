import os
from flask import Flask, request, make_response
from parser import read_single_file, search_directory, read_n_log_entries

app = Flask(__name__)

@app.route("/")
def index():
    return "This is a log-reading server as part of the interview process for Cribl."

@app.route('/log')
def get_single_log_file():
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
    keyword = request.args.get('keyword')
    if not keyword:
        return make_response("No keyword provided.", 400)
    
    # Remove quotes from the keyword, if any. 
    keyword = keyword.replace('"', '').replace("'", "")
    results = search_directory(keyword)
    
    if type(results) == dict:
        return results 
    else:
        return make_response(results, 404)
    

@app.route('/log/<file>')
def read_number_of_entries(file: str):
    entries = int(request.args.get('entries'))
    
    if not entries:
        return make_response("No number of enties provided.", 400)
    
    # Remove quotes from the keyword, if any. 
    results = read_n_log_entries(file, entries)
    
    if type(results) == dict:
        return results 
    else:
        return make_response(results, 404)

