""" Library to provide access to MLKSHK API. """

import base64
import datetime
from hashlib import md5, sha1
import hmac
# import json
# from requests_oauthlib import OAuth2
import imghdr
import os
import random
import requests
import six
import time

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

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
                 base_url=None,
                 testing=False):

        if base_url is None:
            self.base_url = 'http://mlkshk.com'
        else:
            self.base_url = base_url

        self.port = 80
        self.authenticated = False

        if testing:
            self.testing = True

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        auth_list = [consumer_key, consumer_secret,
                     access_token_key, access_token_secret]

        if all(auth_list):
            self.authenticated = True

        # Set headers, client info for requests.
        # default_headers = {'User-Agent': 'PyShk v0.0.1'}
        # self.client_args = {}
        # self.client_args['headers'] = default_headers

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

    def get_auth(self, redirect_uri=None):
        if not redirect_uri:
            redirect_uri = "http://localhost:8000"

        authentication_url = (
            "https://mlkshk.com/api/authorize"
            "?response_type=code&client_id={key}&redirect_uri={uri}").format(
                key=self.consumer_key,
                uri=redirect_uri)

        access_token_url = 'https://mlkshk.com/api/token'

        if not self.testing:
            webbrowser.open(authentication_url, new=1)
            authorization_code = input("Enter the code from the redirected URL: ")
        else:
            authorization_code = 123456

        message = {
            'grant_type': "authorization_code",
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret}

        data = urlencode(message)
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

    def _get_url_endpoint(self, endpoint):
        return self.base_url + endpoint

    def _make_headers(self,
                      verb=None,
                      endpoint=None,
                      nonce=None,
                      timestamp=None):
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

        if six.PY2:
            signature = base64.encodestring(digest).strip().decode('utf8')
        else:
            signature = base64.encodebytes(digest).strip().decode('utf8')

        auth_str = (
            'MAC token="{0}", '
            'timestamp="{1}", '
            'nonce="{2}", '
            'signature="{3}"').format(
            self.access_token_key,
            str(timestamp),
            nonce,
            signature)
        return auth_str

    def _make_request(self, verb, endpoint=None, data=None):
        if not self.authenticated:
            raise ApiInstanceUnauthorized

        resource_url = self._get_url_endpoint(endpoint)

        timestamp = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        nonce = self.get_nonce()

        authorization_header = self._make_headers(
            verb=verb,
            endpoint=endpoint,
            nonce=nonce,
            timestamp=timestamp)

        if verb == "GET":
            req = requests.get(
                resource_url,
                headers={'Authorization': authorization_header},
                verify=False)
        elif verb == "POST":
            req = requests.post(
                resource_url,
                headers={'Authorization': authorization_header},
                files=data)

        if req.status_code == 401:
            raise ApiResponseUnauthorized(req)
        elif req.status_code == 404:
            raise NotFound404(req)
        elif req.status_code == 500:
            raise Exception(req)

        try:
            return req.json()
        except:
            print('returning req')
            return req

    @staticmethod
    def get_nonce():
        nonce = md5(
            str(random.SystemRandom().randint(0, 100000000)).encode('utf8')
        ).hexdigest()
        return nonce

    @staticmethod
    def _get_image_type(image):
        if imghdr.what(image) == 'jpeg':
            return 'image/jpeg'
        elif imghdr.what(image) == 'gif':
            return 'image/gif'

    def get_user(self, user_id=None, user_name=None):
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

        data = self._make_request(verb="GET", endpoint=endpoint)

        try:
            return User.NewFromJSON(data)
        except:
            return data

    def get_user_shakes(self, user_id=None, user_name=None):
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
        data = self._make_request(verb="GET", endpoint=endpoint)
        shakes = [Shake.NewFromJSON(shk) for shk in data['shakes']]
        return shakes

    def get_shared_files_from_shake(self, shake_id=None):
        """
        Returns a list of SharedFile objects from a particular shake.

        Args:
            shake_id (int): Shake from which to get a list of SharedFiles

        Returns:
            List (list) of SharedFiles.
        """
        if not shake_id:
            shake_id = ''
        else:
            shake_id = '/' + str(shake_id)

        endpoint = '/api/shakes{shake_id}'.format(
            shake_id=shake_id)

        data = self._make_request(verb="GET", endpoint=endpoint)
        return [SharedFile.NewFromJSON(f) for f in data['sharedfiles']]

    def get_shared_file(self, sharekey=None):
        endpoint = '/api/sharedfile/{0}'.format(sharekey)
        data = self._make_request('GET', endpoint)
        return SharedFile.NewFromJSON(data)

    def post_shared_file(self,
                         image_file=None,
                         source_link=None,
                         shake_id=None,
                         title=None,
                         description=None):
        """ Upload an image.

        TODO:
        Don't have a pro account to test (or even write) code to upload a
        shared filed to a particular shake.

        Args:
            image_file (str): path to an image (jpg/gif) on your computer.
            source_link (str): URL of a source (youtube/vine/etc.)
            shake_id (int): shake to which to upload the file or
                source_link [optional]
            title (str): title of the SharedFile [optional]
            description (str): description of the SharedFile

        Returns:
            SharedFile key.
        """
        if image_file and source_link:
            raise Exception('You can only specify an image file or '
                            'a source link, not both.')
        if not image_file and not source_link:
            raise Exception('You must specify an image file or a source link')

        content_type = self._get_image_type(image_file)

        if not title:
            title = os.path.basename(image_file)

        f = open(image_file, 'rb')
        endpoint = '/api/upload'

        files = {'file': (title, f, content_type)}
        data = self._make_request('POST', endpoint=endpoint, data=files)

        f.close()
        return data

    def like_shared_file(self, sharekey=None):
        """ 'Like' a SharedFile. mlkshk doesn't allow you to unlike a
        sharedfile, so this is ~~permanent~~.

        Args:
            sharekey (str): Sharekey for the file you want to 'like'.

        Returns:
            Either a SharedFile on success, or an exception on error.
        """
        endpoint = '/api/sharedfile/{sharekey}/like'.format(sharekey=sharekey)
        data = self._make_request("POST", endpoint=endpoint, data=None)

        # return data

        try:
            sf = SharedFile.NewFromJSON(data)
            sf.liked = True
            return sf
        except:
            raise Exception("{0}".format(data['error']))

    def get_comments_on_shared_file(self, sharekey=None):
        pass


    def post_comment(self, comment=None):
        pass
