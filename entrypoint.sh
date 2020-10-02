#!/bin/bash

echo "threads n. " $GU_THREADS_NUM
echo "processes n. " $GU_WORK_NUM

if [ "$GU_THREADS_NUM" == "" ]
then
  export GU_THREADS_NUM="1"
fi

if [ "$GU_WORK_NUM" == "" ]
then
  export GU_WORK_NUM="10"
fi

/usr/sbin/sshd -D &

echo "threads n. " $GU_THREADS_NUM
echo "processes n. " $GU_WORK_NUM

# threading influenced by https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
GUNICORN_CMD_ARGS="--bind=127.0.0.1 --workers=$GU_WORK_NUM --threads=$GU_THREADS_NUM --preload" gunicorn -b 0.0.0.0:5000 application:app
# python application.py
