import os
from concurrent.futures import ThreadPoolExecutor
from collections import deque


def read_log_file(file_path: str, all_log_entries: dict) -> None:
    """
    Parses by loading chunks of 1MB at the time (max), and parses these
    chunks 1 line at the time. 
    
    The assumption is that each log entry ends with a new line.
    
    Populates the 'all_log_entries' dictionary with the log entries per file. 
    """
    CHUNK_SIZE = 1024 * 1024 # 1MB chunks
    log_entries = deque()

    try:
        with open(file_path, 'r') as file:
            while True:
                chunk = file.readlines(CHUNK_SIZE)
                
                if not chunk:
                    # If no more chunks available, we've reached the end of the file 
                    # and should build a result entry for the dictionary with all 
                    # log entries and filename as key. 

                    if log_entries:
                        all_log_entries[file_path] = list(log_entries)
                    break  # No more chunks
                
                for line in chunk:
                    log_entries.appendleft(line.strip('\n'))

    except Exception as e:
        print(f"Error reading: {file_path}. Won't be included in the response")

def read_all_log_files() -> list:
    """
    Traverses a directory and parses every log file within it. 
    Returns a list of dictionaries, each of which uses the file path
    as the key and the logs as list of entries.
    """

    log_directory = os.environ.get('LOG_DIRECTORY', '/var/log')
    
    all_log_entries = {}
    tasks = []

    # Traverse directory and read each log file in a separate thread
    with ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(log_directory):
            for file in files:
                file_path = os.path.join(root, file)
                task = executor.submit(read_log_file, file_path, all_log_entries)
                tasks.append(task)

        # Wait for each file search task to complete
        for task in tasks:
            task.result()

    # Display aggregated logs
    return all_log_entries
