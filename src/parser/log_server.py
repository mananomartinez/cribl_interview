import os
from flask import Flask, request
from parser import read_all_log_files, read_log_file

app = Flask(__name__)

@app.route("/")
def index():
    return "This is a log-reading server as part of the interview process for Cribl."

@app.route('/logs')
def get_all_logs():
    return read_all_log_files()

@app.route('/log')
def get_single_log_file():
    file_name = request.args.get('file')
    dir = os.environ.get('LOG_DIRECTORY', '/var/log')
    return read_log_file(dir + "/" + file_name)