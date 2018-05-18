import numpy as np
import cv2
from matplotlib import pyplot as plt
#imgname = "box.jpg"          # query image (large scene)
#imgname2 = "box_in_scene.jpg"   # train image (small object)
imgname = "small.png"
imgname2 = "big.png"

## Create SIFT object
sift = cv2.xfeatures2d.SIFT_create()

## Create flann matcher
FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#matcher = cv2.FlannBasedMatcher_create()
matcher = cv2.FlannBasedMatcher(flann_params, {})

## Detect and compute
img1 = cv2.imread(imgname)
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
kpts1, descs1 = sift.detectAndCompute(gray1,None)

## As up
img2 = cv2.imread(imgname2)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
kpts2, descs2 = sift.detectAndCompute(gray2,None)

## Ratio test
matches = matcher.knnMatch(descs1, descs2, 2)
matchesMask = [[0,0] for i in range(len(matches))]
for i, (m1,m2) in enumerate(matches):
    if m1.distance < 0.7 * m2.distance:
        matchesMask[i] = [1,0]
        ## Notice: How to get the index
        pt1 = kpts1[m1.queryIdx].pt
        pt2 = kpts2[m1.trainIdx].pt
        print(i, pt1,pt2 )
        if i % 5 ==0:
            ## Draw pairs in purple, to make sure the result is ok
            cv2.circle(img1, (int(pt1[0]),int(pt1[1])), 5, (255,0,255), -1)
            cv2.circle(img2, (int(pt2[0]),int(pt2[1])), 5, (255,0,255), -1)


cv2.imshow("img1", img1)
cv2.imshow("img2", img2)
"""
## Draw match in blue, error in red
draw_params = dict(matchColor = (255, 0,0),
                   singlePointColor = (0,0,255),
                   matchesMask = matchesMask,
                   flags = 0)

res = cv2.drawMatchesKnn(img1,kpts1,img2,kpts2,matches,None,**draw_params)
cv2.imshow("Result", res);
"""
cv2.waitKey()
cv2.destroyAllWindows()
