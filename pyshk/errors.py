from __future__ import print_function

import re


def get_api_errors(test_str):
    err_code_search = re.compile(r'error="([\w]*)"')
    err_desc_search = re.compile(r'error_description="(.*)"')
    error_code = re.search(err_code_search, test_str).groups()[0]
    error_description = re.search(err_desc_search, test_str).groups()[0]
    return (error_code, error_description)


class MlkShkError(Exception):

    """ Exceptions from the MLKSHK API """

    def __init__(self, reason):
        self.reason = reason
        print(self.__dict__)
        Exception.__init__(self, reason)

    def __str__(self):
        return "Mlkshk Error: {0}".format(self.reason)


class ApiUnauthorized(MlkShkError):

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


class NotFound404(MlkShkError):

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
