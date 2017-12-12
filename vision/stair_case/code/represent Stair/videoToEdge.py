import sys
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import time

img = cv2.imread('../removeBandi/0.png')
height, width = img.shape[:2]

#video = cv2.VideoCapture('../video/resultCut.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter('../123123.avi', fourcc, 25, (width, height))

#success, img = video.read()

imgSet = []

count = 0

for i in range(0, 413):
    img = cv2.imread('../removeBandi/%d.png' % count)

    imgSet.append(img)

    count += 1
#    imgSet.append(img)

for i in range(len(imgSet)):
    video.write(imgSet[i])

video.release()
