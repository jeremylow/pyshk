import datetime
import json
import unittest

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
                     'profile_image_url': 'http://mlkshk.com/static/images/default-icon-venti.png',
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

    def test_json_representation(self):
        self.maxDiff = None
        u = models.User(id=67136, name='jcbl', about='me', shakes=None,
                        profile_image_url='http://example.com',
                        website='http://example.com')
        u_json_str = '{"about": "me", "id": 67136, "mlkshk_url": "https://mlkshk.com/user/jcbl", "name": "jcbl", "profile_image_url": "http://example.com", "shake_count": 0, "website": "http://example.com"}'
        self.assertEqual(u.AsJsonString(), u_json_str)
        self.assertEqual(u.__repr__(), u_json_str)


class TestShake(unittest.TestCase):

    """
    Test Shake objects
    """

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
            self.assertTrue(shake1 != shake2)

    def test_shake_as_dict(self):
        sf = models.SharedFile(sharekey='test', name='test.jpg', title='test',
                               description='test',
                               posted_at='2015-10-09T15:58:11Z',
                               permalink='test', width=500, height=500,
                               views=1, likes=1, saves=1, nsfw=False,
                               comments=0,
                               image_url='http://example.com/test.jpg',
                               source_url='http://example.com/test.jpg',
                               saved=True, liked=True)

        sf_dict = {'sharekey': 'test', 'name': 'test.jpg', 'title': 'test',
                   'description': 'test',
                   'posted_at': datetime.datetime(2015, 10, 9, 15, 58, 11),
                   'permalink': 'test', 'width': 500, 'height': 500,
                   'views': 1, 'likes': 1, 'saves': 1, 'nsfw': False,
                   'comments': 0, 'image_url': 'http://example.com/test.jpg',
                   'source_url': 'http://example.com/test.jpg', 'saved': True,
                   'liked': True}

        self.assertDictEqual(sf.AsDict(), sf_dict)

    def test_shake_json(self):
        u = models.User(id=67136, name='jcbl', about='me', shakes=None,
                        profile_image_url='http://example.com',
                        website='http://example.com')
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
        s_json_str = '{"description": "test", "id": 1, "name": "noone shake", "owner": {"about": "me", "id": 67136, "mlkshk_url": "https://mlkshk.com/user/jcbl", "name": "jcbl", "profile_image_url": "http://example.com", "shake_count": 0, "website": "http://example.com"}, "thumbnail_url": "http://example.com", "type": "user", "url": "http://example.com"}'
        self.assertEqual(s.AsJsonString(), s_json_str)
        self.assertEqual(s.AsJsonString(), s.__repr__())


class TestComment(unittest.TestCase):

    """
    Test Comments object
    """

    def test_comment_creation(self):
        with open('tests/test_data/api/comments') as f:
            data = json.load(f)
        comments = [models.Comment.NewFromJSON(d) for d in data['comments']]

        self.assertEqual(len(comments), 2)
        self.assertIsInstance(comments[0], models.Comment)
        self.assertIsInstance(comments[0].user, models.User)
        self.assertEqual(comments[0].body, 'api test')

    def test_json_str(self):
        self.maxDiff = None
        with open('tests/test_data/api/comments') as f:
            data = json.load(f)
        comment = [models.Comment.NewFromJSON(d) for d in data['comments']][0]
        c_json_string = comment.AsJsonString()

        # This isn't strictly correct since we try to determine the number of
        # Shakes that a user has. This is somewhat unavoidable since the API
        # doesn't return the user's shakes when just looking at a User object
        # from the comment endpoint.
        json_string = '{"body": "api test", "posted_at": "2015-10-16T01:05:54Z", "user": {"id": 67136, "mlkshk_url": "https://mlkshk.com/user/jcbl", "name": "jcbl", "profile_image_url": "http://mlkshk-production.s3.amazonaws.com/account/67136/profile.jpg", "shake_count": 0}}'
        self.assertEqual(c_json_string, json_string)
