import numpy as np
import cv2
import time
import threading

inVideo = cv2.VideoCapture('../origin.avi')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

complete = False
imgCount = 0
seeker = 0
imgSet = []

# take first frame of the video
success, img = inVideo.read()
height, width = img.shape[:2]

tracker = cv2.MultiTracker_create()

# setup initial location of window
x1, y1, w1, h1 = 720, 870, 940 - 720, 1080 - 870  # simply hardcoded the values
x2, y2, w2, h2 = 1050, 840, 1250 - 1050, 1025 - 840
box1 = (x1, y1, w1, h1)
box2 = (x2, y2, w2, h2)

tracker.add(cv2.TrackerBoosting_create(), img, box1)
tracker.add(cv2.TrackerBoosting_create(), img, box2)

def saveImg():
    global seeker
    global imgSet

    while True:
        while True:
            time.sleep(0.2)
            if complete or (len(imgSet) > 0):
                break

        if complete:
            break

        img = imgSet[seeker]

        cv2.imwrite('../tracking/test%d.png' % seeker, img)

        seeker += 1

        print('saveImg >> write Img %d' %seeker)

def multiTracking(img):
    global box

    box = tracker.update(img)

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


t = threading.Thread(target = saveImg)

t.start()

avgTime = 0

while success:
    startTime = time.time()

    multiTracking(img)

    # draw shoes
    for pt in box:
        cv2.rectangle(img, (int(pt[0]), int(pt[1])), (int(pt[0] + pt[2]), int(pt[1] + pt[3])), (0, 0, 255), 2)

    # draw stair
    
    endTime = time.time()

    print('main >>', imgCount)
    imgSet.append(img)

    success, img = inVideo.read()

    avgTime += endTime - startTime

    imgCount += 1

print(avgTime / (imgCount + 1))

# write video
outVideo = cv2.VideoWriter('../tracking_v0.3.avi', fourcc, 25, (width, height))

while True:
    if seeker == imgCount:
        break

    print(seeker, imgCount)

complete = True

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()
