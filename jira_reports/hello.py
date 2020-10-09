"""
This is a placeholder module. More coming soon.
"""

from jira_reports.client.jira_client import JiraClient


def pardon_dust():
    """
    This is a simple hello world function. More to come.
    :return: message
    """
    msg = 'Hello World. More coming soon. Please don\'t write in the dust.'
    return msg


def main():
    """
    This defines the simple main functionality - and serves as the entry
    point
    :return: None
    """
    hello_str = pardon_dust()
    print(f'[main]: {hello_str}')
    j_client = JiraClient()
    # issue = j_client.client.issue('DEVPM-1')
    # issues = j_client.client.search_issues('sprint in openSprints() and sprint not in futureSprints()')
    # stories = [issue for issue in issues if issue.fields.issuetype.name == 'Story']
    # test_result = j_client.test_issue()
    test_result_2 = j_client.test_sprints()
    test_results_3 = j_client.test_sprint_issues()
    # print('Jira client initialized')
    print('test done')
