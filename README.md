# jira-reports
This python package provides functionality to generate data about jira 
activity and build custom reports based off of that data. This package adds 
the following types of reporting:
 - Task-wise burn down
 
 ## Authentication
This packages uses OAuth to connect with the JIRA cloud api. Credentials are 
stored in env variables for security reasons. The following env variables are 
used:
 - JIRA_ID
 - JIRA_SECRET
 
 TODO: Add information about the 3 legged auth
 
 ## Setup
 This package uses poetry for dependency management. To install the 
 appropriate dependencies for development, run the following command(s):
 
```
poetry install
```

To install package dependencies without dev requirements, run the following 
command(s):

```
poetry install --no-dev
```

## Usage
This package is intended for use as a dependency for other projects. Example 
usage:

```
# TODO: Implement me
```

## Local Dev Usage
This package can also be run locally, for development or otherwise. Example 
usage from commandline include:

```
# main runner
poetry run runner

# call __main__
poetry run python3 -m jira_reports
```

## Local Dev Quality Tools
This package uses code quality tools. To run these locally, use the following 
commands:

```
# pylint 
poetry run pylint jira_reports
# pytest
poetry run pytest
```
