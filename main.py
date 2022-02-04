import cv2
import numpy as np
import math
from enum import Enum
import datetime
from ball_processing import BallProcessing
import general_settings as g_sets
from tape_processing import TapeProcessing
from networktables import NetworkTables


if __name__ == "__main__":

    settings = BallProcessing(g_sets.TEAM)

    while True:
        # for timing the process #
        #begin_time = datetime.datetime.now()

        # getting the video signal from the camera #
        video = cv2.VideoCapture(0)
        print(video.set(cv2.CAP_PROP_EXPOSURE,1))
        
        
        
        _, frame = video.read()
        
        
        # using picture as video signal for testing #
        #frame = cv2.imread("2022VisionSampleImages/NearLaunchpad5ft4in.png")
        
        frame = cv2.resize(
            frame, (g_sets.FRAME_SIZE_WIDTH, g_sets.FRAME_SIZE_HEIGHT))

        ball = settings.process(frame)


        # finding center of the ball #
        M = cv2.moments(ball)
        try:
            cX = int(M['m10'] / M['m00']) - (g_sets.FRAME_SIZE_WIDTH/2)
            cY = abs(int(M['m01'] / M['m00']) -
                     g_sets.FRAME_SIZE_HEIGHT) - (g_sets.FRAME_SIZE_HEIGHT / 2)
            ball_coords = (cX, cY)
        except ZeroDivisionError:
            ball_coords = None

        #print(ball_coords)

        #ball_x, ball_y = ball_coords

        # now tape #
        tape = TapeProcessing().process(frame)       

        try:
            rect = cv2.minAreaRect(tape)
            tape_coords, _, _ = rect
        except :
            tape_coords = None
        
        #print(tape_coords)
        
        #tape_x, tape_y = tape_coords


        NetworkTables.initialize(server=g_sets.ROBO_RIO_ADDRESS)
        sd = NetworkTables.getTable('SmartDashboard')

        #sd.putNumber('ball_x', ball_x)
        #sd.putNumber('ball_y', ball_y)
        #sd.putNumber('tape_x', tape_x)
        #sd.putNumber('tape_y', tape_y)


        # for timing the process #
        #print(datetime.datetime.now() - begin_time)

        cv2.waitKey(5)
        #for displaying the cameras' content / turn on from general settings
        if g_sets.Calibration.is_on:
            g_sets.Calibration.display_screens()