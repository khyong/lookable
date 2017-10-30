import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images.jpg', 0)
blur = cv2.bilateralFilter(img,5,25,25)

cv2.imwrite('test.jpg', blur)

plt.subplot(121), plt.imshow(img, cmap = 'gray')
plt.title('Orgin'), plt.xticks([]), plt.yticks([])

plt.subplot(122), plt.imshow(blur, cmap = 'gray')
plt.title('filtered'), plt.xticks([]), plt.yticks([])

