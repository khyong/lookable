import cv2
import numpy as np
from matplotlib import pyplot as plt

# read video
inVideo = cv2.VideoCapture('../origin.avi')

# init fourcc
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# set of image for write video
imgSet = []

success, img = inVideo.read()
height, width = img.shape[:2]

imgCount = 0

while success:
    print(imgCount)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
#    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    # Finding unknown region
#    sure_fg = np.uint8(sure_fg)
#    unknown = cv2.subtract(sure_bg, sure_fg)

    cv2.imwrite('../segmentation/test%d.png' %imgCount, dist_transform)

    imgSet.append(dist_transform)

    imgCount += 1

    success, img = inVideo.read()


# write video
outVideo = cv2.VideoWriter('../segmentation_v0.1.avi', fourcc, 25, (width, height), False)

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()
