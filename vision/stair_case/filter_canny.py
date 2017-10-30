import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread(sys.argv[1], 0)
#amount of blur is controlled by third and forth parameters
blur = cv2.bilateralFilter(img,5,60,60)
edges = cv2.Canny(blur, 50, 100)

cv2.imwrite('blur.jpg', blur)
cv2.imwrite('result.jpg', edges)

#plt.subplot(121), plt.imshow(img, cmap = 'gray')
#plt.title('Orgin'), plt.xticks([]), plt.yticks([])

#plt.subplot(122), plt.imshow(blur, cmap = 'gray')
#plt.title('filtered'), plt.xticks([]), plt.yticks([])

