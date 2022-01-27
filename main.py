import cv2
import numpy
import math
from enum import Enum
import datetime
from ball_processing import BallProcessing
import tape_settings
from general_settings import team


if __name__ == "__main__":

    settings = BallProcessing(team)

    while True:
        # for timing the process
        #begin_time = datetime.datetime.now()

        # capturing balls and getting the contours
        video = cv2.VideoCapture(0)
        
        
        _, video = video.read()

        ball = settings.process(video)
        

        M = cv2.moments(ball)

        #print(M)
        #cv2.imshow("Video", video)
        #cv2.imshow("Detected Ball", ball)


        # finding center of the ball (just copy-pasted, don't know what it actually does)
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])

        print(f'Coordinates of the center: ({cX},{cY})')

        #cv2.imshow("Source with contours", image)
        #cv2.imshow("Contours", contours)


        # for timing the process
        #print(datetime.datetime.now() - begin_time)

        cv2.waitKey(5)
