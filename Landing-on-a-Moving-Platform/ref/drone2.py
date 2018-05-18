# USAGE
# python drone.py --video FlightDemo.mp4

# import the necessary packages
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

# load the video
camera = cv2.VideoCapture(args["video"])


class ShapeRecognition():
    def __init__(self, img):
        self.img = img
        self.edged = self.pre_processsing()
        self.circle_list = []
        self.inner_most_list = []
        self.h_list = []

    def pre_processsing(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 50, 150)
        cv2.imshow('edged', edged)
        return edged

    def find_inner_most(self):
        # hierarchy: an array of four values : [Next, Previous, First_Child, Parent]
        im2, contours, hierarchy = cv2.findContours(self.edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        index = 0
        hierarchy = hierarchy[0]
        for component in zip(contours, hierarchy):
            currentContour = component[0]
            currentHierarchy = component[1]
            print(currentHierarchy[2])
            if currentHierarchy[2] < 0:
                if currentHierarchy[3] > 0:
                    self.inner_most_list.append([currentContour, index])

                    c = contours[index]
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                    area = cv2.contourArea(c)

                    if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
                        self.h_list.append(c)

            index = index + 1

        cv2.drawContours(self.img, self.h_list, -1, (255, 0, 0), 2)
        cv2.imshow("inner_most", self.img)

    # @todo 找出inner most的parent，其实hierarchy中第三，第4个 参数已经可以做了
    def find_parent_of_inner_most(self):
        pass

    def find_center(self):
        pass

    # 首先把所有的点分类，然后计算类别
    def find_h(self, contour):
        point_list = []
        distance_list = []
        for i in range(len(contour)):
            # point_list.append([])
            # for j in range(contour):
            #    point_list[i].append(distance)
            point_list.append(contour[i][0])
        for i in range(len(contour)):
            distance_list.append([])
            for j in range(len(contour)):
                (distance_list[i]).append(distance(point_list[i], point_list[j]))
        print("len(sistance_list)", len(distance_list))
        return distance_list
        # 计算第一个点和其他点之间的距离

    def find_rectangle(self):
        im2, contours, hierarchy = cv2.findContours(self.edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # loop over our contours
        for c in contours:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            area = cv2.contourArea(c)

            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            """
            if len(approx) == 4:
                screenCnt = approx
                cv2.drawContours(self.img, [screenCnt], -1, (0, 255, 0), 3)
                cv2.drawContours(self.img, [screenCnt], -1, (0, 255, 0), 3)
            if (len(approx) > 8):
                self.circle_list.append(c)
            """
            if (len(approx) == 16):
                print(approx)
                for i in range(len(approx)):
                    cv2.circle(self.img, tuple(approx[i][0]), 3, [0, 255, 0], -1)
                print(approx[0])
                # @todo find ddistance还需要改，这里返回的结果似乎至于一个列表
                # print("distance list", self.find_h(c))
            if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
                self.circle_list.append(c)
        print(len(self.circle_list))
        cv2.drawContours(self.img, self.circle_list, -1, (255, 0, 0), 2)
        cv2.imshow("find_rectangle", self.img)


# keep looping
while True:
    # grab the current frame and initialize the status text
    (grabbed, frame) = camera.read()
    # status = "No Targets"

    # check to see if we have reached the end of the
    # video
    if not grabbed:
        break

    frame_class = ShapeRecognition(frame)
    frame_class.find_inner_most()

cv2.waitKey(0)
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
