import cv2
import numpy as np
from matplotlib import pyplot as plt

# read image
img = cv2.imread('../picture/2.png')
blur = cv2.bilateralFilter(img, 5, 100, 100)
edge = cv2.Canny(blur, 100, 200)
h, w = img.shape[:2]

shoeW, shoeH = int(w * 0.08), int(h * 0.08)

edgeSum = []

for i in range(0, h):
    temp = []
    valueSum = 0
    
    for j in range(0, w):
        valueSum += edge[i][j]
        
        if i == 0:
            temp.append(valueSum)
        else:
            temp.append(valueSum + edgeSum[i - 1][j])
    
    edgeSum.append(temp)

footSum = edgeSum[285 + shoeH][295 + shoeW] - edgeSum[285][295 + shoeW] - edgeSum[285 + shoeH][295] + edgeSum[285][295]

#min_val
x = []
y = []

for i in range(0, h - shoeH):
    for j in range(0, w - shoeW):
        val = edgeSum[i + shoeH][j + shoeW] - edgeSum[i][j + shoeW] - edgeSum[i + shoeH][j] + edgeSum[i][j]
        
        if ((footSum * 1) >= val) & ((footSum * 1) <= val):
            x.append(i)
            y.append(j)
            print(footSum, val, i, j)

for i in range(0, len(x)):
    cv2.rectangle(img, (x[i], y[i]), (x[i] + shoeW, y[i] + shoeH), (0, 255, 0), 2)

cv2.imwrite('../test.png', img)
