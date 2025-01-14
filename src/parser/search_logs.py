import os
from concurrent.futures import ThreadPoolExecutor

def search_in_file(file_path: str, keyword: str, results: dict) -> None:
    """
    Search for the text in a single file.
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
    Search for the text in all files in the directory recursively.
    
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
        return f"Keyword '{keyword}' was not found in any file in the {log_directory} directory."