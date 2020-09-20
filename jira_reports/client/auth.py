"""
This module has been refactored from code documentation from Atlassian to
work with python3. Their original code can be found here:
https://bitbucket.org/atlassianlabs/atlassian-oauth-examples/src/master/python/app.py
"""
import base64
from tlslite.utils import keyfactory
import oauth2 as oauth


class SignatureMethod_RSA_SHA1(oauth.SignatureMethod):
    """
    Custom SignatureMethod for oauth. Implements the attributes and sign
    behavior.
    """
    name = 'RSA-SHA1'

    def signing_base(self, request, consumer, token):
        """
        Base functionality to sign requests.
        :param request: http request
        :param consumer: oauth consumer
        :param token: oauth token
        :return: key and key bytes
        """
        if not hasattr(request, 'normalized_url') or request.normalized_url is None:
            raise ValueError("Base URL for request is not set.")

        sig = (
            oauth.escape(request.method),
            oauth.escape(request.normalized_url),
            oauth.escape(request.get_normalized_parameters()),
        )

        key = '%s&' % oauth.escape(consumer.secret)
        if token:
            key += oauth.escape(token.secret)
        raw = '&'.join(sig)
        return key, bytes(raw, 'utf-8')

    def sign(self, request, consumer, token):
        """
        Build signature string.
        :param request: http request
        :param consumer: oauth consumer
        :param token: oauth token
        :return: signed signature b64
        """
        key, raw = self.signing_base(request, consumer, token)

        private_key = read_key_cert()
        privatekey = keyfactory.parsePrivateKey(private_key)
        signature = privatekey.hashAndSign(raw)

        return base64.b64encode(signature)


def read_key_cert(filename='auth/jira_privatekey.pem'):
    """
    Function reads in the private key data from the pem file for the jira
    integration,
    :param filename: opt filename of private key
    :return: key value
    """
    with open('auth/jira_privatekey.pem', 'r') as j_pk:
        data = j_pk.read()
    private_key = data.strip()
    return private_key

# TODO: Define custom UserNotAuthenticated Exception
