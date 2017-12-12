# this is searching the stair's edge with represent set
# v0.1 is added movBasicLen

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

# get information of video shape and predected interval between each stair
success, img = inVideo.read()
height, width = img.shape[:2]
stairInterval = height / 5

# for image stabilization, save the represent of stair
representStair = [] # (index[0] = y, index[1] = w, index[2] = mean((y + w) / 2))

movBasicLen = 0
imgCount = 0

#################################################################################
# Algorithm description
# 1. get edge: stair has linear edge properties, so, at first, use edge detection
# 2. extract high value of x axis: after sum value of edge's x axis, extract high
#       value that sum of edge's x axis
# 3. segmentation: predict whether stair's edge is same or not
# 4. image stabilization: when hand is shaked(?), image must be stabilized
#       for this fuction, make represent stair edge using previous data
# 5. draw rectangle: draw rectangle to edge of stair using predected x,y coordinate
#################################################################################

# get frame from video
while success:
    print('%d' %imgCount)

    # preproccess for detecting edges(blur), and detect edges
    blur = cv2.bilateralFilter(img, 4, 80, 80)
    edge = cv2.Canny(blur, 50, 100)
    
    # sum each edges of x aixs for searching stair's edge ( algorithm part )
    edgeSum = []
    
    for i in range(0, height):
        edgeSum.append((np.sum(edge[i]), i))
    
    # for extracting high value, sorting sum of edges
    edgeSum.sort(reverse = True)
    
    numIndex = 0
    
    # threshold is decided when ratio of edgeSum = 1 (high value of edge's x aixs)
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
    
    meanIndex = [] # (index[0] = y, index[1] = w, index[2] = mean((y + w) / 2))
    
    # search continuous edge partition (segmantation)
    for i in range(1, numIndex):
        if (indexSet[i] - startIndex) > stairInterval:
            endIndex = indexSet[i - 1]
            meanIndex.append([startIndex, endIndex - startIndex, int((startIndex + endIndex) / 2)])
            startIndex = indexSet[i]
    
    if numIndex != 0:
        endIndex = indexSet.pop()
        meanIndex.append([startIndex, endIndex - startIndex, int((startIndex + endIndex) / 2)])
    
    # image stabilization and update represent set of stair
    difY = [[-1, height] for i in range(0, len(meanIndex))]
    
    for i in range(0, len(representStair)):
        if len(meanIndex) == 0:
            break
    
        dif_index = 0
        dif_val = height
    
        for j in range(0, len(meanIndex)):
            if meanIndex[j][2] >= representStair[i][2]:
                dif_index = j
                dif_val = meanIndex[j][2] - representStair[i][2]
                break
    
        if dif_val < (stairInterval / 3):
            difY[dif_index][0] = i
            difY[dif_index][1] = dif_val
    
    # move about average of moving length
    movLen = 0
    movCount = 0
    
    for i in range(0, len(difY)):
        if difY[i][0] != -1:
            movLen += difY[i][1]
            movCount += 1
    
    movAvgLen = 0

    if movAvgLen > (height / 10):
        movAvgLen = movBasicLen
    elif movCount != 0:
        movAvgLen = int(movLen / movCount)
        movBasicLen = int(0.5 * movAvgLen + 0.5 * movBasicLen)
    
    rmvCount = 0
    
    for i in range(0, len(representStair)):
        representStair[i - rmvCount][0] += movAvgLen
        representStair[i - rmvCount][2] += movAvgLen
        
        # already pass this stair
        if representStair[i - rmvCount][0] + representStair[i - rmvCount][1] > (9 * height / 10):
            representStair.remove([representStair[i - rmvCount][0], representStair[i - rmvCount][1], representStair[i - rmvCount][2]])
            rmvCount += 1
    
    # draw rectangle to represent sitar area
    for i in range(0, len(representStair)):
        check = True
        
        for j in range(0, len(meanIndex)):
            if difY[j][0] == i:
                check = False
        
        #if check:
        cv2.rectangle(img, (0, representStair[i][0]), (width - 1, representStair[i][0] + representStair[i][1]), (0, 255, 0), 2)
    
    # add represent set of stair
    posRange = []
    seeker = 0
    
    for i in range(0, len(representStair)):
        if seeker < (representStair[i][0] - stairInterval):
            posRange.append([seeker, representStair[i][0] - stairInterval])
        
        seeker = int(representStair[i][0] + representStair[i][1] + stairInterval / 2)

    if seeker < (height - 1):
        posRange.append([seeker, height - 1])

    for i in range(0, len(meanIndex)):
        if difY[i][0] == -1:
            check = False
            
            for j in range(0, len(posRange)):
                if (meanIndex[i][2] < posRange[j][1]) & (meanIndex[i][2] > posRange[j][0]):
                    check = True
            
            if check:
                representStair.append([meanIndex[i][0], meanIndex[i][1], meanIndex[i][2]])
    
    representStair.sort()
    
    imgSet.append(img)
    
    cv2.imwrite('../basicMov/test%d.png' %imgCount, img)
    
    imgCount += 1
    
    # get next frame
    success, img = inVideo.read()

# write video
outVideo = cv2.VideoWriter('../basicMov.avi', fourcc, 25, (width, height))

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()
