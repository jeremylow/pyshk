import unittest
import json

import responses

from pyshk.api import Api
from pyshk import models
from pyshk import errors


class ApiTests(unittest.TestCase):

    """ Test various API functions """

    def test_api_creation(self):
        a = Api(consumer_key='test',
                consumer_secret='test',
                access_token_key='test',
                access_token_secret='supersecret')
        self.assertEqual(a.base_url, 'http://mlkshk.com')
        a = Api(base_url='http://example.com')
        self.assertEqual(a.base_url, 'http://example.com')

    def test_api_unauthorized(self):
        a = Api(consumer_key='test', consumer_secret='test')
        self.assertRaises(errors.ApiInstanceUnauthorized, a.get_user)

    # @responses.activate
    # def test_api_auth(self):
    #     auth_url = (
    #         'https://mlkshk.com/api/authorize?response_type='
    #         'code&client_id=test&redirect_uri=http://localhost:8000')

    #     with open('tests/test_data/api/authorize') as f:
    #         resp_data = f.read()
    #         responses.add(
    #             responses.POST,
    #             auth_url,
    #             body=resp_data,
    #             status_code=200)

    #         a = Api(
    #             consumer_key='test',
    #             consumer_key='test',
    #             redirect_uri='http://localhost:8000')
    #         req = a.get_auth()


class TestAPIResponses(unittest.TestCase):

    def setUp(self):
        self.api = Api(
            consumer_key='test',
            consumer_secret='test',
            access_token_key='test',
            access_token_secret='test')

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
        self.assertEqual(user.name, 'jcbl')

        # By user_id
        with open('tests/test_data/api/user_id/67136') as f:
            resp_data = f.read()

            responses.add(
                responses.GET,
                'http://mlkshk.com/api/user_id/67136',
                body=resp_data,
                status=200)
            user = self.api.get_user(user_id=67136)
        self.assertEqual(user.name, 'jcbl')

        # By user_name
        with open('tests/test_data/api/user_name/jcbl') as f:
            resp_data = f.read()

            responses.add(
                responses.GET,
                'http://mlkshk.com/api/user_name/jcbl',
                body=resp_data,
                status=200)
            user = self.api.get_user(user_name='jcbl')
        self.assertEqual(user.name, 'jcbl')

    @responses.activate
    def test_get_authd_user_shakes(self):
        with open('tests/test_data/api/shakes') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/shakes',
            body=resp_data,
            status=200)
        shakes = self.api.get_user_shakes()
        self.assertEqual(len(shakes), 1)

    @responses.activate
    def test_get_sharedfiles_from_shake(self):
        with open('tests/test_data/api/shakes.59884') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/shakes/59884',
            body=resp_data,
            status=200)
        files = self.api.get_shared_files_from_shake(shake_id=59884)
        self.assertEqual(len(files), 10)

        with open('tests/test_data/api/sharedfile/16509') as f:
            sharedfile = models.SharedFile.NewFromJSON(json.load(f))

        self.assertTrue(sharedfile == files[0])

        self.assertRaises(
            Exception,
            lambda: self.api.get_shared_files_from_shake(
                before='0001', after='0002'))

    @responses.activate
    def test_post_shared_file(self):
        with open('tests/test_data/api/upload') as f:
            resp_data = f.read().encode('utf8')

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
        self.assertRaises(
            Exception,
            lambda: self.api.post_shared_file(
                image_file='1.jpg',
                source_link='http://example.com'))

    def test_headers(self):
        test_headers = self.api._make_headers(
            nonce='bcbd15da3e38847ebad5655231912ac8',
            timestamp=1444770686)
        std_headers = (
            'MAC token="test", timestamp="1444770686", '
            'nonce="bcbd15da3e38847ebad5655231912ac8", '
            'signature="vdjjGj07papwf0H28Nkc3SbWuUQ="')
        self.assertEqual(test_headers, std_headers)

    @responses.activate
    def test_get_shared_file(self):
        with open('tests/test_data/api/sharedfile/164DW') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/sharedfile/164DW',
            body=resp_data,
            status=200
        )
        sf = self.api.get_shared_file(sharekey='164DW')
        sf.user = None
        sf2 = models.SharedFile(
            comments=0,
            pivot_id="164DW",
            title="Shakeys",
            name="tumblr_ntg61qKrOe1rtr67io1_500.jpg",
            posted_at="2015-10-10T15:14:30Z",
            like=False,
            saved=False,
            permalink_page="http://mlkshk.com/p/164DW",
            nsfw=False,
            height=645,
            likes=1,
            description=None,
            sharekey="164DW",
            original_image_url="http://s.mlkshk.com/r/164DW",
            saves=0,
            width=500,
            views=0)
        self.assertTrue(sf == sf2)

    @responses.activate
    def test_like_shared_file(self):
        with open('tests/test_data/api/sharedfile/164DW') as f:
            resp_data = f.read()

        responses.add(
            responses.POST,
            'http://mlkshk.com/api/sharedfile/164DW/like',
            body=resp_data,
            status=200)
        sf = self.api.like_shared_file(sharekey='164DW')

        self.assertTrue(sf.liked)
        self.assertRaises(Exception, lambda: self.api.like_shared_file())

    @responses.activate
    def test_save_shared_file(self):
        with open('tests/test_data/api/sharedfile/165PZ/save') as f:
            resp_data = f.read()

        responses.add(
            responses.POST,
            'http://mlkshk.com/api/sharedfile/165PZ/save',
            body=resp_data,
            status=200)

        sf = self.api.save_shared_file(sharekey='165PZ')
        self.assertTrue(sf.saved)
        self.assertEqual(sf.user.id, 14430)

    @responses.activate
    def test_get_favorites(self):
        with open('tests/test_data/api/favorites') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/favorites',
            body=resp_data,
            status=200)
        favs = self.api.get_favorites()

        self.assertEqual(len(favs), 10)
        self.assertIsInstance(favs[0], models.SharedFile)

    @responses.activate
    def test_get_friends_shake(self):
        with open('tests/test_data/api/friends') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/friends',
            body=resp_data,
            status=200
        )
        friends_shake = self.api.get_friends_shake()
        self.assertIsInstance(friends_shake[0], models.SharedFile)
        self.assertIsInstance(friends_shake, list)
        self.assertRaises(
            Exception,
            lambda: self.api.get_friends_shake(
                before='0001', after='0002'))

    @responses.activate
    def test_get_incoming_shake(self):
        with open('tests/test_data/api/incoming') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/incoming',
            body=resp_data,
            status=200
        )
        incoming_shake = self.api.get_incoming_shake()
        self.assertIsInstance(incoming_shake[0], models.SharedFile)
        self.assertIsInstance(incoming_shake, list)

    @responses.activate
    def test_get_magic_files(self):
        with open('tests/test_data/api/magicfiles') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/magicfiles',
            body=resp_data,
            status=200
        )
        magic_files = self.api.get_magic_shake()
        self.assertIsInstance(magic_files[0], models.SharedFile)
        self.assertIsInstance(magic_files, list)

    @responses.activate
    def test_get_magic_files_after(self):
        with open('tests/test_data/api/magicfiles.after') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/magicfiles/after/1643X',
            body=resp_data,
            status=200
        )
        magic_files = self.api.get_magic_shake(after='1643X')
        self.assertIsInstance(magic_files[0], models.SharedFile)
        self.assertEqual(magic_files[0].sharekey, 'CO04')
        self.assertIsInstance(magic_files, list)
        self.assertEqual(len(magic_files), 10)

    @responses.activate
    def test_get_magic_files_before(self):
        with open('tests/test_data/api/magicfiles.before') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/magicfiles/before/1643X',
            body=resp_data,
            status=200
        )
        magic_files = self.api.get_magic_shake(before='1643X')
        self.assertIsInstance(magic_files[0], models.SharedFile)
        self.assertEqual(magic_files[0].sharekey, 'CO0E')
        self.assertIsInstance(magic_files, list)
        self.assertEqual(len(magic_files), 10)

    @responses.activate
    def test_get_user_shakes(self):
        with open('tests/test_data/api/shakes') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/shakes',
            body=resp_data,
            status=200
        )
        shakes = self.api.get_user_shakes()
        self.assertIsInstance(shakes[0], models.Shake)
        self.assertIsInstance(shakes[0].owner, models.User)
        self.assertEqual(len(shakes), 1)

    @responses.activate
    def test_update_shared_file(self):
        with open('tests/test_data/api/sharedfile/1669X.POST') as f:
            resp_data = f.read()

        responses.add(
            responses.POST,
            'http://mlkshk.com/api/sharedfile/1669X',
            body=resp_data,
            status=200
        )

        sf = self.api.update_shared_file(sharekey='1669X', description='test')

        self.assertIsInstance(sf, models.SharedFile)
        self.assertEqual(sf.description, 'test')

        with open('tests/test_data/api/sharedfile/1669X.POST.title') as f:
            resp_data = f.read()

        responses.add(
            responses.POST,
            'http://mlkshk.com/api/sharedfile/1669X',
            body=resp_data,
            status=200
        )
        sf = self.api.update_shared_file(sharekey='1669X',
                                         title='journalism')
        self.assertIsInstance(sf, models.SharedFile)
        self.assertEqual(sf.title, 'journalism')

        self.assertRaises(
            Exception,
            lambda: self.api.update_shared_file(sharekey='1669X'))
        self.assertRaises(
            Exception,
            lambda: self.api.update_shared_file())

    @responses.activate
    def test_get_comments(self):
        with open('tests/test_data/api/sharedfile/162LG/comments') as f:
            resp_data = f.read()

        responses.add(
            responses.GET,
            'http://mlkshk.com/api/sharedfile/162LG/comments',
            body=resp_data,
            status=200
        )
        comments = self.api.get_comments(sharekey='162LG')
        self.assertEqual(len(comments), 4)
        self.assertIsInstance(comments[0], models.Comment)
        self.assertEqual(comments[0].body, '!!!!!!!')
        self.assertRaises(Exception,
                          lambda: self.api.get_comments())
