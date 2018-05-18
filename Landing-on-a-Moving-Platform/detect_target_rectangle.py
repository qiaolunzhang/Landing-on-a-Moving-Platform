# USAGE
# python drone.py --video FlightDemo.mp4

# import the necessary packages
import cv2

standard_path = "./data/mark.jpg"
video_path = "../video/test.mp4"

sift = cv2.xfeatures2d.SIFT_create()

## Create flann matcher
FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#matcher = cv2.FlannBasedMatcher_create()
matcher = cv2.FlannBasedMatcher(flann_params, {})

## Detect and compute
img1 = cv2.imread(standard_path)
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
kpts1, descs1 = sift.detectAndCompute(gray1,None)

# load the video
camera = cv2.VideoCapture(video_path)

# keep looping
while True:
    # grab the current frame and initialize the status text
    (grabbed, frame) = camera.read()
    status = "No Targets"

    # check to see if we have reached the end of the
    # video
    if not grabbed:
        break

    ## as up
    gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kpts2, descs2 = sift.detectAndCompute(gray2, None)

    try:
        matches = matcher.knnMatch(descs1, descs2, 2)
        matchesMask = [[0, 0] for i in range(len(matches))]
        pt2_list = []
        for i, (m1, m2) in enumerate(matches):
            if m1.distance < 0.7 * m2.distance:
                matchesMask[i] = [1, 0]
                ## Notice: How to get the index
                pt1 = kpts1[m1.queryIdx].pt
                pt2 = kpts2[m1.trainIdx].pt
                print(i, pt1, pt2)
                if i % 5 == 0:
                    ## Draw pairs in purple, to make sure the result is ok
                    cv2.circle(img1, (int(pt1[0]), int(pt1[1])), 5, (255, 0, 255), -1)
                    cv2.circle(frame, (int(pt2[0]), int(pt2[1])), 5, (255, 0, 255), -1)
                    pt2_list.append(pt2)
        x_min = pt2_list[0][0]
        x_max = pt2_list[0][0]
        y_min = pt2_list[0][1]
        y_max = pt2_list[0][1]
        for point in pt2_list:
            if point[0] < x_min:
                x_min = point[0]
            elif point[0] > x_max:
                x_max = point[0]

            if point[1] < y_min:
                y_min = point[1]
            elif point[1] > y_max:
                y_max = point[1]
        print("Now point is", x_min, y_min)

        """
        shape_pic = frame.shape
        if x_max >= shape_pic[0]:
            x_max = shape_pic[0]
        if y_max >
        """

        #cv2.rectangle(frame, (x_min, y_min), (y_min, y_max), (0, 255, 0), 5)
        cv2.rectangle(frame, (0, 0), (20, 20), (0, 255, 0), 5)
        #@todo find the top left point

        #@todo find the bottom right point

        # show the frame and record if a key is pressed
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
    except:
        continue

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()