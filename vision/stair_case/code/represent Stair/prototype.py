# import library #########################################################
import cv2
import numpy as np
from matplotlib import pyplot as plt

# initiate variables #####################################################
# read video
video = cv2.VideoCapture('../video/resultCut.mp4')

# init fourcc
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# set of image for writing video
imgSet = []

# get height and width of video
success, img = inVideo.read()
height, width = img.shape[:2]

# alert end of stair
##########################################################################
# while (can read video): next frame
while success:
    blur = cv2.bilateralFilter(img, 5, 100, 100)
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
    
    # draw rectangle to end partition of stair
    for i in range(0, numIndex - 1):
        if (int(indexSet[i] / 100) != int(indexSet[i + 1] / 100)):
            endIndex = indexSet[i]
            cv2.rectangle(img, (0, startIndex), (width - 1, endIndex), (255, 0, 0), 2)
            startIndex = indexSet[i + 1]
        if i == (numIndex - 2):
            endIndex = indexSet[i + 1]
            cv2.rectangle(img, (0, startIndex), (width - 1, endIndex), (255, 0, 0), 2)
    
    # add processed image to set of images
    imgSet.append(img)

    # get next frame
    success, img = inVideo.read()

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
