#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

from functools import wraps
import math
import random
import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 240     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) +j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def syncToMusic(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        output = conn.recv(2048);
        if output.strip() == "disconnect":
            conn.close()
            sys.exit("Received disconnect message.  Shutting down.")
            conn.send(b"dack")
        elif output:
            decoded = output.decode("utf-8").rstrip()
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        cava_values = decoded.split(";")
        avg = (int(cava_values[0]) + int(cava_values[1]) + int(cava_values[2]) + int(cava_values[3])) / 4

        strip.setBrightness(avg)
        strip.show()
        time.sleep(wait_ms/1000.0)

def musicServer(strip):
    host = '10.0.0.37'
    port = 8268
    address = (host, port)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(address)
    server_socket.listen(5)

    print ("Listening for client . . .")
    conn, address = server_socket.accept()
    print ("Connected to client at ", address)
    while True:
        output = conn.recv(2048);
        if output.strip() == "disconnect":
            conn.close()
            sys.exit("Received disconnect message.  Shutting down.")
            conn.send(b"dack")
        elif output:
            decoded = output.decode("utf-8").rstrip()
        cava_values = decoded.split(";")
        avg = (int(cava_values[0]) + int(cava_values[1]) + int(cava_values[2]) + int(cava_values[3])) / 4

        strip.setBrightness(avg)
        strip.show()

def music_leds(strip, music):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    numMusic = len(music) - 1
    total = strip.numPixels() / numMusic
    for j in range(strip.numPixels()):
        strip.setPixelColor(j, Color(int(music[0]), int(music[0]), int(music[0])))
    strip.show()

def theaterChaseRainbow(strip, wait_ms=50):
    # Rainbow movie theater light style chaser animation.
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

"""
#Christmas style
#def theaterChaseRainbow(strip, wait_ms=75):
    # Rainbow movie theater light style chaser animation.
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, Color(255, 0, 0))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, Color(0, 255, 0))
"""

def spreadout(strip, wait_ms=20, iterations=5):
    middle = strip.numPixels()/2
    for j in range(iterations):
        for i in range(middle):
            strip.setPixelColor(middle + i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.setPixelColor(middle - i, wheel((int(i * 256 / strip.numPixels()) - j) & 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
        for x in range(middle):
            strip.setPixelColor(x, wheel((int(x * 256 / strip.numPixels()) + j) & 255))
            strip.setPixelColor(strip.numPixels() - x, wheel((int(strip.numPixels() - x * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms/1000.0)

def randColor():
    return Color(random.randint(0,255),random.randint(0,255), random.randint(0, 255)) 

# Define functions which animate LEDs in various ways.
def customColor(strip, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for c in range(250):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(greenSlider, redSlider, blueSlider))
        strip.show()
        time.sleep(wait_ms/1000.0)

def simpleWave(strip, rate, cycles, scale, wait):
    pos=0.0;
    for x in range(strip.numPixels() * cycles):
        pos = pos+rate
        for i in range(strip.numPixels()):
            level = math.sin(i+pos * scale) * 127 + 128
            strip.setPixelColor(i, wheel(int(level)))
        strip.show()
        time.sleep(wait/1000.0)

def fade(strip, cycles, wait_ms=5):
    for c in range(cycles):
        for x in range(200):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(x, x/2, 255))
            strip.show()
            time.sleep(timeDelay/100000.0)
        for y in range(200):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(200 - y, (200 - y)/2, 255))
            strip.show()
            time.sleep(timeDelay/100000.0)

def handleServerFIFO():
    print "Opening FIFO for reading"
    path = "/home/pi/alaunus/fifopipes/testpipe"
    try:
        os.remove(path)
        os.mkfifo(path)
        os.chmod(path, 0o777)
    except:
        print "FIFO already exists"
    with open(path) as fifo:
        print "FIFO opened"
        while True:
            data = fifo.read().decode(encoding='UTF-8')
            if len(data) != 0:
                global timeDelay 
                global redSlider
                global greenSlider
                global blueSlider

                global fadeColorFrom
                global fadeColorTo

                # Check boxes
                global customColorActive
                global fadeActive
                global simpleWaveActive
                global spreadoutActive
                global theaterChaseRainbowActive
                global rainbowActive
                global rainbowCycleActive
                vals = data.split()
                print(vals)
                try:
                    if (vals[0] == "timeSlider" and int(vals[1]) <= 2000):
                        timeDelay = int(vals[1])
                    else:
                        if vals[0] == "redSlider":
                            redSlider = int(vals[1])
                        elif vals[0] == "blueSlider":
                            blueSlider = int(vals[1])
                        elif vals[0] == "greenSlider":
                            greenSlider = int(vals[1])
                        elif vals[0] == "fadeColorFrom":
                            blueSlider = int(vals[1])
                        elif vals[0] == "fadeColorTo":
                            greenSlider = int(vals[1])
                        elif vals[0] == "customColorCheckBox":
                            customColorActive = bool(int(vals[1]))
                        elif vals[0] == "fadeCheckBox":
                            fadeActive = bool(int(vals[1]))
                        elif vals[0] == "simpleWaveCheckBox":
                            simpleWaveActive = bool(int(vals[1]))
                        elif vals[0] == "spreadoutCheckBox":
                            spreadoutActive = bool(int(vals[1]))
                        elif vals[0] == "theaterChaseRainbowCheckBox":
                            theaterChaseRainbowActive = bool(int(vals[1]))
                        elif vals[0] == "rainbowCheckBox":
                            rainbowActive = bool(int(vals[1]))
                        elif vals[0] == "rainbowCycleCheckBox":
                            rainbowCycleActive = bool(int(vals[1]))
                except:
                    print ""
                print 'Read: "{0}"'.format(data)


import os
import socket
import sys
import threading
import fileinput

timeDelay = 1000

customColorActive = False
fadeActive = True
simpleWaveActive = True
spreadoutActive = True
theaterChaseRainbowActive = True
rainbowActive = True
rainbowCycleActive = True

redSlider = 255
greenSlider = 0
blueSlider = 0


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-m', '--music', action='store_true', help='start server for sync to music')
    parser.add_argument('-k', '--kill', action='store_true', help='start server for sync to music')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    if args.kill:
        print "Performing colorwipe"
        colorWipe(strip, Color(0,0,0))
        sys.exit()
    elif args.music:
        serverThread = threading.Thread(target=musicServer, args=(strip,))
        serverThread.start()
    print ('Press Ctrl-C to quit.')
    fifoThread = threading.Thread(target=handleServerFIFO, args=())
    fifoThread.start()
    if not args.clear:
        print ('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            # Check boxes
            if (customColorActive):
                customColor(strip)
            print (customColorActive, fadeActive, simpleWaveActive, spreadoutActive, theaterChaseRainbowActive, rainbowActive, rainbowCycleActive)
            if (fadeActive):
                fade(strip, 20)
            if (simpleWaveActive):
                simpleWave(strip, 0.01,5, 20, 10)
            if (spreadoutActive):
                spreadout(strip)
            if (theaterChaseRainbowActive):
                theaterChaseRainbow(strip)
            if (rainbowActive):
                rainbow(strip)
            if (rainbowCycleActive):
                rainbowCycle(strip)
                
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

