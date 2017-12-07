# import library #########################################################
import sys
import cv2
import math
import numpy as np
import time
from matplotlib import pyplot as plt

# initiate variables #####################################################
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

# read video
video = cv2.VideoCapture('../video/resultCut.mp4')

# init python plot for test (developer)
subPlot = plt.subplot(111)
plt.ion()

# while (success to find stair) : next frame
##########################################################################
# extract first frame of video 
success, img = video.read()
blur = cv2.bilateralFilter(img, 5, 100, 100)
edge = cv2.Canny(blur, 50, 100)
height, width = edge.shape[:2]

# search (or predict) a stair
image, contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)

contList = []

for c in contours:
    # get the bounding rect
    x, y, w, h = cv2.boundingRect(c)
    # push the x, y, w, h in contList if w > width / 3
    if w > 0:
        contList.append([w, h, x, y])
    #    cv2.rectangle(img, (x, y), (x+w, y+h), (R, G, B), 2)


# represent of stair (sencond big size of width)
contList.sort(reverse = True)

stairX = contList[1][2]
stairY = contList[1][3]
stairW = contList[1][0]
stairH = contList[1][1]

# clip the stair for template
stair = img[stairY : stairY + stairH, stairX : stairX + stairW]

# make a stair template
cv2.imwrite('../video/stair.jpg', stair)

# stair load
stair = cv2.imread('../stair.jpg')

# are you sure that 'template.jpg' is stair? [not yet]
##########################################################################

# while (success to find shoes) : next frame
##########################################################################
# search (or predict) a foot (or shoes) [not yet]
shoes = cv2.imread('../picture/shoesEdge.jpg')

##########################################################################

imgCount = 0

# get keypoints of template
stairKp, stairDes = sift.detectAndCompute(stair, None)
shoesKp, shoesDes = sift.detectAndCompute(shoes, None)

# while (success to complete using stair) : next frame
while success:
##########################################################################
    # search (or predict) next stair
    success, img = video.read()
#    blur = cv2.bilateralFilter(img, 5, 100, 100)
#    edge = cv2.Canny(blur, 100, 200)

    # get keypoints of image
    imgKp, imgDes = sift.detectAndCompute(img, None)

    stairMatches = flann.knnMatch(stairDes, imgDes, k = 2)
    shoesMatches = flann.knnMatch(shoesDes, imgDes, k = 2)

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


    min_x = math.ceil(min_x)
    min_y = math.ceil(min_y)
    max_x = math.ceil(max_x)
    max_y = math.ceil(max_y)

    # draw rectangle to stair in image
    cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)

    # save test image
    #cv2.imwrite('../video/result%d.jpg' % imgCount, img)
    fig = subPlot.imshow(img)
    plt.pause(0.001)


plt.ioff()
plt.show()
# alarm whether safety or unsafety by using algorithm (foot line, end line of stair) [not yet]
##########################################################################
