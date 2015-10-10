""" Library to provide access to MLKSHK API. """

import base64
import datetime
import hmac
from hashlib import md5, sha1
# import json
import random
import requests
# from requests_oauthlib import OAuth2
import time
import urllib
import webbrowser

from .models import (
    SharedFile,
    User,
    Comment,
    Shake
)

from .errors import (
    ApiResponseUnauthorized,
    ApiInstanceUnauthorized,
    NotFound404
)


class Api(object):

    def __init__(self,
                 consumer_key=None,
                 consumer_secret=None,
                 access_token_key=None,
                 access_token_secret=None,
                 base_url=None):

        if base_url is None:
            self.base_url = 'http://mlkshk.com'
        else:
            self.base_url = base_url

        self.port = 80

        # Set headers, client info for requests.
        default_headers = {'User-Agent': 'PyShk v0.0.1'}
        self.client_args = {}
        self.client_args['headers'] = default_headers

        # Set up auth - TODO:
        # self.auth = None
        # if self.access_token_key:
        #     token = {
        #         'token_type': 'mac',
        #         'hash_algorithm': 'hmac-sha-1',
        #         'access_token': self.access_token_key
        #     }
        #     self.auth = OAuth2(self.consumer_key, token=token)
        # self.client = requests.Session()
        # self.client.auth = self.auth

        self.SetCredentials(
            consumer_key,
            consumer_secret,
            access_token_key,
            access_token_secret)

    ####################################################################
    # Helper Functions
    ####################################################################

    def DoAuthDance(self,
                    redirect_uri=None):
        if not redirect_uri:
            redirect_uri = "http://localhost:8000"
        authentication_url = (
            "https://mlkshk.com/api/authorize"
            "?response_type=code&client_id={key}&redirect_uri={uri}").format(
                key=self.consumer_key,
                uri=redirect_uri)
        print(authentication_url)
        access_token_url = 'https://mlkshk.com/api/token'
        webbrowser.open(authentication_url, new=1)
        authorization_code = input("Enter the code from the redirected URL: ")
        message = {
            'grant_type': "authorization_code",
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret
        }
        data = urllib.parse.urlencode(message)
        req = requests.post(access_token_url, params=data, verify=False)
        json_resp = req.json()
        print("""
            {full_token}
            >>> Your access token is: {token}
            >>> Your access secret is: {secret}
            """.format(full_token=json_resp,
                       token=json_resp['access_token'],
                       secret=json_resp['secret']))

        self.access_token_key = json_resp['access_token']
        self.access_token_secret = json_resp['secret']

    def SetCredentials(self,
                       consumer_key=None,
                       consumer_secret=None,
                       access_token_key=None,
                       access_token_secret=None):
        """Set the consumer_key and consumer_secret for this instance

        Args:
          consumer_key:
            The consumer_key of the MLKSHK app.
          consumer_secret:
            The consumer_secret for the MLKSHK app.
          access_token_key:
            The oAuth access token key value you retrieved
            from running DoAuthDance().
          access_token_secret:
            The oAuth access token's secret, also retrieved
            from the DoAuthDance() run.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        auth_list = [consumer_key, consumer_secret,
                     access_token_key, access_token_secret]

        if not all(auth_list):
            raise ApiInstanceUnauthorized
        self.authenticated = True

    def _get_url_endpoint(self, endpoint):
        return self.base_url + endpoint

    def _RequestUrl(self, verb, endpoint=None, data=None):
        if not self.authenticated:
            raise ApiInstanceUnauthorized

        timestamp = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        nonce = self.get_nonce()

        resource_url = self._get_url_endpoint(endpoint)

        normalized_string = "{0}\n".format(self.access_token_key)
        normalized_string += "{0}\n".format(timestamp)
        normalized_string += "{0}\n".format(nonce)
        normalized_string += "{0}\n".format(verb)
        normalized_string += "mlkshk.com\n"
        normalized_string += "80\n"
        normalized_string += "{0}\n".format(endpoint)

        digest = hmac.new(
            self.access_token_secret.encode('ascii'),
            normalized_string.encode('ascii'),
            sha1).digest()
        signature = base64.encodestring(digest).strip().decode('utf8')
        auth_str = (
            'MAC token="{0}", '
            'timestamp="{1}", '
            'nonce="{2}", '
            'signature="{3}"').format(
                self.access_token_key,
                str(timestamp),
                nonce,
                signature)
        req = requests.get(
            resource_url,
            headers={'Authorization': auth_str},
            verify=False)

        if req.status_code == 401:
            raise ApiResponseUnauthorized(req)
        elif req.status_code == 404:
            raise NotFound404(req)
        elif req.status_code == 500:
            raise Exception(req)

        try:
            data = req.json()
        except:
            raise Exception(req)
        return data

    @staticmethod
    def get_nonce():
        nonce = md5(
            str(random.SystemRandom().randint(0, 100000000)).encode('utf8')
        ).hexdigest()
        return nonce

    ####################################################################
    # Users
    ####################################################################

    def GetUser(self,
                user_id=None,
                user_name=None):
        """ Get a user object from the API. If no ``user_id`` or ``user_name``
        is specified, it will return the User object for the currently
        authenticated user.

        Args:
            user_id (int): User ID of the user for whom you want to get
                information. [Optional]
            user_name(str): Username for the user for whom you want to get
                information. [Optional]

        Returns:
            A User object.
        """

        if user_id:
            # Return user by user_id
            endpoint = '/api/user_id/{0}'.format(user_id)
        elif user_name:
            # Return user by user_name
            endpoint = '/api/user_name/{0}'.format(user_name)
        else:
            # Return currently authorized user
            endpoint = '/api/user'

        data = self._RequestUrl(verb="GET", endpoint=endpoint)

        try:
            return User.NewFromJSON(data)
        except:
            return data

    ####################################################################
    # Shakes
    ####################################################################

    def GetUserShakes(self,
                      user_id=None,
                      user_name=None):
        """ Get a list of Shake objects for a user. If no ``user_id`` or
        ``user_name`` is specified, then get a list of shakes for the currently
        authenticated user.

        Args:
            user_id (int): User id for which to grab shakes. [Optional]
            user_name (str): Username for which to grab shakes. [Optional]

        Returns:
            A list of Shake objects.
        """
        if user_id:
            endpoint = '/api/user_id/{0}'.format(user_id)
        elif user_name:
            endpoint = '/api/user_name/{0}'.format(user_name)
        else:
            endpoint = '/api/shakes'
        data = self._RequestUrl(verb="GET", endpoint=endpoint)
        shakes = [Shake.NewFromJSON(shk) for shk in data['shakes']]
        return shakes

    def GetShakeSharedFiles(self,
                            shake_id=None):
        endpoint = '/api/shakes/{shake_id}'.format(
            shake_id=shake_id)

        data = self._RequestUrl(verb="GET", endpoint=endpoint)
        return data

    def GetSharedFile(self,
                      sharekey=None):
        endpoint = '/api/sharedfile/{0}'.format(sharekey)
        data = self._RequestUrl('GET', endpoint)
        return SharedFile.NewFromJSON(data)

    def PostSharedFile(self,
                       image_file=None,
                       source_link=None,
                       shake_id=None,
                       title=None,
                       description=None):
        endpoint = '/api/upload'.format(self.base_url)
        pass

    def LikeSharedFile(self,
                       sharekey=None):
        endpoint = '/api/sharedfile/{sharekey}/like'.format(self.base_url)

    def PostComment():
        pass
