import os
from concurrent.futures import ThreadPoolExecutor

def search_in_file(file_path: str, keyword: str, results: dict) -> None:
    """
    Searches for a specific keyword in a given file and stores the lines containing the keyword in a shared results dictionary.

    Parameters:
    - file_path (str): The path to the file that will be searched.
    - keyword (str): The keyword to search for within the file.
    - results (dict): A dictionary to store the search results. The file path is used as the key,
                      and the value is a list of lines where the keyword was found.

    """
    
    found_in_file = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if keyword in line:
                    found_in_file.append(line.strip('\n'))
            if found_in_file:
                results[file_path] = found_in_file

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def search_directory(keyword: str) -> dict:
    """
    Searches for a specific keyword in all log files within a specified directory. 
    By default, the directory is set to `/var/log`, but this can be overridden using 
    the `LOG_DIRECTORY` environment variable.

    This method uses multi-threading to concurrently search through multiple files, 
    improving the efficiency of the search process. 
    Each file is processed in a separate thread, and the results are collected in a shared dictionary.

    Parameters:
        - keyword (str): The keyword to search for within the log files.

    Returns:
        - dict: A dictionary containing file paths as keys and lists of lines where the keyword was found as values.
        - dict: An error message if the keyword is not found.
    """
    results = {}
    tasks = []
    log_directory = os.environ.get('LOG_DIRECTORY', '/var/log')

    # Create a thread per file to search
    with ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(log_directory):
            for file in files:
                file_path = os.path.join(root, file)
                task = executor.submit(search_in_file, file_path, keyword, results)
                tasks.append(task)

        # Wait for each file search task to complete
        for task in tasks:
            task.result()
    
    if results:
        return results
    else:
        return {"ERROR": f"Keyword '{keyword}' was not found in any file in the {log_directory} directory."}