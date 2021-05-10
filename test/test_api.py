from unittest import TestCase
import os

from app.main import app


class TestRoutes(TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()
        cls.endpoint = '/classify/resnet'
        cls.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')

    def test_invalid_method(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 405)

    def test_image_not_supplied(self):
        response = self.client.post(self.endpoint, data={})
        self.assertEqual(response.status_code, 400)

