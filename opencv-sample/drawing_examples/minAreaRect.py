import numpy as np
import cv2

img = np.zeros((512, 512, 3), np.uint8)
cnt = np.random.randint(0, 100, (20, 2))
print(cnt)
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

cv2.imshow("img", img)

k = cv2.waitKey(0)