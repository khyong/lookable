import cv2
import numpy as np
from matplotlib import pyplot as plt

inVideo = cv2.VideoCapture('../resultCut.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

imgSet = []

success, img = inVideo.read()
height, width = img.shape[:2]

while success:
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
#    for i in range(0, numIndex - 1):
#        if (int(indexSet[i] / 100) != int(indexSet[i + 1] / 100)):
#            endIndex = indexSet[i]
#            cv2.rectangle(img, (0, startIndex), (width - 1, endIndex), (255, 0, 0), 2)
#            startIndex = indexSet[i + 1]
#        if i == (numIndex - 2):
#            endIndex = indexSet[i + 1]
#            cv2.rectangle(img, (0, startIndex), (width - 1, endIndex), (255, 0, 0), 2)

    imgSet.append(img)
    
    success, img = inVideo.read()

videoW = cv2.VideoWriter('../test.avi', fourcc, 25, (width, height))

for i in range(len(imgSet)):
    videoW.write(imgSet[i])

videoW.release()
