import cv2
import numpy as np
from matplotlib import pyplot as plt

#img = cv2.imread('images.jpg', 0)
img = cv2.imread('../picture/2.png', 0)
blur = cv2.bilateralFilter(img, 5, 100, 100)
edges = cv2.Canny(blur, 100, 200)

cv2.imwrite('../picture/temp.jpg', edges)

plt.subplot(121), plt.imshow(img, cmap = 'gray')
plt.title('Orgin'), plt.xticks([]), plt.yticks([])

plt.subplot(122), plt.imshow(edges, cmap = 'gray')
plt.title('edge'), plt.xticks([]), plt.yticks([])
