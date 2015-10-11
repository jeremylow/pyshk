import unittest
import json

import responses

from pyshk.api import Api
from pyshk import models
from pyshk import errors


class ApiTests(unittest.TestCase):

    """ Test various API functions """

    def test_api_creation(self):
        self.assertRaises(errors.ApiInstanceUnauthorized, Api)
        a = Api(consumer_key='test',
                consumer_secret='test',
                access_token_key='test',
                access_token_secret='supersecret')
        self.assertEqual(a.base_url, 'http://mlkshk.com')


class TestAPIResponses(unittest.TestCase):

    def setUp(self):
        self.api = Api(
            consumer_key='test',
            consumer_secret='test',
            access_token_key='test',
            access_token_secret='supersecret')

    @responses.activate
    def test_get_user(self):
        with open('tests/test_data/api/user') as f:
            resp_data = f.read()

            responses.add(
                responses.GET,
                'http://mlkshk.com/api/user',
                body=resp_data,
                status=200)
            user = self.api.get_user()
            print(user.Name)

    @responses.activate
    def test_get_authd_user_shakes(self):
        with open('tests/test_data/api/shakes') as api_shakes:
            resp_data = api_shakes.read()

            responses.add(
                responses.GET,
                'http://mlkshk.com/api/shakes',
                body=resp_data,
                status=200)
            shakes = self.api.get_user_shakes()
            self.assertEqual(len(shakes), 1)

    @responses.activate
    def test_upload(self):
        with open('tests/test_data/api/upload') as upload:
            resp_data = upload.read().encode('utf8')

            responses.add(
                responses.POST,
                'http://mlkshk.com/api/upload',
                body=resp_data,
                status=200
            )
            resp = self.api.post_shared_file(
                image_file='tests/test_data/like-tiny.gif')
        expected_resp = {"share_key": "164L4", "name": "like-tiny.gif"}
        self.assertEqual(resp['share_key'], expected_resp['share_key'])
