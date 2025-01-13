import os
from concurrent.futures import ThreadPoolExecutor
from collections import deque


def read_log_file(file_path: str, all_log_entries: dict, n_entries: int = 0) -> list:
    """
    Parses a log file and returns every line ordered by the latest first.
    Assumes each log entry ends with a new line.
    """
    log_entries = deque()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                log_entries.appendleft(line.strip('\n'))

    except Exception as e:
        print(f"Error reading: {file_path}. Won't be included in the response")

    if log_entries:
        all_log_entries[file_path] = list(log_entries)


def read_all_log_files(n_entries: int = 0) -> list:
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
