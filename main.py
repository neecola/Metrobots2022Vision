from xmlrpc.client import Server
import cv2
import numpy as np
import math
from enum import Enum
import datetime
from ball_processing import BallProcessing
import general_settings as g_sets
from tape_processing import TapeProcessing
from networktables import NetworkTables
import os

os.system("v4l2-ctl -c exposure_auto=1")

if __name__ == "__main__":

    settings = BallProcessing(g_sets.TEAM)
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    video.set(cv2.CAP_PROP_EXPOSURE, 0)
    #assert video.set(cv2.CAP_PROP_EXPOSURE, 0) is not False, 'Error: Camera does not support exposure'      

    while True:
        # for timing the process #
        #begin_time = datetime.datetime.now()

        # gets frame and resizes it #
        #_, frame = video.read()
        
        frame = cv2.imread('2022VisionSampleImages/FarLaunchpad10ft10in.png')
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

        




        # now tape #
        tape = TapeProcessing().process(frame)       

        try:
            rect = cv2.minAreaRect(tape)
            tape_coords, tape_dims, _ = rect
            
            
            # getting hub angle #
            tape_x, _ = tape_coords
            print(tape_x)
            tape_x -= (g_sets.FRAME_SIZE_WIDTH/2) #SETS CENTER TO 0
            
            
            
            
            # getting hub distance #
            tape_width, _ = tape_dims
            tape_dist_diag = g_sets.TAPE_ACTUAL_WIDTH * g_sets.CAMERA_FOCAL_LENGTH / tape_width
            tape_dist_horz = math.cos(g_sets.TAPE_CAMERA_ANGLE) * tape_dist_diag
        except :
            tape_coords = None
        
        #tape_x, tape_y = tape_coords
        
        #print(tape_x)
        #print(tape_dist_hz)


        #NetworkTables.initialize(server=g_sets.ROBO_RIO_ADDRESS)
        #sd = NetworkTables.getTable('SmartDashboard')
        #sd.putNumber('hubAngle', tape_angle)
        
        #print(tape_coords)
        

        # start networktables client
        sd = NetworkTables.getTable('SmartDashboard')
        NetworkTables.startClientTeam(3324)
        NetworkTables.startClient(Server)
        NetworkTables.initialize(server=g_sets.ROBO_RIO_ADDRESS)

        # push videos to smartdashboard (ball and tape as well for debugging)
        sd.putNumberArray("VideoFeed", video)
        sd.putNumberArray("BallProcessing", ball)
        sd.putNumberArray("TapeProcessing", tape)
        sd.putNumber("CenterOfBall", M)

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