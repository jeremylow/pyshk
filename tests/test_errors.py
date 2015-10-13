import unittest
import json

import responses

from pyshk.api import Api
from pyshk import models
from pyshk import errors


class ErrorTests(unittest.TestCase):

    """ test that error are raised properly """

    def setUp(self):
        self.api = Api(
            consumer_key='test',
            consumer_secret='test',
            access_token_key='test',
            access_token_secret='supersecret')

    @responses.activate
    def test_api_response_raises_error_401(self):
        responses.add(
            responses.GET,
            'http://mlkshk.com/api/token',
            body=None, status=401)
        self.assertRaises(
            errors.ApiResponseUnauthorized,
            lambda: self.api._make_request(
                'GET', '/api/token'))

    @responses.activate
    def test_api_response_raises_error_404(self):
        responses.add(
            responses.GET,
            'http://mlkshk.com/api/token',
            body=None, status=404)
        self.assertRaises(
            errors.NotFound404,
            lambda: self.api._make_request(
                'GET', '/api/token'))

    @responses.activate
    def test_api_response_raises_error_500(self):
        responses.add(
            responses.GET,
            'http://mlkshk.com/api/token',
            body="Oh no! Server error", status=500)
        self.assertRaises(
            Exception,
            lambda: self.api._make_request(
                'GET', '/api/token'))
