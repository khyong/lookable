import sys
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import time

# init SIFT
sift = cv2.xfeatures2d.SIFT_create()

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(check = 50) # or pass empty dictionary 
                                 # check = a number of trial

# init FLANN
flann = cv2.FlannBasedMatcher(index_params, search_params)
del FLANN_INDEX_KDTREE, index_params, search_params

video = cv2.VideoCapture('../video/resultCut.mp4')
stair = cv2.imread('../stair.jpg')

success, img = video.read()

subPlot = plt.subplot(111)
plt.ion()

stairKp, stairDes = sift.detectAndCompute(stair, None)
imgKp, imgDes = sift.detectAndCompute(img, None)

stairMatches = flann.knnMatch(stairDes, imgDes, k = 2)

stairMatchesMask = [[0, 0] for i in range(len(stairMatches))]

min_x = width
max_x = 0
min_y = height
max_y = 0

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(stairMatches):
    if m.distance < 0.75 * n.distance:
        #matchesMask[i] = [1, 0]
        min_x = min(min_x, imgKp[m.trainIdx].pt[0])
        min_y = min(min_y, imgKp[m.trainIdx].pt[1])
        max_x = max(max_x, imgKp[m.trainIdx].pt[0])
        max_y = max(max_y, imgKp[m.trainIdx].pt[1])


in_x = math.ceil(min_x)
min_y = math.ceil(min_y)
max_x = math.ceil(max_x)
max_y = math.ceil(max_y)

while success:
    success, img = video.read()
    #blur = cv2.bilateralFilter(img, 4, 80, 80)
    #edge = cv2.Canny(blur, 50, 100)

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
