import os
from flask import Flask, request, make_response
from parser import read_all_log_files, read_log_file, search_directory

app = Flask(__name__)

@app.route("/")
def index():
    return "This is a log-reading server as part of the interview process for Cribl."

@app.route('/logs')
def get_all_logs():
    results = read_all_log_files()
    if results:
        return results
    else:
        return make_response("No readable log files found.", 404)

@app.route('/log')
def get_single_log_file():
    file_name = request.args.get('file')
    if not file_name:
        return make_response("No file name provided.", 400)
    
    # Remove quotes from the file_name, if any. 
    file_name = file_name.replace('"', '').replace("'", "")
    
    # Construct the dir since the file name is not a full path
    dir = os.environ.get('LOG_DIRECTORY', '/var/log')
    results = read_log_file(dir + "/" + file_name)
    
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
