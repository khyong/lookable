import cv2
import numpy as np

img = cv2.imread('../result/test0.png')
height, width = img.shape[:2]
imgType = type(img)

# init fourcc
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# write video
outVideo = cv2.VideoWriter('../result.avi', fourcc, 10, (width, height))

imgCount = 0

while type(img) == imgType:
    print(imgCount)

    img = cv2.imread('../result/test%d.png' %imgCount)

    outVideo.write(img)

    imgCount += 1

outVideo.release()    