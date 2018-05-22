import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('box.png', 0)     # query image
img2 = cv2.imread('box_in_scene.png', 0) # trainImage

# Initiate SIFT detector
orb = cv2.ORB()
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)
print("Test")