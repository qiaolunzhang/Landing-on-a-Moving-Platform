import cv2

img = cv2.imread('./data/mark_original.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(blurred, 50, 150)

cv2.imshow("edged", edged)

cv2.imwrite('output.jpg', edged)