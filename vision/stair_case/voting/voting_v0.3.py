# this is searching the stair's edge using voting stair's edges
# v0.1 is just voting, alpha is 0.8
# v0.2 use threshold to determine whether it is stair or not
# v0.3 verify that fixed number of stiars is better than previous version
# v0.4 update stairInterval(or num of stairs) when each frame is updated
# v0.? will use represent set between each stairInterval

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
numOfStairs = 3
stairInterval = height / numOfStairs
edgeArea = int(stairInterval / 3)
predNum = 1

# for voting stair's edge, save the voting set of stairs
voteStair = []

for i in range(0, height):
    voteStair.append(0)

imgCount = 0

#################################################################################
# Algorithm description
# 1. get edge: stair has linear edge properties, so, at first, use edge detection
# 2. save values of x axis: to vote, sum value of edge's x axis and is saved to set
# 3. draw high values of set: draw predicted stair's edge to image
#################################################################################
# get frame from video
while success:
    #if imgCount < 350:
    #    for i in range(0, 350):
    #        print('%d' %imgCount)
    #        success, img = inVideo.read()
    #        imgCount += 1
    #else:
    #    print('%d' %imgCount)
    print('%d' %imgCount)

    # preproccess for detecting edges(blur), and detect edges
    blur = cv2.bilateralFilter(img, 4, 80, 80)
    edge = cv2.Canny(blur, 50, 100)
    
    # sum each edges of x aixs for searching stair's edge ( algorithm part )    
    for i in range(0, height):
        if np.sum(edge[i]) == 0:
            voteStair[i] *= 0.9
        else:
            voteStair[i] = 0.5 * np.sum(edge[i]) + 0.5 * voteStair[i]
    
    stair = []

    for i in range(0, height - edgeArea):
        stair.append([0, i])

        for j in range(0, edgeArea):
            stair[i][0] += voteStair[i + j]

    # for extracting high value, sorting sum of edges
    stair.sort(reverse = True)

    startIndex = []
    endIndex = []
    seeker = 0

    # search continuous edge partition and draw
    while (len(startIndex) < numOfStairs) and (seeker < len(stair)):
        check = True

        # not allow to draw in overlapped area
        for i in range(0, len(startIndex)):
            if (startIndex[i] < stair[seeker][1]) and (stair[seeker][1] < endIndex[i]):
                check = False
                break

        if check:
            cv2.rectangle(img, (0, stair[seeker][1]), (width - 1, stair[seeker][1] + edgeArea), (0, 255, 0), 2)        
            startIndex.append(stair[seeker][1] - stairInterval)
            endIndex.append(stair[seeker][1] + stairInterval)

        seeker += 1

    imgSet.append(img)
    
    cv2.imwrite('../voting/test%d.png' %imgCount, img)
    
    imgCount += 1
    
    # get next frame
    success, img = inVideo.read()

# write video
outVideo = cv2.VideoWriter('../voting_v0.3.avi', fourcc, 25, (width, height))

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()