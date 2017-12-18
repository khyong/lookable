# v0.2 is just drawing rectangle to the hightest value of y aixs
#   => fail
# v0.2 is matching the pattern
THRESHOLD = 0.25

import cv2
import numpy as np
from matplotlib import pyplot as plt

# read image
img = cv2.imread('../picture/2.png')
blur = cv2.bilateralFilter(img, 5, 100, 100)
edge = cv2.Canny(blur, 100, 200)
h, w = img.shape[:2]

footEdge = cv2.imread('../picture/footEdge.png', 0 )
shoeH, shoeW = footEdge.shape[:2]

result = []

for img_i in range(0, h - shoeH):
    for img_j in range(0, w - shoeW):
        product = 0

        for tem_i in range(0, shoeH):
            for tem_j in range(0, shoeW):
                product = footEdge[tem_i][tem_j] * edge[img_i + tem_i][img_j + tem_j]
                
        result.append([product, img_i, img_j])

        
cv2.imwrite('../test.png', img)
