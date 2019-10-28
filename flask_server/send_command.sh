#!/bin/bash
sudo pkill -f led_control.py
sudo PYTHONPATH='.:build/lib.linux-armv7l-2.7' python ~/alaunus/led_control.py &
