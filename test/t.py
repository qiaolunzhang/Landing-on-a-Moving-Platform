#!/usr/bin/python

import picamera
import time
#import numpy as np
import string
import random
import os

from PIL import Image, ImageDraw, ImageFont

# Video Resolution for recording
VIDEO_HEIGHT = 940
VIDEO_WIDTH = 1280

baseDir='/home/pi/osd/' # directory where the video will be recorded

os.system('clear') # clear the terminal from any other text

with picamera.PiCamera() as camera:
   camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
   camera.framerate = 60
   #camera.led = False
   camera.start_preview()

   try:
      while True:
         time.sleep(1)

   except KeyboardInterrupt:
      print "Cancelled"
