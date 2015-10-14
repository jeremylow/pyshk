import unittest
import json

from pyshk import models


class ModelTests(unittest.TestCase):

    """ Test that pyshk creates proper models from API responses """

    def test_create_user_from_api(self):
        with open('tests/test_data/api/user') as f:
            data = json.load(f)
        u = models.User.NewFromJSON(data)
        self.assertEqual(u.id, 67136)
        self.assertEqual(len(u.shakes), 1)
        self.assertEqual(len(u.shakes), u.shake_count)
        self.assertEqual(u.name, 'jcbl')
        self.assertEqual(
            u.profile_image_url,
            "http://mlkshk.com/static/images/default-icon-venti.png")
        self.assertEqual(u.about, '')
        self.assertEqual(u.website, '')
        self.assertEqual(u.mlkshk_url, 'https://mlkshk.com/user/jcbl')

        shk = u.shakes[0]
        self.assertEqual(shk.id, 68435)

    def test_create_user_dict(self):
        with open('tests/test_data/api/user') as f:
            user = models.User.NewFromJSON(json.load(f)).AsDict()
        tmp_shk = models.Shake(
            created_at='2015-04-27T17:22:54Z',
            description='New Shake',
            id=68435,
            name='jcbl',
            thumbnail_url=('http://mlkshk.com'
                           '/static/images/default-icon-venti.png'),
            type='user',
            updated_at='2015-04-27T17:22:54Z',
            url='http://mlkshk.com/user/jcbl')

        user_dict = {'name': 'jcbl',
                     'mlkshk_url': 'https://mlkshk.com/user/jcbl',
                     'id': 67136,
                     'shakes': [tmp_shk],
                     'shake_count': 1}

        diff = set(user_dict.keys()) - set(user.keys())
        self.assertFalse(diff)

        # Due to equality comparisons of dictionaries, we have to get rid
        # of the nested shake dictionary and compare separately.
        user.pop('shakes', None)
        user_dict.pop('shakes', None)

        self.assertDictEqual(user_dict, user)

    def test_user_equality(self):
        with open('tests/test_data/api/user') as f:
            u1 = models.User.NewFromJSON(json.load(f))
            f.seek(0)
            u2 = models.User.NewFromJSON(json.load(f))

            self.assertTrue(u1 == u2)

    def test_shake_equality(self):
        with open('tests/test_data/api/shakes') as f:
            shake1 = models.Shake.NewFromJSON(json.load(f))
            f.seek(0)
            shake2 = models.Shake.NewFromJSON(json.load(f))

            self.assertTrue(shake1 == shake2)
            shake1.id = 2
            self.assertFalse(shake1 == shake2)
            delattr(shake1, 'id')
            self.assertFalse(shake1 == shake2)

    def test_json_representation(self):
        u = models.User(
            id=67136,
            name='jcbl',
            profile_image_url='http://example.com',
            about='me', website='http://example.com',
            shakes=None)
        u_json_str = (
            '{"about": "me", "id": 67136, '
            '"mlkshk_url": "https://mlkshk.com/user/jcbl", '
            '"name": "jcbl", "shake_count": 0, '
            '"website": "http://example.com"}')
        self.assertEqual(u.AsJsonString(), u_json_str)
        self.assertEqual(u.__repr__(), u_json_str)
        s = models.Shake(
            id=1,
            name='noone shake',
            owner=u,
            url='http://example.com',
            thumbnail_url='http://example.com',
            description='test',
            type='user',
            created_at=None,
            updated_at=None
        )
        s_json_str = (
            '{"description": "test", "id": 1, "name": "noone shake", '
            '"owner": {"about": "me", "id": 67136, "mlkshk_url": '
            '"https://mlkshk.com/user/jcbl", "name": "jcbl", "shake_count": '
            '0, "website": "http://example.com"}, "thumbnail_url": '
            '"http://example.com", "type": "user", "url": "http://example.com"}'

        )
        self.assertEqual(s.AsJsonString(), s_json_str)
        self.assertEqual(s.AsJsonString(), s.__repr__())

    def test_shake_as_dict(self):
        sf = models.SharedFile(
            sharekey='test',
            name='test.jpg',
            title='test',
            description='test',
            posted_at='test',
            permalink='test',
            width=500,
            height=500,
            views=1,
            likes=1,
            saves=1,
            nsfw=False,
            comments=0,
            image_url='http://example.com/test.jpg',
            source_url='http://example.com/test.jpg',
            saved=True,
            liked=True,
        )

        sf_dict = {
            'sharekey': 'test',
            'name': 'test.jpg',
            'title': 'test',
            'description': 'test',
            'posted_at': 'test',
            'permalink': 'test',
            'width': 500,
            'height': 500,
            'views': 1,
            'likes': 1,
            'saves': 1,
            'nsfw': False,
            'comments': 0,
            'image_url': 'http://example.com/test.jpg',
            'source_url': 'http://example.com/test.jpg',
            'saved': True,
            'liked': True,
        }

        self.assertDictEqual(sf.AsDict(), sf_dict)
