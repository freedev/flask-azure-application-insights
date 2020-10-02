#!/bin/bash

virtualenv  .direnv -p python3
source .direnv/bin/activate
pip install -r requirements.txt
