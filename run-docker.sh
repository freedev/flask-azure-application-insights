#!/bin/bash

export DOCKER_BUILDKIT=1
docker build -t faai .
docker run -ti  \
    -e APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=$1" \
    -e GU_THREADS_NUM=1 \
    -e GU_WORK_NUM=3 \
    -p 2222:2222 -p 5000:5000 faai
