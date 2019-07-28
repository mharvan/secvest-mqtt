#!/bin/bash
#
# Setup python virtual environment
#

python3 -m venv paho-mqtt
source paho-mqtt/bin/activate
pip3 install paho-mqtt bs4 requests

