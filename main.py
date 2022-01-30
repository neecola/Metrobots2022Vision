import cv2
import numpy as np
import math
from enum import Enum
import datetime
from ball_processing import BallProcessing
import general_settings as g_sets
from tape_processing import TapeProcessing
    

if __name__ == "__main__":

    settings = BallProcessing(g_sets.team)

    while True:
        # for timing the process #
        #begin_time = datetime.datetime.now()

        # getting the video signal from the camera #
        video = cv2.VideoCapture(0)
        _, frame = video.read()
        
        # using picture as video signal for testing #
        #frame = cv2.imread("2022VisionSampleImages/NearLaunchpad5ft4in.png")
        
        frame = cv2.resize(
            frame, (g_sets.frame_size_width, g_sets.frame_size_height))

        ball = settings.process(frame)


        # finding center of the ball #
        M = cv2.moments(ball)
        try:
            cX = int(M['m10'] / M['m00']) - (g_sets.frame_size_width/2)
            cY = abs(int(M['m01'] / M['m00']) -
                     g_sets.frame_size_height) - (g_sets.frame_size_height / 2)
            ctr_coords = (cX, cY)
        except ZeroDivisionError:
            ctr_coords = None

        #print(ctr_coords)


        # now tape #
        tape = TapeProcessing().process(frame)       

        try:
            rect = cv2.minAreaRect(tape)
            tape_coords, _, _ = rect
        except :
            tape_coords = None
        print(tape_coords)
        print(tape_coords)
        
        # for timing the process #
        #print(datetime.datetime.now() - begin_time)

        cv2.waitKey(5)
        #for displaying the cameras' content / turn on from general settings
        if g_sets.Calibration.is_on:
            g_sets.Calibration.display_screens()