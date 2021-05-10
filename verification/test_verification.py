from unittest import TestCase

import requests
import os
import json


class TestVerification(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.predict_url = 'http://localhost:5000/classify/resnet'
        cls.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')

    def test_post_png(self):
        img = os.path.join(self.test_data_dir, 'cat.png')
        response = requests.post(self.predict_url,
                                 files={'image': open(img, 'rb')})
        self.assertEqual(response.status_code, 400)

    def test_post_cat(self):
        img = os.path.join(self.test_data_dir, 'cat.jpg')
        response = requests.post(self.predict_url,
                                 files={'image': open(img, 'rb')})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text)['classes'], 286)

    def test_post_dog(self):
        img = os.path.join(self.test_data_dir, 'dog.jpg')
        response = requests.post(self.predict_url,
                                 files={'image': open(img, 'rb')})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text)['classes'], 261)






