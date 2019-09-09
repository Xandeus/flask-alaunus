#!/usr/bin/env python

import os
import socket
import sys
import time
import fileinput

pi_ip = os.environ["PI_IP"]
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((pi_ip, 8268))

for line in fileinput.input():
    print(line)
    client_socket.send(line.encode("UTF-8"))

#send disconnect message
dmsg = "disconnect"
print("Disconnecting")
client_socket.send(dmsg)

client_socket.close()
