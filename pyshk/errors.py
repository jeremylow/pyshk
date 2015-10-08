from __future__ import print_function

import re


def get_api_errors(test_str):
    err_code_search = re.compile(r'error="([\w]*)"')
    err_desc_search = re.compile(r'error_description="(.*)"')
    error_code = re.search(err_code_search, test_str).groups()[0]
    error_description = re.search(err_desc_search, test_str).groups()[0]
    return (error_code, error_description)


class ApiResponseUnauthorized(Exception):

    """ Handle errors with authenticating the API instance """

    def __init__(self, response):
        vals = ['status_code', 'headers', 'reason']
        [setattr(self, var, getattr(response, var))
            for var in vars(response) if var in vals]
        www = self.headers['www-authenticate']
        self.error_code, self.error_description = get_api_errors(www)

    def __str__(self):
        return (
            "Mlkshk Error: {status} {reason} "
            "(Error code: {errcode}: {errdesc})").format(
                status=self.status_code,
                reason=self.reason,
                errcode=self.error_code,
                errdesc=self.error_description)


class ApiInstanceUnauthorized(Exception):
    def __init__(self):
        self.reason = ("API Instance is unauthorized. You must provide "
                       "a Consumer Key, Consumer Token, Access Key, and "
                       "Access Secret. You can call DoAuthDance() on your "
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

    def __str__(self):
        return (
            "404 Not Found: ({url})").format(
                url=self.url)
