import cv2
import numpy as np

img = cv2.imread('../tracking/test0.png')
height, width = img.shape[:2]
imgType = type(img)

# init fourcc
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# write video
outVideo = cv2.VideoWriter('../tracking.avi', fourcc, 25, (width, height))

imgCount = 0

while type(img) == imgType:
    print(imgCount)

    img = cv2.imread('../tracking/test%d.png' %imgCount)

    outVideo.write(img)

    imgCount += 1

outVideo.release()    