# Cribl Interview Assignment - Jose L. Martinez

## Introduction

### Problem statement

A customer has asked you for a way to provide on-demand monitoring of various unix-based servers without having to log into each individual machine and opening up the log files found in /var/log. The customer has asked for the ability to issue a REST request to a machine in order to retrieve logs from /var/log on the machine receiving the REST request.

### Acceptance criteria

1. HTTP REST API should be the primary interface to make data requests

2. The results returned must be presented with the newest log events first.

3. The REST API should support additional query parameters which include:

    a. The ability to specify a filename within /var/log

    b. The ability to specify the last n number of log entries to retrieve within the log

    c. The ability to filter results based on basic text/keyword matches
  
4. Must not use any pre-built log aggregation systems - this must be custom, purpose-built software.

5. Minimize the number of external dependencies in the business logic code path (framework things like HTTP servers, etc are okay)

#### Bonus points:
There is potential to double the deal size with this customer if you can successfully implement “nice-to-have” features that will make your produce more valuable to them:

1. The ability to issue a REST request to one “primary” server in order to retrieve logs from a list of “secondary” servers. There aren’t any hard requirements for the protocol used between the primary and secondary servers.

2. A basic UI to demo the API

## Design 

### Milestones

This assignment can be broken up into multiple milestones that, following a specific sequence, can yield the desired results. The following sections outline what each of these milestones are  

#### Access log data
This is the most important step because it provides the data that the next steps will manipulate and return to the caller of an endpoint. 

The code will query each and every single file, recursing into directories, and pull every line of logs. The data for each file will be aggregated into an array to maintain the order in which the log entry arrive when converting to JSON. 

Additionally, performance can be an issue when there is a large number of files that need to be parsed. This is particularly important for REST requests that can and will timeout if the process of loading the data is long-lived. 

To expedite processing of data, each log file within the `/var/log` directory will be read in parallel using a multi-processing approach. 

#### Return logs for specific file
In order to support this case easily, the general purpose log parsing and aggregation code will be modular so that it can either be called directly from an endpoint with a file name or called from another function that is in charge of going over all files in a directory. 

#### Find specific text/keyword matches
In order to expedite the process of finding text/keywords in a file, it will be simpler to perform the search in the files themselves and return the log entries that contain the matching text. 

The search will be done in parallel and each matching line in a file will be aggregated to a final hash map that aggregates the results per file.

#### Considerations 

 *Performance*


 *Memory usage*

## Tech Stack requirements
- Python (3.1.0)
- Flask (3.1.3)
- PipEnv (2024.4.0)
- coverage (7.6.10)

## Endpoints
### `index endpoint (/)`
This endpoint returns a message about the server. 

### `get all logs endpoint (/logs)`
- This endpoint will traverse the log directory and aggregate the logs for all the files it finds in the directory, if they are readable. 
- If no files exist or none of them are readable, returns error with status code `404`.

### `get single log file endpoint (/log?file=)`
- This endpoint will traverse the log directory for a file with the name provided in the `file` query parameter and return the contents if it exists and it is readable. 
- If no file name is provided in the `file` query parameter, returns error with status code `400`.
- If the file does not exist, returns error with status code 404.

### `search log files endpoint (/search?keyword=)`
- This endpoint will traverse the log directory and aggregte the contents of every log file it finds. 
- If no keyword/text is provided in the `keyword` query parameterreturns error with status code `400`.
- If the file does not exist, returns error with status code `404`.

## Setup 
### Virtual environent
When running locally, it is recommended to run this code in a virtual environemt, such as pipenv to avoid installing dependencies on the main python library. For that, it is necessary to install the module `pipenv`. This can be done one of two ways, and both make it available to all projects.

1. Directly with `pip` from the command line, using the command `pip install pipenv` (Note that this could fail, if Python is managed by OS.)
2. Using a package manager, such as `homebrew`. For example, `brew install pipenv`

Once installed, navigate to the top of directory of this project in a terminal and issue the command `pip shell` to create and switch the context of the terminal to the new virtual environment. 

### Install dependencies
Once in a virtual environment, install the necessary dependencies by simply run the following command in the terminal. 
`pip install -r requirements.txt`

## Execution
- Navigate to the root of this project in the terminal
- Ensure that all dependecies have been installed
- Execute the command `flask --app ./src/parser/log_server.py run`

### Optional
To change the log directory to parse from `/var/log`, set the `LOG_DIRECTORY` environment variable before running the server. Otherwise, `/var/log` will be the default. 

## Testing

To run the unit tests, use the `coverage` module by entering the following command at the root level of this project in a terminal

`coverage run -m pytest ./tests/unit`

To see how much coverage the unit tests have, you can run the command

`coverage report -m`
