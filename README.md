# Resnet Image Classifier (yoti-resnet-clf)

## Overview 

Implementation of Resnet v2 with tensorflow/serving for jpeg image classification.
See Specification.pdf for full description.

## Services

This image classifier is comprised of two services:

### TensorFlow Serving 

A tensorflow/serving service with a pre-built resnet image classifier model attached 
(models/resnet_v2_fp32_savedmodel_NHWC_jpg). 

This accepts input of image data and returns the probability of the image belonging to 
each Resnet class (1-1000) as well as the class with the highest probability.

### Image Classifier 

The main image classifier service is a Python-Flask application that accepts requests 
containing attached jpeg files. The jpeg image is then converted to byte data and passed
to the tf-serving service to retrieve the classification.
  
## Deployment 

The local **docker-compose.yml** file can be used to bring up both services in a local 
network using:

- docker-compose -d up

This will take a short will to initialise as both services will automatically be built from 
Dockerfile (**Dockerfile-TF** and **Dockerfile-IC**), if local images do not exist, and then started.

**docker-compose-test.yml** file can be used to run unit tests against the services:

- docker-compose -f docker-compose-test.yml up  

**docker_run.sh** contains commands to build and run the services individually if required.


## Usage, Testing and Verification

When the service is live an endpoint will be available on localhost to POST images for 
classification to:

- http://localhost:5000/classify/resnet

Test data is provided at **verification/test_data**. The provided images can be sent manually
using Curl, Postman or similar tool with request format:

- curl -F "image=@cat.jpg" -X POST http://localhost:5000/classify/resnet

To receive response in format:

- {"classes": 286}

Verification tests can also be executing the following command from the project directory:

- python -m pytest verification


 
## Further work

Suggested further work if service were to be fully implemented:

- Provide full set of verification test data for this version
- Bulk up unit tests
- Create .env file or similar to contain service configuration (simplify docker-compose)
- Add more error/case handling when parsing request  
- Move deployment from localhost 
- Add healthcheck endpoint that can be queried to test if service is up
- Add list of supported models at /classify
- Add Swagger / Sphinx documentation 
- Add more models and routes in flask app
- Consider moving models to file system and attach to tf-serving via mount/volume.
 