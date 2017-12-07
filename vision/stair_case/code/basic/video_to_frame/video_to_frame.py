import cv2
import numpy as np
import sys

# point and percentage are hyperparameter
point = 50
percentage = 60
sigma = 30
radius = 4
imgCount = 0

video = cv2.VideoCapture(sys.argv[1])

success, image = video.read()

while success:
    lineChecker = 0

    success, image = video.read()

    blur = cv2.bilateralFilter(image, radius, sigma, sigma)
    edges = cv2.Canny(blur, 100, 200)
    height, width = edges.shape[:2]

    checkpoint = height * point / 100
    checkpoint = np.rint(checkpoint)
    checkpoint = int(checkpoint)

    for seeker in range(0, width - 1):
        if edges[checkpoint][seeker] > 100:
            lineChecker += 1

    if(lineChecker > (width * percentage / 100)):
        cv2.imwrite("../video/frame%d.jpg" % imgCount, image)

    imgCount += 1