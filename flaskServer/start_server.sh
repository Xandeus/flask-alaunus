#!/bin/bash
. ./venv/bin/activate
export FLASK_APP=js_example
flask run --host=raspberrypi.local &
echo "Server started succesfully"
