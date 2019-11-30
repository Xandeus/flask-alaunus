import os
import sys

path = "/tmp/testpipe"
fifo = open(path, "w")
fifo.write(sys.argv[1])
fifo.close()
