import cv2
import numpy
import math
from enum import Enum
import blue_settings as blue_s
import red_settings as red_s
import tape_settings as tape_s


if __name__ == "__main__":
    while True:
        gplr = GripPipelineRed()
        video = cv2.VideoCapture(0)
        redval, redimg = video.read()

        contours = gplr.process(redimg) 
        cv2.drawContours(redimg, contours, -1, 0xFF0000)
        cv2.imshow("Source with contours", redimg)
        #cv2.imshow("Contours", contours)
        cv2.waitKey(5)