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

<!-- 
Given that there could be any number of formats for logs, it is important to normalize each log entry into an object with the most common and useful fields in a log.

These fields are, in no particular order:
 - timestamp
 - message
 - log level (if any)
 - metadata (if any)

 Information considered metada in this case are `user information`, `network information`, `log file`. -->

Additionally, performance can be an issue when there is a large number of files that need to be parsed. This is particularly important for REST requests that can and will timeout if the process of loading the data is long-lived.

To expedite processing of data, each log file within the `/var/log` directory will be read in parallel using a multi-processing approach. 
 
<!-- #### Aggregate log data
Once the data from log files has been normalized, it is necessary to aggregate the data into a specific data structure that will maintain the data from the log files before returning it to the caller.

The options in terms of aggregation will likely be based on timestamp to facilitate the return of newest log entries first in a response to a REST call. 

Given that maintaining large amounts log data in memory can become problem, even if normalized, it is necessary to work with a data schema and structures that minimize memory usage to prevent memory-related issues. -->

#### Return logs for specific file
In order to support this case easily, the general purpose log parsing and aggregation code will be modular so that it can either be called directly from an endpoint with a file name or called from another function that is in charge of going over all files in a directory. 

#### Find specific text/keyword matches
In order to expedite the process of finding text/keywords in a file, it will be simpler to perform the search in the files themselves and return the log entries that contain the matching text. The search will be done in parallel and each matching line in a file will be aggregated to a final hash map that aggregates the results per file.

#### Considerations 

 *Performance*


 *Memory usage*

## Tech Stack requirements
- Python (3.13)
- PipEnv (2024.4.0)
- Flask


## Code Execution
### Virtual environent
When running locally, it is recommended to run this code in a virtual environemt, such as pipenv to avoid installing dependencies on the main python library. For that, it is necessary to install the module `pipenv`. This can be done one of two ways, and both make it available to all projects.

1. Directly with `pip` from the command line, using the command `pip install pipenv` 
2. Using a package manager, such as `homebrew`, with the command `brew install pipenv`

Once installed, navigate to the top of directory of this project in a terminal and issue the command `pip shell` to create and switch the context of the terminal to the new virtual environment. 

### Dependencies
Once in a virtual environment, install the necessary dependencies by simply run the following command in the terminal. 
`pip install -r requirements.txt`

## Testing

To run the unit tests, use the `coverage` module by entering the following command at the root level of this project in a terminal

`coverage run -m pytest ./tests/unit`

To see how much coverage the unit tests have, you can run the command

`coverage report -m`
