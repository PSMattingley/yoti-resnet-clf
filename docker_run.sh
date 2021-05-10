#!/usr/bin/env bash
docker build -t tf-serving -f Dockerfile-TF .
docker build -t img-class -f Dockerfile-IC .
docker run --name tf-serving-cont -p 8501:8501 -e MODEL_NAME=resnet_v2_fp32_savedmodel_NHWC_jpg tf-serving
docker run --name img-class-cont -p 5000:5000 img-class

