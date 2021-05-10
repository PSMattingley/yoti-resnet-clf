from unittest import TestCase

from app.main import get_model_predict_url, retrieve_predictions


class TestUtilFuncs(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_predict_url(self):
        exp_url = 'http://localhost:8501/v1/models/test:predict'
        self.assertEqual(get_model_predict_url('test'), exp_url)

    def test_retrieve_predictions(self):
        # TODO add unit test
        pass




