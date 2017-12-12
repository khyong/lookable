import sys
import cv2
import numpy as np

# point and percentage are hyperparameter
point = 50
percentage = 60
imgCount = 0

video = cv2.VideoCapture(sys.argv[1])

success, image = video.read()

while success:
    lineChecker = 0

    success, image = video.read()

    edges = cv2.Canny(image, 40, 80)
    height, width = edges.shape[:2]

    checkpoint = height * point / 100
    checkpoint = np.rint(checkpoint)
    checkpoint = int(checkpoint)

    for seeker in range(0, width - 1):
        if edges[checkpoint][seeker] > 100:
            lineChecker += 1
    
    cv2.imwrite("../video/noblur/frame%d,%d.jpg" % (imgCount, lineChecker), edges)     # save frame as JPEG file

    imgCount += 1