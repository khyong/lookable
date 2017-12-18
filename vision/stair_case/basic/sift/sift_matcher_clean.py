import cv2
import numpy as np
from matplotlib import pyplot as plt

# read template and image and convert RGB to Gray
tem = cv2.imread('../picture/temp.png')
img = cv2.imread('../picture/2.png')

# init SIFT
sift = cv2.xfeatures2d.SIFT_create()

# get keypoints of template and image
temKp, temDes = sift.detectAndCompute(tem, None)
imgKp, imgDes = sift.detectAndCompute(img, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(check = 50) # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(temDes, imgDes, k = 2)

matchesMask = [[0, 0] for i in range(len(matches))]

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 1.1 * n.distance:
        matchesMask[i] = [1, 0]

draw_params = dict(matchColor = (0, 255, 0), singlePointColor = (255, 0, 0),
    matchesMask = matchesMask, flags = 0)
 
# draw
result = cv2.drawMatchesKnn(tem, temKp, img, imgKp, matches, None, **draw_params)
cv2.imwrite('../picture/sift_match.jpg', result)

#plt.imshow(result), plt.show()

#img=cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#cv2.imwrite('../picture/sift_test.jpg',img)