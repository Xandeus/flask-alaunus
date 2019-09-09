#!/bin/bash
ssh $RPI "sudo pkill python; sudo PYTHONPATH='.:build/lib.linux-armv7l-2.7' python ~/rpi_ws281x/python/examples/strandtest.py -k"
