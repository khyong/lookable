import cv2
import numpy as np

img = cv2.imread('asd.png', 0)

kernel = np.ones((5, 5), np.float32) / 25
filt_img = cv2.filter2D(img, -1, kernel)

plt.subplot(121), plt.imshow(img, cmap = 'gray')
plt.title('Orgin'), plt.xticks([]), plt.yticks([])

plt.subplot(122), plt.imshow(filt_img, cmap = 'gray')
plt.title('filtered'), plt.xticks([]), plt.yticks([])