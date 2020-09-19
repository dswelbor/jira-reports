"""
This module serves to wrap auth logic for the jira api python wrapper. It
also serves as a starting point for extending additional custom behavior for
the client.
"""
import json
import jira


class JiraClient:
    """
    Basic wrapper class for the python-jira api wrapper. Wraps authentication
    and can be used for extending custom query logic.
    """
    def __init__(self):
        """
        Superclass ctor for the jira client.
        """
        # TODO: Try to read oauth dict file if present
        try:
            self._read_auth()
        except Exception:
            # no credentials file - build one
            pass

        # TODO: Handle creating dict file if not present

    def _read_auth(self):
        """
        Read auth from file.
        """
        with open('jira_oauth.json', 'rb') as auth_file:
            self.__credentials = json.load(auth_file)

    def _handshake(self):
        """
        This method performs the 3l oauth handshake.
        """
        pass
