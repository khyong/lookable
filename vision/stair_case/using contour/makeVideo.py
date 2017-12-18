import sys
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import time

video = cv2.VideoCapture('../video/resultCut.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

imgSet = []

success, image = video.read()

height, width = image.shape[:2]

while success:
    success, img = video.read()
    blur = cv2.bilateralFilter(img, 4, 80, 80)
    edge = cv2.Canny(blur, 50, 100)
    imgSet.append(edge)

videoW = cv2.VideoWriter('../test.mp4', fourcc, 25, (width, height), False)

for i in range(len(imgSet)):
    videoW.write(imgSet[i])

video.release()
videoW.release()
