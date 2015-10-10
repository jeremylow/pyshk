import unittest
import json

from pyshk import models


class ModelTests(unittest.TestCase):
    """ test that pyshk creates proper models from API responses """

    def test_create_user_from_api(self):
        with open('tests/test_data/api_resp__user_endpoint.json') as f:
            data = json.load(f)
            u = models.User.NewFromJSON(data)
            self.assertEqual(u.Id, 67136)
            self.assertEqual(len(u.Shakes), 1)

            shk = u.Shakes[0]
            self.assertEqual(shk.Id, 68435)

