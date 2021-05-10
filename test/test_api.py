from unittest import TestCase

from app.main import app


class TestRoutes(TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()
        cls.endpoint = '/classify/resnet'

    def test_invalid_method(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 405)

    def test_image_not_supplied(self):
        response = self.client.post(self.endpoint, data={})
        self.assertEqual(response.status_code, 400)

    def test_valid_post(self):
        # TODO add mocked data
        pass
