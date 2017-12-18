import cv2
import numpy as np
from matplotlib import pyplot as plt

# read video
inVideo = cv2.VideoCapture('../origin.avi')
template = cv2.imread('../foot.png')

# init fourcc
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# set of image for write video
imgSet = []

success, img = inVideo.read()
height, width = img.shape[:2]
shoeH, shoeW = template.shape[:2]

imgCount = 0

templateRGB = [[0, 0, 0] for i in range(0, 255)]
#representRGB = [] # index[0] = RGB, index[1] = top 10 [0,10)

for i in range(0, shoeH):
    for j in range(0, shoeW):
        templateRGB[template[i][j][0]][0] += 1
        templateRGB[template[i][j][1]][2] += 1
        templateRGB[template[i][j][2]][2] += 1
     
shoeR = templateRGB[0].index(max(templateRGB[0]))
shoeG = templateRGB[1].index(max(templateRGB[1]))
shoeB = templateRGB[2].index(max(templateRGB[2]))

#for i in range(0, 3):
#    templateRGB.sort()
#    temp = []###

#    for j in range(0, 10):
#        temp.append([template[j][0]])

#    representRGB.append(temp)

#    for j in range(0, 255):
#        temlateRGB[i][0] = 0

while success:
    print(imgCount)

    pointRGB = []

    #for i in range(0, height - shoeH):
    #    temp = []

#        for j in range(0, width - shoeW):
#            temp.append(

    for i in range(0, height - shoeH):
        for j in range(0, width - shoeW):
            if (img[i][j][0] > 0.95 * shoeR) and (img[i][j][1] > 0.95 * shoeG) and (img[i][j][2] > 0.95 * shoeB) and (img[i][j][0] < 1.05 * shoeR) and (img[i][j][1] < 1.05 * shoeG) and (img[i][j][2] < 1.05 * shoeB):
                pointRGB.append([j, i])

    for i in range(0, len(pointRGB)):
        cv2.rectangle(img, (pointRGB[i][0], pointRGB[i][1]), (pointRGB[i][0] + shoeW, pointRGB[i][1] + shoeH), (0, 255, 0), 2)
            
    cv2.imwrite('../search/test%d.png' %imgCount, img)

    imgSet.append(img)

    imgCount += 1

    success, img = inVideo.read()


# write video
outVideo = cv2.VideoWriter('../search.avi', fourcc, 25, (width, height), False)

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()
