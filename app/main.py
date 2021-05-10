from flask import Flask, Response, request
import requests
import base64
import json
import logging

"""
Image Classification Service 

Uses Python-Flask to accept request from client containing jpeg format image data.
Image data is passed to the TensorFlow model service to return the predicted class of the image.

Supported Models:
    - resnet_v2_fp32_savedmodel_NHWC_jpg (/classify/resnet)

Deployment is limited to localhost on Port 5000 for testing.
"""

app = Flask(__name__)

# Initialize logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

TF_SERVICE_URL = 'http://localhost'
PORT = 8501


@app.route('/')
def index():
    return "This is the API for the Image Classification Service"


@app.route('/classify/resnet', methods=['POST'])
def classify_resnet():
    """
    Expects POST containing jpg format image data

    Example Usage: curl -F "image=@test.jpg" -X POST http://localhost:5000/classify/resnet

    :return: Flask response containing the predicted ResNet class for the image [1-1000]
    """

    # Define model to use for this route
    model = 'resnet_v2_fp32_savedmodel_NHWC_jpg'
    supported_formats = ['jpg', 'jpeg']
    logger.info(f'Making prediction on route /classify/resnet using model: {model}')
    model_url = get_model_predict_url(model)

    # Extract file data from request
    try:
        image_file = request.files['image']
    except KeyError:
        msg = 'Could not load image from request. Check payload contains "image" with a valid jpg image assigned.'
        logger.error(msg)
        return Response(status=400, response=json.dumps({'Error': msg}))

    if image_file.filename.split('.')[-1].lower() not in supported_formats:
        msg = f'Image is not in supported formats for this model: {supported_formats}'
        logger.error(msg)
        return Response(status=400, response=json.dumps({'Error': msg}))
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Convert image data to required format and retrieve prediction
    try:
        prediction = retrieve_predictions(image_data, model_url)
    except:
        msg = 'Model failed to make predictions for given image. Check tf prediction services are up and healthy.'
        logger.error(msg)
        return Response(status=500, response=json.dumps({'Error': msg}))

    # If model is successful return predictions
    return Response(status=200, response=json.dumps({'classes': prediction['classes']}))


def get_model_predict_url(model_name):
    """
    Builds model URL given the model name and base URL of the deployed tensorflow service

    :param model_name: Name of the deployed model in the TF service

    :return: URL to request for TF model predictions
    """
    predict_url = f'{TF_SERVICE_URL}:{PORT}/v1/models/{model_name}:predict'
    logger.info(f'Making call to tf-serving predict endpoint at {predict_url}')
    return predict_url


def retrieve_predictions(image_data, model_url):
    """
    Uses converted image data to send a request to the TF model URL and retrieve predictions

    :param image_data: Image file data in required model format e.g. jpeg-bytes
    :param model_url: TF model service URL to retrieve predictions from

    :return: Predictions dictionary containing probability for each model class and predicted class
    """
    predict_request = '{"instances" : [{"b64": "%s"}]}' % image_data
    response = requests.post(model_url, data=predict_request)
    response.raise_for_status()
    prediction = response.json()['predictions'][0]
    pred_class = prediction['classes']
    logger.info(f'Successfully retrieved predictions from model URL: {pred_class}')
    return prediction


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

