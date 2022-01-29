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
        blank_image = np.zeros([g_sets.frame_size_height, g_sets.frame_size_width, 3])
        
        

        try:
            M = cv2.moments(tape)
            
            tX = int(M['m10'] / M['m00']) - (g_sets.frame_size_width/2)
            tY = abs(int(M['m01'] / M['m00']) -
                     g_sets.frame_size_height) - (g_sets.frame_size_height / 2)
            tape_coords = (tX, tY)
        except:# ZeroDivisionError:
            tape_coords = None

        
        
        # for timing the process #
        #print(datetime.datetime.now() - begin_time)

        cv2.waitKey(5)
        #for displaying the cameras' content / turn on from general settings
        if g_sets.Calibration.is_on:
            g_sets.Calibration.display_screens()