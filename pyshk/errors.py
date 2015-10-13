from __future__ import print_function

import re


class ApiResponseUnauthorized(Exception):

    """ Handle errors with authenticating the API instance """

    def __init__(self, response):
        vals = ['status_code', 'headers', 'reason']
        [setattr(self, var, getattr(response, var))
            for var in vars(response) if var in vals]

    def __repr__(self):
        return (
            "Mlkshk Error: {status} {reason}").format(
                status=self.status_code,
                reason=self.reason)

class ApiInstanceUnauthorized(Exception):
    def __init__(self):
        self.reason = ("API Instance is unauthorized. You must provide "
                       "a Consumer Key, Consumer Token, Access Key, and "
                       "Access Secret. You can call get_auth() on your "
                       "API instance to get the access key and secret after "
                       "creating your application on mlkshk.com")
        super(ApiInstanceUnauthorized, self).__init__(self.reason)


class NotFound404(Exception):

    """ Handle errors with 404 Not Found Status Codes """

    def __init__(self, response):
        vals = ['status_code', 'headers', 'reason']
        [setattr(self, var, getattr(response, var))
            for var in vars(response) if var in vals]
        self.url = response.url

    def __repr__(self):
        return (
            "404 Not Found: ({url})").format(
                url=self.url)
