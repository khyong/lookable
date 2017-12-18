import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

# init SIFT
sift = cv2.xfeatures2d.SIFT_create()

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(check = 50) # or pass empty dictionary 
                                 # check = a number of trial

# init FLANN
flann = cv2.FlannBasedMatcher(index_params, search_params)

# load image
img = cv2.imread('../picture/2.png')
blur = cv2.bilateralFilter(img, 5, 100, 100)
edge = cv2.Canny(blur, 100, 200)

# size of image
height, width, channel = img.shape

image, contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)

contList = []

for c in contours:
    # get the bounding rect
    x, y, w, h = cv2.boundingRect(c)
    # push the x, y, w, h in contList if w > width / 3
    if w > (width / 3):
        contList.append([w, h, x, y])
    #    cv2.rectangle(img, (x, y), (x+w, y+h), (R, G, B), 2)


# represent of stair (sencond big size of width)
contList.sort(reverse = True)

stairX = contList[1][2]
stairY = contList[1][3]
stairW = contList[1][0]
stairH = contList[1][1]

# clip the stair for template
tem = img[stairY : stairY + stairH, stairX : stairX + stairW]

# save the template (for programmer)
cv2.imwrite('../picture/template.jpg', tem)

# get keypoints of template and image
temKp, temDes = sift.detectAndCompute(tem, None)
imgKp, imgDes = sift.detectAndCompute(img, None)

matches = flann.knnMatch(temDes, imgDes, k = 2)

matchesMask = [[0, 0] for i in range(len(matches))]

min_x = width
max_x = 0
min_y = height
max_y = 0

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
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

# draw rectangle that matched object
cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)

cv2.imwrite('../picture/why.jpg', img)
