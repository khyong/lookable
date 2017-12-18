import numpy as np
import cv2

inVideo = cv2.VideoCapture('../origin.avi')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# take first frame of the video
success, img = inVideo.read()
height, width = img.shape[:2]

tracker1 = cv2.TrackerBoosting_create()
tracker2 = cv2.TrackerBoosting_create()
temp1 = cv2.TrackerBoosting_create()
temp2 = cv2.TrackerBoosting_create()

# setup initial location of window
x1, y1, w1, h1 = 720, 870, 940 - 720, 1080 - 870  # simply hardcoded the values
x2, y2, w2, h2 = 1050, 840, 1250 - 1050, 1025 - 840
box1 = (x1, y1, w1, h1)
box2 = (x2, y2, w2, h2)

tracker1.init(img, box1)
tracker2.init(img, box2)
temp1.init(img, box1)
temp2.init(img, box2)

imgCount = 0

imgSet = []

while success:
    success1, tempbox1 = temp1.update(img)
    success2, tempbox2 = temp2.update(img)

    if (tempbox1[0] + tempbox1[2] - tempbox2[0]) < 50:
        if (tempbox1[0] + tempbox1[2]) < (width / 2):
            tracker1.update(img)
            box1 = tempbox1
        else:
            temp1.init(img, box1)
            
        if tempbox2[0] > (width / 2):
            tracker2.update(img)
            box2 = tempbox2
        else:
            temp2.init(img, box2)
            

    if success1:
        cv2.rectangle(img, (int(box1[0]), int(box1[1])), (int(box1[0] + box1[2]), int(box1[1] + box1[3])), (0, 255, 0), 2)
    if success2:
        cv2.rectangle(img, (int(box2[0]), int(box2[1])), (int(box2[0] + box2[2]), int(box2[1] + box2[3])), (0, 255, 0), 2)

    imgSet.append(img)

    cv2.imwrite('../tracking/test%d.png' %imgCount, img)

    imgCount += 1

    success, img = inVideo.read()

    print(imgCount)

# write video
outVideo = cv2.VideoWriter('../tracking.avi', fourcc, 25, (width, height))

# writing video from images
for i in range(len(imgSet)):
    outVideo.write(imgSet[i])

inVideo.release()
outVideo.release()
