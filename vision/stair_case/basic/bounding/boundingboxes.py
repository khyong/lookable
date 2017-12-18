import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('../picture/2.png')
blur = cv2.bilateralFilter(img, 5, 100, 100)
edge = cv2.Canny(blur, 100, 200)

image, contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    # get the bounding rect
    x, y, w, h = cv2.boundingRect(c)
    # draw a green rectangle to visualize the bounding rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
    # get the min area rect
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    # convert all coordinates floating point values to int
    box = np.int0(box)
    # draw a red 'nghien' rectangle
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

cv2.imwrite('../picture/edge_box.jpg', img)
