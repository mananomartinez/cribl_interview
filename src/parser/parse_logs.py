import os
from concurrent.futures import ThreadPoolExecutor
from typing import Generator


def read_all_log_files() -> list:
    """
    This function traverses the directory specified by the environment variable 
    `LOG_DIRECTORY` (or '/var/log' by default) and reads each log file. It uses a 
    thread pool to read the log files concurrently, and aggregates the log entries 
    into a dictionary.

    Returns:
        list: A list of aggregated log entries from all the log files found in the 
              specified log directory. 
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
    Reads a single log file and stores its contents in a provided dictionary.
    Each line from the file is collected and added to a list, which is then 
    associated with the file path in the dictionary.

    Parameters:
      - file_path (str): The path to the log file to be read.
      - all_log_entries (dict): A dictionary to store the log entries. 
                                The file path is used as the key, and a list of log lines is the value.

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
        print(f"Error reading: {file_path}. Won't be included in the response.")

def read_n_log_entries(file_name: str, n_entries: int) -> list:
    """
    Reads up to a specified number of log entries from a given log file. 
    The method ensures that only the most recent entries are returned, 
    up to the maximum number specified.

    Parameters:
      - file_name (str): The name of the log file to read. 
      - n_entries (int): The maximum number of log entries to read from the file.

    Returns:
      - dict: A dictionary with the file path as the key and a list of up to `n_entries` log entries as the value.

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
    return {file_path: entries}

def _read_log_lines(file_path: str) -> Generator[str]:
    """
    Reads a log file in reverse order and yields each line from the end to the beginning. 
    This method efficiently reads large log files by processing chunks of data in reverse 
    without loading the entire file into memory.

    Parameters:
      - file_path (str): The path to the log file to be read.

    Yields:
      - str: Each line from the log file, starting from the last line and working backwards to the first.
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

