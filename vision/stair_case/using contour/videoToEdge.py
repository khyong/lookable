import sys
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import time

video = cv2.VideoCapture('../video/resultCut.mp4')

success, image = video.read()

subPlot = plt.subplot(111)
plt.ion()

while success:
    success, img = video.read()
    blur = cv2.bilateralFilter(img, 4, 80, 80)
    edge = cv2.Canny(blur, 50, 100)

    image, contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
    height, width = edge.shape[:2]

    contList = []

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > (0):
            #contList.append([w, h, x, y])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #contList.sort(reverse = True)

    #stairX = contList[0][2]
    #stairY = contList[0][3]
    #stairW = contList[0][0]
    #stairH = contList[0][1]

    #stair = img[stairY : stairY + stairH, stairX : stairX + stairW]

    #fig = subPlot.imshow(stair)
    fig = subPlot.imshow(edge)
    plt.pause(0.001)

plt.ioff()
plt.show()
