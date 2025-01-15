# Cribl Interview Assignment - Jose L. Martinez

## Introduction
This is an assignment as part of the engineering interview process for Cribl. The definition of this project can be found in [this file ](docs/Cribl_log_collection_assignment.pdf)

## Design 
Given the vague nature of the assignment, the approach for this assignment was to focus on the Minimal Viable Product (MVP). This means that the focus is on implementing the most basic functionality with a solid foundation in performance and maintainability for later expansion of features.

### Log Parsing and Aggregation

*ASSUMPTION*: Granted in the requirements was that newest log entries sit at the end of a file. 

This process will be divided into two methods:

- Single log file parser: This method will handle the parsing of individual log files, extracting all log entries.

- Directory navigator and aggregator: This method will traverse the `/var/log` directory, using the single log file parser method to collect and parsw log entries from all files.

#### Data Aggregation

Each parsed log entry will be aggregated into an array, which is then stored in a hashmap. The keys of this hashmap are the file paths, providing a clear association between each file and its corresponding log entries. When parsing multiple files, the individual hashmaps are merged into a larger hashmap to provide a comprehensive view of all collected logs.

#### Performance Considerations

Handling a large number of files or processing particularly large log files can be performance-intensive. This is especially critical in scenarios involving REST API requests, where prolonged data processing can lead to timeouts.

To enhance performance and mitigate bottlenecks, the system will employ a multi-threaded approach. This will allow multiple log files within the `/var/log` directory to be read and processed in parallel, significantly increasing throughput and reducing the time required to aggregate all log data.

### Find specific text/keyword matches
In order to expedite the process of finding text/keywords in a file, it will be simpler to perform the search in the files themselves and return the log entries that contain the matching text. 

To ensure that the code is performant, the search will be done in parallel and each matching line in a file will be aggregated to a final hash map that aggregates the results per file.

### Return specific number of entries 
The MVP for this was reduced to returning N-number of entries from one file with an eye towards allowing for scaling up later on, if needed.

This endpoint takes a file name with a relative path as well as a positive integer value indicating the number of log entries to retrieve from that file. 

### Considerations 

#### Performance
Given that log files can be rather large, and that there could be a large number of files in the directory, it was important to make sure that the code performed in an efficient fashion. By using multi-threading, when searching or parsing all the log files in the directory, it is possible to parse files without having to wait for completion of the previous one.

This is of particular importance when dealing with large files because it would take a long time to parse and would block completion of the process for other files. 

#### Memory usage*
When parsing a file, or group of files, the contents must be kept in memory before returning to the caller. In order to prevent holding duplicate records in memory, it is best to read files line by line and contrain the memory load to the response as it is being built. 

This presents some challenges with Python because it defaults to reading from the beginning of a file and not the end, which means that it is important to write the line-by-line parsing that accomodates log files with newer records at the end of the file..

## Tech Stack requirements
- Python (3.1.0)
- Flask (3.1.3)
- requests (2.32.3)
- PipEnv (2024.4.0)
- coverage (7.6.10)

## Endpoints
### `/ -- index`
This endpoint returns a message about the server. 

### `/logs -- get all logs`
- Method: `GET`

- This endpoint will traverse the log directory and aggregate the logs for all the files it finds in the directory, if they are readable. 

- If no files exist or none of them are readable, returns error with status code `404`.

### `/log?file=` -- get single log file endpoint
- Method: `GET`

- This endpoint will traverse the log directory for a file with the name provided in the `file` query parameter and return the contents if it exists and it is readable. 

- If no file name is provided in the `file` query parameter, returns error with status code `400`.

- If the file does not exist, returns error with status code 404.

### ` /log/<file>?entries=` -- get _n_ entries for a specific log file endpoint
- Method: `GET`

- This endpoint will obtain N log entries in the specified file with the name provided in the `<file>` path and using the `entries` parameter.

- If the value entered for `entries` is less than or equal to 0 or not a number, an error will be returned with status code `400`

- If nothing is entered for the `entries` query parameter, returns error with status code `400`.

- If the file does not exist, returns error with status code 404.

### `/search?keyword=` -- search log files endpoint
- Method: `GET`

- This endpoint will traverse the log directory and aggregte the contents of every log file it finds. 

- If no keyword/text is provided in the `keyword` query parameterreturns error with status code `400`.

- If the file does not exist, returns error with status code `404`.

### `/remote` -- access remote log files endpoint 
- Method: `POST`
- This endpoint provides acces to a remote deployment of this server to obtain log information from that system. 

- The endpoint takes a JSON payload that requires a target `host` (IP address or domain name and por) and an `action` to indicate the endpoint to call. 

  - The action mappings are as follows, along with the other fields required for each one: 
    - parse = /logs
      - None
    - search = /search?keyword=
      - `keyword`
    - log = /log?file_name=
      - `file_name` of the target file in the remote host 
    - entries = /log/<file_name>?entries=
      - `file_name` of the target file in the remote host 
      - `entries` positive integer value for the number of log entries to retrieve 

  - Example payload:

 ```json
    {
        "host":"localhost:8000",
        "action":"entries",
        "file_name":"install.log",
        "entries": 5
    }
```

## Setup and execution
### Virtual environent
When running locally, it is recommended to run this code in a virtual environemt, such as pipenv to avoid installing dependencies on the main python library. For that, it is necessary to install the module `pipenv`. This can be done one of two ways, and both make it available to all projects.

1. Directly with `pip` from the command line, using the command `pip install pipenv` (Note that this could fail, if Python is managed by OS.)
2. Using a package manager, such as `homebrew`. For example, `brew install pipenv`

Once installed, navigate to the top of directory of this project in a terminal and issue the command `pip shell` to create and switch the context of the terminal to the new virtual environment. 

### Install dependencies
Once in a virtual environment, install the necessary dependencies by simply run the following command in the terminal. 
`pip install -r requirements.txt`

### Execution
- Navigate to the root of this project in the terminal
- Ensure that all dependecies have been installed
- Execute the command `flask --app ./src/parser/log_server.py run`

This will run the server on the default port, `5000`. 

#### Running multiple servers.
It is possible to run multiple instances of this server on the same machine. To do so, the port number needs to change for each instance. 

To achieve this, simply add `--port=` to the end of the command. For example: `flask --app ./src/parser/log_server.py run --port=8000`

This 

### Optional
To change the log directory to parse from `/var/log`, set the `LOG_DIRECTORY` environment variable before running the server. Otherwise, `/var/log` will be the default. 

## Testing

To run the unit tests, use the `coverage` module by entering the following command at the root level of this project in a terminal

`coverage run -m pytest ./tests/unit`

To see how much coverage the unit tests have, you can run the command

`coverage report -m`
