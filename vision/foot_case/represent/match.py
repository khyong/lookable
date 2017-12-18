import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
THRESHOLD = 0.5

# initiate variables #####################################################
# read video
inVideo = cv2.VideoCapture('../origin.avi')

success, img = inVideo.read()
height, width = img.shape[:2]

template = cv2.imread('../foot.png', 0)
w, h = template.shape[::-1]

# init fourcc
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# set of image for write video
imgSet = []

firstShoe = [720, 870]
secondShoe = [1050, 820]

imgCount = 0

avgTime = 0

while success:
    print(imgCount)
    start = time.time()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(imgGray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= THRESHOLD)

    firstX, firstY = 0, 0
    firstDis = pow(w, 2) + pow(h, 2)
    secondX, secondY = 0, 0
    secondDis = pow(w, 2) + pow(h, 2)

    for pt in zip(*loc[::-1]):
#        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if (pow(firstShoe[0] - pt[0], 2) + pow(firstShoe[1] - pt[1], 2)) < firstDis:
            firstX, firstY = pt[0], pt[1]
            firstDis = pow(firstShoe[0] - pt[0], 2) + pow(firstShoe[1] - pt[1], 2)
        if (pow(secondShoe[0] - pt[0], 2) + pow(secondShoe[1] - pt[1], 2)) < secondDis:
            secondX, secondY = pt[0], pt[1]
            secondDis = pow(secondShoe[0] - pt[0], 2) + pow(secondShoe[1] - pt[1], 2)

    if (firstDis <= 10000) and ((secondShoe[0] - w) > firstX):
        firstShoe[0] = firstX
        firstShoe[1] = firstY
    if (secondDis <= 10000) and ((firstShoe[0] + w) < secondX):
        secondShoe[0] = secondX
        secondShoe[1] = secondY
        
    cv2.rectangle(img, (firstShoe[0], firstShoe[1]), (firstShoe[0] + w, firstShoe[1] + h), (0, 0, 255), 2)
    cv2.rectangle(img, (secondShoe[0], secondShoe[1]), (secondShoe[0] + w, secondShoe[1] + h), (0, 0, 255), 2)
    end = time.time()

    imgSet.append(img)
    
    cv2.imwrite('../match/test%d.png' %imgCount, img)
    
    imgCount += 1
    
    # get next frame
    success, img = inVideo.read()
    avgTime += end - start

print(avgTime / (imgCount + 1))

# write video
outVideo = cv2.VideoWriter('../match.avi', fourcc, 25, (width, height))

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()
