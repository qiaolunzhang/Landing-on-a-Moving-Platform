# USAGE
# python drone.py --video FlightDemo.mp4

# import the necessary packages
import cv2

# load the video
camera = cv2.VideoCapture('test.mp4')

# keep looping
while True:
    # grab the current frame and initialize the status text
    (grabbed, frame) = camera.read()
    status = "No Targets"

    # check to see if we have reached the end of the
    # video
    if not grabbed:
        break

    bilateral_filtered_image = cv2.bilateralFilter(frame, 5, 175, 175)

    edged = cv2.Canny(bilateral_filtered_image, 75, 200)

    # convert the frame to grayscale, blur it, and detect edges
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    #edged = cv2.Canny(blurred, 50, 150)

    # find contours in the edge map
    # hierarchy: an array of four values : [Next, Previous, First_Child, Parent]
    _, cnts, hierarchy_original = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    try:
        hierarchy = hierarchy_original[0]
        index_contours = 0
        h_list = []
        for component in zip(cnts, hierarchy):
            currentContour = component[0]
            currentHierarchy = component[1]
            print(currentHierarchy)
            if currentHierarchy[2] < 0:
                if currentHierarchy[3] > 0:
                    print("ok")
                    c = cnts[index_contours]
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                    area = cv2.contourArea(c)

                    if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
                        h_list.append(c)


                    cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                    status = "Target(s) Acquired"

                    # compute the center of the contour region and draw the
                    # crosshairs
                    M = cv2.moments(approx)
                    (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                    (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                    cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
                    cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)
            index_contours = index_contours + 1

        # draw the status text on the frame
        cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (0, 0, 255), 2)

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