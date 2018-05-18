# import the necessary packages
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

# load the video
camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    # grab the current frame and initialize the status text
    (grabbed, frame) = camera.read()
    status = "No Targets"

    # check to see if we have reached the end of the video
    if not grabbed:
        break

    # convert the frame to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred =cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)

    # find contours in the edge map
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

