# this is just searching the stair's edge without represent set

import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt

# initiate variables #####################################################
# read video
inVideo = cv2.VideoCapture('../origin.avi')

# init fourcc
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# set of image for write video
imgSet = []

success, img = inVideo.read()
height, width = img.shape[:2]
stairInterval = height / 5

imgCount = 0

# get frame from video
while success:
    print('%d' %imgCount)

    blur = cv2.bilateralFilter(img, 4, 80, 80)
    edge = cv2.Canny(blur, 50, 100)
    
    # search stair's edge
    edgeSum = []
    
    for i in range(0, height):
        edgeSum.append((np.sum(edge[i]), i))
    
    edgeSum.sort(reverse = True)
    
    numIndex = 0
    
    # threshold is decided when ratio of edgeSum = 1
    for i in range(0, height - 1):
        if edgeSum[i][0] == edgeSum[i + 1][0]:
            numIndex = i
            break
    
    indexSet = [] # set of indice that present the edge
    
    for i in range(0, numIndex):
        indexSet.append(edgeSum[i][1])
        
    indexSet.sort()
        
    # draw rectangle to place of stair (a number of = endIndex)
    if numIndex != 0:
        startIndex = indexSet[0]
    
    # search continuous edge partition
    for i in range(1, numIndex):
        if (indexSet[i] - startIndex) > stairInterval:
            endIndex = indexSet[i - 1]
            cv2.rectangle(img, (0, startIndex), (width - 1, endIndex), (255, 0, 0), 2)
            startIndex = indexSet[i]

    if numIndex != 0:
        endIndex = indexSet.pop()
        cv2.rectangle(img, (0, startIndex), (width - 1, endIndex), (255, 0, 0), 2)
    
    imgSet.append(img)

    cv2.imwrite('../simple_stair/test%d.png' %imgCount, img)

    imgCount += 1

    # get next frame
    success, img = inVideo.read()

# write video
outVideo = cv2.VideoWriter('../simple_stair.avi', fourcc, 25, (width, height))

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()
