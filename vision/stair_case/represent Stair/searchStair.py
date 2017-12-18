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
stairInterval = height / 4

# for image stabilization, save the represent of stair
representStair = [] # (index[0] = y, index[1] = w, index[2] = mean((y + w) / 2))

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
    
    meanIndex = [] # (index[0] = y, index[1] = w, index[2] = mean((y + w) / 2))
    
    # search continuous edge partition
    for i in range(0, numIndex - 1):
        if (indexSet[i + 1] - indexSet[i]) > stairInterval:
            endIndex = indexSet[i]
            cv2.rectangle(img, (0, startIndex), (width - 1, endIndex), (255, 0, 0), 2)
            meanIndex.append([startIndex, endIndex - startIndex, int((startIndex + endIndex) / 2)])
            startIndex = indexSet[i + 1]
        if (i == (numIndex - 2)) & (startIndex != endIndex):
            endIndex = indexSet[i + 1]
            cv2.rectangle(img, (0, startIndex), (width - 1, endIndex), (255, 0, 0), 2)
            meanIndex.append([startIndex, endIndex - startIndex, int((startIndex + endIndex) / 2)])
    
    # image stabilization and update represent set of stair
    difY = [[-1, width] for i in range(0, len(meanIndex))]
    
    for i in range(0, len(representStair)):
        if len(meanIndex) == 0:
            break
    
        dif_index = 0
        dif_val = width
    
        for j in range(0, len(meanIndex)):
            if dif_val > abs(meanIndex[j][2] - representStair[i][2]):
                dif_index = j
                dif_val = abs(meanIndex[j][2] - representStair[i][2])
    
        if (difY[dif_index][1] > dif_val) & (dif_val < (stairInterval / 3)):
            difY[dif_index][0] = i
            difY[dif_index][1] = dif_val
    
    # draw additional rectangle
    for i in range(0, len(representStair)):
        check = True
    
        for j in range(0, len(meanIndex)):
            if difY[j][0] == i:
                check = False
    
        if check:
            cv2.rectangle(img, (0, representStair[i][0]), (width - 1, representStair[i][0] + representStair[i][1]), (0, 255, 0), 2)
    
        # for test
        else:
            cv2.rectangle(img, (0, representStair[i][0]), (width - 1, representStair[i][0] + representStair[i][1]), (0, 255, 0), 2)
    
    ############################## if accuracy is low, try to using mean value ######
    # update represent set of stair
    for i in range(0, len(meanIndex)):
        dif_min = width

        for j in range(0, len(representStair)):
            dif_min = min(abs(representStair[j][2] - meanIndex[i][2]), dif_min)

        if difY[i][0] == -1:
            if (dif_min < stairInterval) | (len(representStair) == 0):
                representStair.append([meanIndex[i][0], meanIndex[i][1], meanIndex[i][2]])

        elif representStair[difY[i][0]][0] < meanIndex[i][0]:
            representStair[difY[i][0]][0] = meanIndex[i][0]
            representStair[difY[i][0]][1] = meanIndex[i][1]
            representStair[difY[i][0]][2] = meanIndex[i][2]
    
    # periodically remove stair that is already processed or not accurate
    rmvCount = 0

    representStair.sort()
    
    for i in range(0, len(representStair)):
        # processed stair
        if (width - representStair[i - rmvCount][0] - representStair[i - rmvCount][1]) < (width / 8):
            representStair.remove([representStair[i - rmvCount][0], representStair[i - rmvCount][1], representStair[i - rmvCount][2]])
            rmvCount += 1
            
        # not accurate stair
        if (i != rmvCount) & (i - rmvCount != len(representStair) - 1):
            if (representStair[i + 1 - rmvCount][0] - representStair[i - 1 - rmvCount][0] - representStair[i - 1 - rmvCount][1]) < stairInterval:
                representStair.remove([representStair[i - rmvCount][0], representStair[i - rmvCount][1], representStair[i - rmvCount][2]])
                rmvCount += 1

    imgSet.append(img)

    cv2.imwrite('../represent/test%d.png' %imgCount, img)

    imgCount += 1

    # get next frame
    success, img = inVideo.read()

# write video
outVideo = cv2.VideoWriter('../test.avi', fourcc, 25, (width, height))

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()
