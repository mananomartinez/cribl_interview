import os
from concurrent.futures import ThreadPoolExecutor
from typing import Generator


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
                task = executor.submit(read_single_file, file_path, all_log_entries)
                tasks.append(task)

        # Wait for each file search task to complete
        for task in tasks:
            task.result()
    
    # Display aggregated logs
    return all_log_entries

def read_single_file(file_path: str, all_log_entries: dict) -> None:
    """
    Parses a single file in the /var/log directory.     
    It is assumed that each log entry ends with a new line.
    
    Populates the 'all_log_entries' dictionary with the log entries per file. 
    """
    file_entries = []

    try:
        for line in _read_log_lines(file_path):
            if line:
                file_entries.append(line)
        
        if file_entries:
            all_log_entries[file_path] = file_entries
        else:
            all_log_entries["ERROR"] = f"There were no entries in {file_path}."

    except Exception as e:
        all_log_entries["ERROR"] = f"Error reading: {file_path}. Won't be included in the response."

def read_n_log_entries(file_name: str, n_entries: int) -> list:
    """
    Retrieves N number of entries in the specified file. 
    
    Returns a list of the entries, with the latest entry first
    """
    count = 0
    entries = []
    
    log_directory = os.environ.get('LOG_DIRECTORY', '/var/log')
    
    # Check if the log_directory is already defined in the file_name
    if (file_name.find(log_directory) == -1):
        file_path = log_directory + "/" + file_name
    else:
        file_path = file_name
    
    # Read up to n_entries or the file is exhausted
    for line in _read_log_lines(file_path):
        if line:
            if count < n_entries: 
                    entries.append(line)
                    count += 1
            else:
                break
    return entries

def _read_log_lines(file_path: str) -> Generator[str]:
    """
    Parses a log file and returns every line ordered by the latest first.
    It reads the file from the last line to the first, assuming that logs
    use an append model to adding log entries. 
    Assumes each log entry ends with a new line.
    
    Yields a generator with every line it finds
    """

    chunk_size = 1024
    with open(file_path, 'rb') as f:
        f.seek(0, 2)  
        position = f.tell()
        buffer = b''

        while position > 0:
            read_size = min(chunk_size, position)
            position -= read_size
            f.seek(position)
            buffer = f.read(read_size) + buffer

            while b'\n' in buffer:
                line_end = buffer.rfind(b'\n')
                yield buffer[line_end + 1:].decode('utf-8')
                buffer = buffer[:line_end]

        if buffer:
            yield buffer.decode('utf-8')

