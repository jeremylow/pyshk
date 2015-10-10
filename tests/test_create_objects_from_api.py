import unittest
import json

from pyshk import models


class ModelTests(unittest.TestCase):

    """ Test that pyshk creates proper models from API responses """

    def test_create_user_from_api(self):
        with open('tests/test_data/api_resp__user_endpoint.json') as f:
            data = json.load(f)
            u = models.User.NewFromJSON(data)
            self.assertEqual(u.Id, 67136)
            self.assertEqual(len(u.Shakes), 1)
            self.assertEqual(len(u.Shakes), u.ShakeCount)
            self.assertEqual(u.Name, 'jcbl')
            self.assertEqual(
                u.ProfileImageUrl,
                "http://mlkshk.com/static/images/default-icon-venti.png")
            self.assertEqual(u.About, '')
            self.assertEqual(u.Website, '')
            self.assertEqual(u.MlkShkUrl, 'https://mlkshk.com/user/jcbl')

            shk = u.Shakes[0]
            self.assertEqual(shk.Id, 68435)

    def test_create_user_dict(self):
        with open('tests/test_data/api_resp__user_endpoint.json') as f:
            user_dict = {}
            user_dict['name'] = 'jcbl'
            user_dict['mlkshk_url'] = 'https://mlkshk.com/user/jcbl'
            user_dict['id'] = 67136

            tmp_shk = models.Shake()
            tmp_shk.created_at = '2015-04-27T17:22:54Z'
            tmp_shk.description = 'New Shake'
            tmp_shk.id = 68435
            tmp_shk.name = 'jcbl'
            tmp_shk.thumbnail_url = 'http://mlkshk.com/static/images/default-icon-venti.png'
            tmp_shk.type = 'user'
            tmp_shk.updated_at = '2015-04-27T17:22:54Z'
            tmp_shk.url = 'http://mlkshk.com/user/jcbl'

            user_dict['shakes'] = [tmp_shk]
            user_dict['shake_count'] = 1

            user = models.User.NewFromJSON(json.load(f)).AsDict()
            diff = set(user_dict.keys()) - set(user.keys())
            self.assertFalse(diff)

            # Due to equality comparisons of dictionaries, we have to get rid
            # of the nested shake dictionary and compare separately.
            user.pop('shakes', None)
            user_dict.pop('shakes', None)

            self.assertDictEqual(user_dict, user)
