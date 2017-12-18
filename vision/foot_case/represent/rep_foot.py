import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
THRESHOLD = 0.9

foot = cv2.imread('../foot.png')
img = cv2.imread('../search/test0.png')

footH, footW = foot.shape[:2]
imgH, imgW = img.shape[:2]

footEdge = cv2.bilateralFilter(foot, 4, 80, 80)
footEdge = cv2.Canny(footEdge, 50, 100)

imgEdge = cv2.bilateralFilter(img, 4, 80, 80)
imgEdge = cv2.Canny(imgEdge, 50, 100)

footVal = np.sum(footEdge)

edgeSum = []
start = time.time()
for i in range(0, imgH):
    temp = []
    valueSum = 0
    
    for j in range(0, imgW):
        valueSum += imgEdge[i][j]
        
        if i == 0:
            temp.append(valueSum)
        else:
            temp.append(valueSum + edgeSum[i - 1][j])
    
    edgeSum.append(temp)
end = time.time()
print(end - start)
x = []
y = []
start = time.time()
for i in range(0, imgH - footH):
    for j in range(0, imgW - footW):
        val = edgeSum[i + footH][j + footW] - edgeSum[i][j + footW] - edgeSum[i + footH][j] + edgeSum[i][j]
        
        #if ((footSum * 1) >= val) & ((footSum * 1) <= val):
        if footVal == val:
            x.append(j)
            y.append(i)
            #print(j, i)

end = time.time()
print(end - start)

for i in range(0, len(x)):
    cv2.rectangle(img, (x[i], y[i]), (x[i] + footW, y[i] + footH), (0, 255, 0), 2)

cv2.imwrite('../test.png', img)
