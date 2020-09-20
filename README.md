# jira-reports
This python package provides functionality to generate data about jira 
activity and build custom reports based off of that data. This package adds 
the following types of reporting:
 - Task-wise burn down
 
 ## Authentication
This packages uses OAuth to connect with the JIRA cloud api. Credentials are 
stored in env variables for security reasons. The following env variables are 
used to perform the oauth:
 - JIRA_HOST
 - JIRA_CONS_KEY
 
 Note: In order to get the appropriate credentials for oauth, an rsa key-pair 
 is required. The public key is used for adding an application link in JIRA, 
 and the private key is used both in authorizing oauth credentials in the 
 oauth handshake dance, as well as in future reuse of those credentials. More 
 information about oauth specifically with JIRA is available at: 
 https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-oauth-authentication/
 
 Optionally, authorized credentials can be stored in env variables:
 - JIRA_TOKEN
 - JIRA_TOKEN_SECRET
 - JIRA_KEY_CERT
 
 Note: Pycharm does not support multiline env vars - as are used in the RSA 
 key. Credentials can be stored locally in `jira_reports/auth/` as needed - 
 and are strictly ignored by .gitignore. DO NOT COMMIT CREDENTIALS TO 
 VERSION CONTROL.
 
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

## API Information
Jira provides a restful API for their services. Documentation can be found:
https://developer.atlassian.com/cloud/jira/software/rest/intro/ and 
additional documentation is available at: 
https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/

### JIRA API Endpoints
**Get Boards** 

`https://yourdomain_here.atlassian.net/rest/agile/1.0/board/`

**Get Board**

`https://yourdomain_here.atlassian.net/rest/agile/1.0/board/1`

**Get Sprints for board_id**

`https://yourdomain_here.atlassian.net/rest/agile/1.0/board/{board_id}/sprint`

**Get Sprint for sprint_id**

`https://yourdomain_here.atlassian.net/rest/agile/1.0/sprint/{sprint_id}`

**Gets all issues for sprint_id**

`https://yourdomain_here.atlassian.net/rest/agile/1.0/sprint/{sprint_id}/issue`

**Note:** `customfield_10026` is used for story point estimates
