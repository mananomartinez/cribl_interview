import os
import json

def read_log_file(filepath: str, n_entries: int = 0) -> list:
    """
    Parses a log file and returns every line.
    Assumes each log entry ends with a new line.
    """
    log_entries = []
    with open(filepath, 'r') as file:
        for line in file:
            log_entries.append(line.rstrip('\n'))
    return log_entries

def read_all_log_files(n_entries: int = 0) -> list:
    """
    Traverses a directory and parses every log file within it. 
    Returns a list of dictionaries, each of which uses the file path
    as the key and the logs as list of entries.
    """

    log_directory = os.environ.get('LOG_DIRECTORY', '/var/log')
    all_log_entries = {}

    # Traverse directory
    for root, dirs, files in os.walk(log_directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                entries = read_log_file(filepath)
                if entries:
                    all_log_entries[filepath] = json.dumps(entries)
                else:
                    all_log_entries[filepath] = "File is empty."
            except Exception as e:
                print(f"Error reading: {file}. Won't be included in the response")

    # Display aggregated logs
    return all_log_entries
