import cv2
import numpy
import math
from enum import Enum
from ball_processing import BallProcessing
import tape_settings
from general_settings import team

if __name__ == "__main__":
    
    settings = BallProcessing(team)

    while True:
        

        #capturing balls and getting the contours
        video = cv2.VideoCapture(0)
        ret, frame = video.read()
        video2 = cv2.resize(frame, (640, 320))
        ball = settings.process(frame)
        
        M = cv2.moments(ball)

        cv2.imshow("Video", video2)
        cv2.imshow("Detected Ball", ball)

        #finding center of the ball (just copy-pasted, don't know what it actually does)
        #cX = int(M["m10"] / M["m00"])
        #cY = int(M["m01"] / M["m00"])

        #print(f'Coordinates of the center: ({cX},{cY})')


        #cv2.imshow("Source with contours", image)
        #cv2.imshow("Contours", contours)
        cv2.waitKey(5)