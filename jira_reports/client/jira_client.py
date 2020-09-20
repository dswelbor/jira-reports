"""
This module serves to wrap auth logic for the jira api python wrapper. It
also serves as a starting point for extending additional custom behavior for
the client. For more information about jira cloud oauth visit:
https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-oauth-authentication/
"""
import json
import os
import oauth2 as oauth
from tlslite.utils import keyfactory
from urllib import parse
from jira import JIRA

from jira_reports.client.auth import SignatureMethod_RSA_SHA1, read_key_cert


class JiraClient:
    """
    Basic wrapper class for the python-jira api wrapper. Wraps authentication
    and can be used for extending custom query logic.
    """

    def __init__(self, init_auth=None):
        """
        Superclass ctor for the jira client. Credentials are either stored
        in env vars or a json file. If neither are found, an exception will
        be thrown. To create these credentials, use the init_auth param
        :param init_auth: opt param to init auth handshake
        """
        self.base_url = os.environ['JIRA_HOST']
        self._consumer_key = os.environ['JIRA_CONS_KEY']
        self._consumer_secret = 'unused'
        self.req_token_end = '/plugins/servlet/oauth/request-token'
        self.access_token_end = '/plugins/servlet/oauth/access-token'
        self.handshake_end = '/plugins/servlet/oauth/authorize'

        if init_auth:
            # args to init oauth handshake
            self._handshake()
        else:
            # env or file based credentials
            try:
                self.__credentials = {
                    'access_token': os.environ['JIRA_TOKEN'],
                    'access_token_secret': os.environ['JIRA_TOKEN_SECRET'],
                    'consumer_key': self._consumer_key,
                    'key_cert': os.environ['JIRA_KEY_CERT']
                }
            except KeyError:
                # no env vars - read from file
                self._read_auth()
        # Add authorized jira api client
        self.client = JIRA(self.base_url, oauth=self.__credentials)

    def _read_auth(self):
        """
        Read auth from file.
        """
        with open('auth/jira_oauth.json', 'rb') as auth_file:
            self.__credentials = json.load(auth_file)

    def _handshake(self):
        """
        This method performs the oauth handshake for jira's API. More info
        about this handshake is available at:
        https://bitbucket.org/atlassianlabs/atlassian-oauth-examples/src/master/python/app.py
        """
        # TODO: refactor to 'prepare_client()'
        token_url = f'{self.base_url}{self.req_token_end}'
        consumer = oauth.Consumer(self._consumer_key, self._consumer_secret)
        client = oauth.Client(consumer)
        client.set_signature_method(SignatureMethod_RSA_SHA1())
        resp, resp_body = client.request(token_url, "POST")

        # Valid consumer key
        if resp.status == 200:
            handshake_url = f'{self.base_url}{self.handshake_end}'
            body_str = str(resp_body, 'utf-8')
            r_tokens = dict(parse.parse_qsl(body_str))
            print(f'Success! Please visit: '
                  f'{handshake_url}?oauth_token={r_tokens["oauth_token"]}\n'
                  f'\toauth_token: {r_tokens["oauth_token"]}\n'
                  f'\toauth_token_secret: {r_tokens["oauth_token_secret"]}\n')
            input("Press Enter to continue...")

            # Finalize authorization
            access_url = f'{self.base_url}{self.access_token_end}'
            oauth_tokens = oauth.Token(r_tokens['oauth_token'],
                                          r_tokens['oauth_token_secret'])
            client = oauth.Client(consumer, oauth_tokens)
            client.set_signature_method(SignatureMethod_RSA_SHA1())
            resp, resp_body = client.request(access_url, "POST")
            # Success - user authorized
            if resp.status == 200:
                body_str = str(resp_body, 'utf-8')
                valid_tokens = dict(parse.parse_qsl(body_str))
                key_cert = read_key_cert()
                self.__credentials = {
                    'access_token': valid_tokens['oauth_token'],
                    'access_token_secret': valid_tokens['oauth_token_secret'],
                    'consumer_key': self._consumer_key,
                    'key_cert': key_cert
                }
                with open('auth/jira_oauth.json', 'w') as auth_file:
                    json.dump(self.__credentials, auth_file)
            # Failure - user did not auth
            else:
                print('User did not authorize')

        # invalid consumer key
        else:
            print('Failed to start OAuth handshake')
            # TODO: Add exception here
            # raise oauth.error.UserNotAuthenticated(str(resp.status))

    def test_issue(self):
        """Just a test method"""
        test_url = f'{self.base_url}/rest/api/3/issue/DEVPM-1'
        consumer = oauth.Consumer(self._consumer_key, self._consumer_secret)
        test_tokens = oauth.Token(self.__credentials['access_token'],
                                  self.__credentials['access_token_secret'])
        test_client = oauth.Client(consumer, test_tokens)
        test_client.set_signature_method(SignatureMethod_RSA_SHA1())
        resp, resp_body = test_client.request(test_url, "GET")
        if resp.status == 200:
            print('test - get issue - success')
            resp_body_dict = json.loads(resp_body)
            print(json.dumps(resp_body_dict, indent=2))
        else:
            print(f'Error: {str(resp_body, "utf-8")}')
            # TODO: Throw custome exception
        print('sucess')

    def test_sprint(self):
        """Just a test method"""
        sprint_id = '1'
        test_url = f'{self.base_url}/rest/agile/1.0/sprint/{sprint_id}'
        consumer = oauth.Consumer(self._consumer_key, self._consumer_secret)
        test_tokens = oauth.Token(self.__credentials['access_token'],
                                  self.__credentials['access_token_secret'])
        test_client = oauth.Client(consumer, test_tokens)
        test_client.set_signature_method(SignatureMethod_RSA_SHA1())
        resp, resp_body = test_client.request(test_url, "GET")
        if resp.status == 200:
            print('test - get sprint - success')
            resp_body_dict = json.loads(resp_body)
            print(json.dumps(resp_body_dict, indent=2))
            return resp_body_dict
        else:
            print(f'Error: {str(resp_body, "utf-8")}')
            # TODO: Throw custome exception
        print('success')

    def test_sprints(self):
        """Just a test method"""
        board_id = '1'
        test_url = f'{self.base_url}/rest/agile/1.0/board/{board_id}/sprint'
        print(f'Getting board_id={board_id}\'s sprints\n{test_url}')
        consumer = oauth.Consumer(self._consumer_key, self._consumer_secret)
        test_tokens = oauth.Token(self.__credentials['access_token'],
                                  self.__credentials['access_token_secret'])
        test_client = oauth.Client(consumer, test_tokens)
        test_client.set_signature_method(SignatureMethod_RSA_SHA1())
        resp, resp_body = test_client.request(test_url, "GET")
        if resp.status == 200:
            print('test - get board\'s sprints - success')
            resp_body_dict = json.loads(resp_body)
            print(json.dumps(resp_body_dict, indent=2))
            return resp_body_dict
        else:
            print(f'Error: {str(resp_body, "utf-8")}')
            # TODO: Throw custome exception
        print('success')

    def test_sprint_issues(self):
        """Just a test method"""
        sprint_id = '1'
        test_url = f'{self.base_url}/rest/agile/1.0/sprint/{sprint_id}/issue'
        print(f'Getting sprint_id={sprint_id}\'s issues\n{test_url}')
        consumer = oauth.Consumer(self._consumer_key, self._consumer_secret)
        test_tokens = oauth.Token(self.__credentials['access_token'],
                                  self.__credentials['access_token_secret'])
        test_client = oauth.Client(consumer, test_tokens)
        test_client.set_signature_method(SignatureMethod_RSA_SHA1())
        resp, resp_body = test_client.request(test_url, "GET")
        if resp.status == 200:
            print('test - get board\'s sprints - success')
            resp_body_dict = json.loads(resp_body)
            print(json.dumps(resp_body_dict, indent=2))
            return resp_body_dict
        else:
            print(f'Error: {str(resp_body, "utf-8")}')
            # TODO: Throw custome exception
        print('success')
