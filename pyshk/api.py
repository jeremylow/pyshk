# -*- coding: utf-8 -*-


""" Library to provide access to MLKSHK API. """

import base64
import datetime
from hashlib import md5, sha1
import hmac
import imghdr
import os
import random
import requests
import requests_toolbelt
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

        self.testing = False
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

    def _make_request(self, verb, endpoint=None, data=None, files=None):
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
            if data:
                req = requests.post(
                    resource_url,
                    headers={'Authorization': authorization_header},
                    data=data)
            elif files:
                req = requests.post(
                    resource_url,
                    headers={'Authorization': authorization_header},
                    files=files)
            elif data and files:
                req = requests.post(
                    resource_url,
                    headers={'Authorization': authorization_header},
                    files=files,
                    data=data)
            else:
                req = requests.post(
                    resource_url,
                    headers={'Authorization': authorization_header})

        if req.status_code == 401:
            raise ApiResponseUnauthorized(req)
        elif req.status_code == 404:
            raise NotFound404(req)
        elif req.status_code == 500:
            raise Exception(req)

        if self.testing:
            return req

        try:
            return req.json()
        except:
            print('returning req', req._content)
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
        elif imghdr.what(image) == 'png':
            return 'image/png'

    def get_favorites(self, before=None, after=None):
        """
        Get a list of the authenticated user's 10 most recent favorites
        (likes).

        Args:
            before (str): get 10 SharedFile objects before (but not including)
                the SharedFile given by `before` for the authenticated user's
                set of Likes.
            after (str): get 10 SharedFile objects after (but not including)
                the SharedFile give by `after' for the authenticated user's set
                of Likes.

        Returns:
            List of SharedFile objects.
        """
        if before and after:
            raise Exception("You cannot specify both before and after keys")

        endpoint = '/api/favorites'

        if before:
            endpoint += '/before/{0}'.format(before)
        elif after:
            endpoint += '/after/{0}'.format(after)

        data = self._make_request("GET", endpoint=endpoint)
        return [SharedFile.NewFromJSON(sf) for sf in data['favorites']]

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
            endpoint = '/api/user_id/{0}'.format(user_id)
        elif user_name:
            endpoint = '/api/user_name/{0}'.format(user_name)
        else:
            # Return currently authorized user
            endpoint = '/api/user'

        data = self._make_request(verb="GET", endpoint=endpoint)

        try:
            return User.NewFromJSON(data)
        except:
            return data

    def get_user_shakes(self):
        """ Get a list of Shake objects for the currently authenticated user.

        Returns:
            A list of Shake objects.
        """
        endpoint = '/api/shakes'
        data = self._make_request(verb="GET", endpoint=endpoint)

        shakes = [Shake.NewFromJSON(shk) for shk in data['shakes']]
        return shakes

    def get_shared_files_from_shake(self,
                                    shake_id=None,
                                    before=None,
                                    after=None):
        """
        Returns a list of SharedFile objects from a particular shake.

        Args:
            shake_id (int): Shake from which to get a list of SharedFiles
            before (str): get 10 SharedFile objects before (but not including)
                the SharedFile given by `before` for the given Shake.
            after (str): get 10 SharedFile objects after (but not including)
                the SharedFile give by `after' for the given Shake.

        Returns:
            List (list) of SharedFiles.
        """
        if before and after:
            raise Exception("You cannot specify both before and after keys")

        endpoint = '/api/shakes'

        if shake_id:
            endpoint += '/{0}'.format(shake_id)

        if before:
            endpoint += '/before/{0}'.format(before)
        elif after:
            endpoint += '/after/{0}'.format(after)

        data = self._make_request(verb="GET", endpoint=endpoint)
        return [SharedFile.NewFromJSON(f) for f in data['sharedfiles']]

    def get_shared_file(self, sharekey=None):
        """
        Returns a SharedFile object given by the sharekey.

        Args:
            sharekey (str): Sharekey of the SharedFile you want to retrieve.

        Returns:
            SharedFile
        """
        if not sharekey:
            raise Exception("You must specify a sharekey.")
        endpoint = '/api/sharedfile/{0}'.format(sharekey)
        data = self._make_request('GET', endpoint)
        return SharedFile.NewFromJSON(data)

    def like_shared_file(self, sharekey=None):
        """ 'Like' a SharedFile. mlkshk doesn't allow you to unlike a
        sharedfile, so this is ~~permanent~~.

        Args:
            sharekey (str): Sharekey for the file you want to 'like'.

        Returns:
            Either a SharedFile on success, or an exception on error.
        """

        if not sharekey:
            raise Exception(
                "You must specify a sharekey of the file you"
                "want to 'like'.")

        endpoint = '/api/sharedfile/{sharekey}/like'.format(sharekey=sharekey)
        data = self._make_request("POST", endpoint=endpoint, data=None)

        try:
            sf = SharedFile.NewFromJSON(data)
            sf.liked = True
            return sf
        except:
            raise Exception("{0}".format(data['error']))

    def save_shared_file(self, sharekey=None):
        """
        Save a SharedFile to your Shake.

        Args:
            sharekey (str): Sharekey for the file to save.

        Returns:
            SharedFile saved to your shake.
        """
        endpoint = '/api/sharedfile/{sharekey}/save'.format(sharekey=sharekey)
        data = self._make_request("POST", endpoint=endpoint, data=None)

        try:
            sf = SharedFile.NewFromJSON(data)
            sf.saved = True
            return sf
        except:
            raise Exception("{0}".format(data['error']))

    def get_friends_shake(self, before=None, after=None):
        """
        Contrary to the endpoint naming, this resource is for a list of
        SharedFiles from your friends on mlkshk.

        Returns:
            List of SharedFiles.
        """
        if before and after:
            raise Exception("You cannot specify both before and after keys")

        endpoint = '/api/friends'

        if before:
            endpoint += '/before/{0}'.format(before)
        elif after:
            endpoint += '/after/{0}'.format(after)

        data = self._make_request("GET", endpoint=endpoint)
        return [SharedFile.NewFromJSON(sf) for sf in data['friend_shake']]

    def get_incoming_shake(self, before=None, after=None):
        """
        Returns a list of the most recent SharedFiles on mlkshk.com

        Args:
            before (str): get 10 SharedFile objects before (but not including)
                the SharedFile given by `before` for the Incoming Shake.
            after (str): get 10 SharedFile objects after (but not including)
                the SharedFile give by `after' for the Incoming Shake.

        Returns:
            List of SharedFile objects.
        """
        if before and after:
            raise Exception("You cannot specify both before and after keys")

        endpoint = '/api/incoming'

        if before:
            endpoint += '/before/{0}'.format(before)
        elif after:
            endpoint += '/after/{0}'.format(after)

        data = self._make_request("GET", endpoint=endpoint)
        return [SharedFile.NewFromJSON(sf) for sf in data['incoming']]

    def get_magic_shake(self, before=None, after=None):
        """
        From the API:

        Returns the 10 most recent files accepted by the 'magic' file selection
        algorithm. Currently any files with 10 or more likes are magic.

        Returns:
            List of SharedFile objects
        """
        if before and after:
            raise Exception("You cannot specify both before and after keys")

        endpoint = '/api/magicfiles'

        if before:
            endpoint += '/before/{key}'.format(key=before)
        elif after:
            endpoint += '/after/{key}'.format(key=after)

        data = self._make_request("GET", endpoint=endpoint)
        return [SharedFile.NewFromJSON(sf) for sf in data['magicfiles']]

    def get_comments(self, sharekey=None):
        """
        Retrieve comments on a SharedFile

        Args:
            sharekey (str): Sharekey for the file from which you want to return
                the set of comments.

        Returns:
            List of Comment objects.
        """
        if not sharekey:
            raise Exception(
                "You must specify a sharekey of the file you"
                "want to 'like'.")

        endpoint = '/api/sharedfile/{0}/comments'.format(sharekey)

        data = self._make_request("GET", endpoint=endpoint)

        return [Comment.NewFromJSON(c) for c in data['comments']]

    def post_comment(self, sharekey=None, comment=None):
        """
        Post a comment on behalf of the current user to the
        SharedFile with the given sharekey.

        Args:
            sharekey (str): Sharekey of the SharedFile to which you'd like
                to post a comment.
            comment (str): Text of the comment to post.

        Returns:
            Comment object.
        """
        endpoint = '/api/sharedfile/{0}/comments'.format(sharekey)

        post_data = {'body': comment}

        data = self._make_request("POST", endpoint=endpoint, data=post_data)
        return Comment.NewFromJSON(data)

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
        data = self._make_request('POST', endpoint=endpoint, files=files)

        f.close()
        return data

    def update_shared_file(self,
                           sharekey=None,
                           title=None,
                           description=None):
        """
        Update the editable details (just the title and description) of a
        SharedFile.

        Args:
            sharekey (str): Sharekey of the SharedFile to update.
            title (Optional[str]): Title of the SharedFile.
            description (Optional[str]): Description of the SharedFile

        Returns:
            SharedFile on success, 404 on Sharekey not found, 403 on
            unauthorized.
        """
        if not sharekey:
            raise Exception(
                "You must specify a sharekey for the sharedfile"
                "you wish to update.")

        if not (title or description):
            raise Exception("You must specify a title or description.")

        post_data = {}

        if title:
            post_data['title'] = title
        if description:
            post_data['description'] = description

        endpoint = '/api/sharedfile/{0}'.format(sharekey)

        data = self._make_request('POST', endpoint=endpoint, data=post_data)

        return SharedFile.NewFromJSON(data)
