import unittest
from pyshk.api import Api


class UtilsTest(unittest.TestCase):

    """ Tests for utility functions """

    def setUp(self):
        self.api = Api(
            consumer_key='test',
            consumer_secret='test',
            access_token_key='test',
            access_token_secret='test')

    def test_image_types(self):
        jpg = self.api._get_image_type('tests/test_data/tiny.jpg')
        self.assertEqual(jpg, 'image/jpeg')

        gif = self.api._get_image_type('tests/test_data/like-tiny.gif')
        self.assertEqual(gif, 'image/gif')

        png = self.api._get_image_type('tests/test_data/tiny.png')
        self.assertEqual(png, 'image/png')
