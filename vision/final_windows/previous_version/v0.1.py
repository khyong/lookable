# ###########################################################################
# this is detecting stairs and shoes
# for detecting stairs, use voting algorithm (A)
# for detecting shoes, use tracking algorithm (B)
# v0.1 is to combine A and B and to develop new algorithm for determine numOfStairs
# refer to A, open '../stair/code/voting_v0.4.py'
# refer to B, open '../foot/code/multiTracking.py'
# ###########################################################################

import numpy as np
import cv2
import time
import threading
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt

# start) init variables #####################################################
# define variable -----------------------------------------------------------
WARNINGTHRESHOLD = 5

# main variable -------------------------------------------------------------
inVideo = cv2.VideoCapture('../origin.avi')
success, img = inVideo.read()
height, width = img.shape[:2]
imgSet = [] # set of image for write video
imgCount = 0 # number of processed imgs
avgTime = 0 # to calculate this program's each image processing time
font = cv2.FONT_HERSHEY_SIMPLEX # alarm safety or not
warningCount = 0
prevDist = 0

# shoes variable ------------------------------------------------------------
tracker = cv2.MultiTracker_create() # init tracker for tracking shoes
x1, y1, w1, h1 = 720, 870, 940 - 720, 1080 - 870 # first shoe's location
x2, y2, w2, h2 = 1050, 840, 1250 - 1050, 1025 - 840 # second shoe's location
box1 = (x1, y1, w1, h1)
box2 = (x2, y2, w2, h2)
tracker.add(cv2.TrackerBoosting_create(), img, box1) # start tracking first shoe
tracker.add(cv2.TrackerBoosting_create(), img, box2) # start tracking second shoe

# stairs variable -----------------------------------------------------------
numOfStairs = 2 # init stair's variables
numOfTester = int(height / 10)
stairInterval = height / numOfStairs
edgeArea = int(stairInterval / numOfStairs) # area of stair's edge
voteStair = [] # for voting stair's edge, save the voting set of stairs
predictCount = 0 # if current predicted value and previous predicted value are same and it's count is 10, maybe predicted number of stairs is exact
preNum = 2 # previous predicted number of stairs

# init voteStair
for i in range(0, height):
    voteStair.append(0)

# saving images variable ----------------------------------------------------
complete = False # flag for checking saving imgs
seeker = 0 # number of saved imgs

# writing video variable ----------------------------------------------------
fourcc = cv2.VideoWriter_fourcc(*'XVID') # fourcc need to extension of video
outVideo = cv2.VideoWriter('../result.avi', fourcc, 25, (width, height))
# end) init variables #######################################################

# start) functions ##########################################################
# ###########################################################################
# Algorithm description: predicting number of stairs
# 1. extract top 10 percent of edge sum
# 2. extract optimized number of cluster
#   2.1 while increasing k, measure minimum distacne between each inter clusters
#   2.2 determine k when gradient of distance between current inter clutster and
#       previous inter cluster is decreasement value
# 3. This algorithm stops prediction when k is 10 consecutively the same value
# ###########################################################################
def predictNumOfStair(edgeSum):
    startPNOS = time.time()

    global predictCount
    global preNum

    copyVoteStair = edgeSum.copy()

    for i in range(0, len(edgeSum)):
        copyVoteStair[i] = [copyVoteStair[i], i]

    copyVoteStair.sort(reverse = True)

    representY = []

    for i in range(0, numOfTester):
        representY.append([copyVoteStair[i][1], 0])

    representY.sort()

    predictNum = 2
    prevMin = 0

#    for i in range(0, numOfTester):
    for i in range(0, int(numOfTester / 10)):
        currMin = height
        currMax = 0
        distIntraCluster = []
        prevCluster = -1
        prevIndexY = -1

        kmeans = KMeans(n_clusters = predictNum, random_state = 0).fit(representY)

        # get min value of inter cluster distance
        for cluster in zip(representY, kmeans.labels_):
            # first time
            if prevIndexY == -1:
                prevCluster = cluster[1]
                prevIndexY = cluster[0][0]
                distIntraCluster.append(cluster[0][0])

            if prevCluster != cluster[1]:
                if currMin > (cluster[0][0] - prevIndexY):
                    currMin = cluster[0][0] - prevIndexY

                if currMax < (cluster[0][0] - prevIndexY):
                    currMax = cluster[0][0] - prevIndexY

                distIntraCluster[len(distIntraCluster) - 1] -= cluster[0][0]
                distIntraCluster[len(distIntraCluster) - 1] *= -1

                prevCluster = cluster[1]

            prevIndexY = cluster[0][0]
            print(cluster)

        print(i, predictNum, currMin, currMax)
        #if prevMin > currMin:
        #    break

        if (currMin / currMax) < 0.7:
            break

        #prevMin = currMin
        predictNum += 1
    
    predictNum -= 1

    if predictNum == preNum:
        predictCount += 1
    else:
        preNum = predictNum
        predictCount = 0

    endPNOS = time.time()
    print('predict number of stairs >>', endPNOS - startPNOS, predictNum, predictCount)

    return predictNum

# ###########################################################################
# Algorithm description: detecting stairs
# 1. get edge: stair has linear edge properties, so, at first, detect edges
# 2. save values of x axis: to vote, sum values of edge's x axis and save at set
# 3. draw high values of set: draw stair's edge to image
# ###########################################################################
def detectStair(img):
    startDS = time.time()

    global numOfStairs
    global stairInterval
    global edgeArea
    global voteStair

    # preproccess for detecting edges(blur), and detect edges
    blur = cv2.bilateralFilter(img, 4, 80, 80)
    edge = cv2.Canny(blur, 50, 100)
    
    # for update number of stairs
    edgeSum = []

    # sum each edges of x aixs for searching stair's edge ( algorithm part )    
    for i in range(0, height):
        if np.sum(edge[i]) == 0:
            voteStair[i] *= 0.9
        else:
            voteStair[i] = 0.5 * np.sum(edge[i]) + 0.5 * voteStair[i]
        edgeSum.append([np.sum(edge[i]), i])

    #edgeSum.sort(reverse = True)

    if predictCount <= 10:
        #numOfStairs = predictNumOfStair(edgeSum)
        numOfStairs = predictNumOfStair(voteStair)
        stairInterval = height / numOfStairs
        edgeArea = int(stairInterval / numOfStairs)

    stair = []

    for i in range(0, height - edgeArea):
        stair.append([0, i])

        for j in range(0, edgeArea):
            stair[i][0] += voteStair[i + j]

    # for extracting high value, sorting sum of edges
    stair.sort(reverse = True)

    startIndex = []
    endIndex = []
    seeker = 0
    stairBox = []

    # search continuous edge partition and draw
    while (len(startIndex) < numOfStairs) and (seeker < len(stair)):
        check = True

        # not allow to draw in overlapped area
        for i in range(0, len(startIndex)):
            if (startIndex[i] < stair[seeker][1]) and (stair[seeker][1] < endIndex[i]):
                check = False
                break

        if check:
            stairBox.append([stair[seeker][1], stair[seeker][1] + edgeArea])
            startIndex.append(stair[seeker][1] - stairInterval)
            endIndex.append(stair[seeker][1] + stairInterval)

        seeker += 1

    endDS = time.time()
    print('detection stairs >>', endDS - startDS)

    return stairBox
    
# ###########################################################################
# Algorithm description: tracking shoes
# 1. get edge: stair has linear edge properties, so, at first, use edge detection
# 2. save values of x axis: to vote, sum value of edge's x axis and is saved to set
# 3. draw high values of set: draw predicted stair's edge to image
# ###########################################################################
def multiTracking(img):
    #    if (tempbox1[0] + tempbox1[2] - tempbox2[0]) < 50:
#        if (tempbox1[0] + tempbox1[2]) < (width / 2):
#            tracker1.update(img)
#            box1 = tempbox1
#        else:
#            temp1.init(img, box1)
#            
#        if tempbox2[0] > (width / 2):
#            tracker2.update(img)
#            box2 = tempbox2
#        else:
#            temp2.init(img, box2)


    return tracker.update(img)

# ###########################################################################
# Algorithm description: saving images
# 1. get edge: stair has linear edge properties, so, at first, use edge detection
# 2. save values of x axis: to vote, sum value of edge's x axis and is saved to set
# 3. draw high values of set: draw predicted stair's edge to image
# ###########################################################################
def saveImg():
    global seeker
    global imgSet

    while True:
        while True:
            time.sleep(0.2)
            if complete or (len(imgSet) > seeker):
                break

        if complete:
            break
        print(seeker, complete, len(imgSet))
        img = imgSet[seeker]

        cv2.imwrite('../result/test%d.png' % seeker, img)

        seeker += 1

        print('saveImg >> write Img %d' %seeker)
# end) functions ############################################################

t = threading.Thread(target = saveImg) # thread for saving images

t.start() # start the thread

# satrt) main ###############################################################
while success:
    print(imgCount, '--')
    startMAIN = time.time()

    shoeMaxY = height
    safety = True
    distShoeStair = height
    stairBorder = []
    
    # detect Stair in image
    stairBox = detectStair(img)

    # detect(tracking) shoes in image
    success, shoeBox = multiTracking(img)

    # draw rectangles to stairs
    for i in range(0, len(stairBox)):
        cv2.rectangle(img, (0, stairBox[i][0]), (width - 1, stairBox[i][1]), (0, 255, 0), 2)

        stairBorder.append(stairBox[i][1])

    # draw rectangles to shoes area
    for pt in shoeBox:
        cv2.rectangle(img, (int(pt[0]), int(pt[1])), (int(pt[0] + pt[2]), int(pt[1] + pt[3])), (0, 0, 255), 2)

        if int(pt[1]) < shoeMaxY:
            shoeMaxY = int(pt[1])

    # determine safety or not
    for i in range(0, len(stairBorder)):
#        if (stairBorder[i][0] < shoeMaxY) and (stairBorder[i][1] > shoeMaxY):
#            if (imgCount != 0) and ((prevDist * 2) < distShoeStair):
#                safety = True

        if (stairBorder[i] < shoeMaxY) and ((shoeMaxY - stairBorder[i]) < distShoeStair):
            distShoeStair = shoeMaxY - stairBorder[i]

    if (imgCount != 0) and ((prevDist * 2) < distShoeStair):
        safety = False
    
    prevDist = distShoeStair
        
    cv2.rectangle(img, (0, shoeMaxY), (width - 1, shoeMaxY + 1), (127, 127, 0), 2)
    cv2.rectangle(img, (0, shoeMaxY - distShoeStair), (width - 1, shoeMaxY - distShoeStair + 1), (0, 127, 127), 2)

#    if distShoeStair < edgeArea:
#        safety = False
##    else:
#        safety = True
    print(safety, distShoeStair)
    if safety == False:
#        warningCount += 1

#        if warningCount > WARNINGTHRESHOLD:
        cv2.putText(img, 'Warning!', (0, int(height / 15)), font, 3, (0, 0, 255), 3, cv2.LINE_AA)
#    else:
#        warningCount = 0

    cv2.putText(img, str(distShoeStair), (int(width * 13 / 15), int(height / 15)), font, 3, (255, 0, 0), 3, cv2.LINE_AA)

    endMAIN = time.time()
    #plt.subplot(111), plt.imshow(img), plt.show()
    imgSet.append(img)

    success, img = inVideo.read()

    avgTime += endMAIN - startMAIN

    imgCount += 1
# end) main #################################################################

print('main >>', avgTime / (imgCount + 1))

# wait for saving images
while True:
    time.sleep(0.1)

    if seeker == imgCount:
        break

    print(seeker, imgCount) # print(or compare) current status of saving images

complete = True # for killing thread

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()
