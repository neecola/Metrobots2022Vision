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


if __name__ == "__main__":

    #os.system("v4l2-ctl -c exposure_auto=1")
    settings = BallProcessing(g_sets.TEAM)
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    video.set(cv2.CAP_PROP_EXPOSURE, 0)
    #assert video.set(cv2.CAP_PROP_EXPOSURE, 0) is not False, 'Error: Camera does not support exposure'      

    while True:


        # gets frame and resizes it #
        #_, frame = video.read()
        
        frame = cv2.imread('2022VisionSampleImages/FarLaunchpad10ft10in.png')
        frame = cv2.resize(
            frame, (g_sets.FRAME_SIZE_WIDTH, g_sets.FRAME_SIZE_HEIGHT))





        # tape #
        tape = TapeProcessing().process(frame)       

        try:
            rect = cv2.minAreaRect(tape)
            tape_coords, tape_dims, _ = rect
            
            
            # getting hub angle #
            tape_x, _ = tape_coords
            print(tape_x)
            tape_x -= (g_sets.FRAME_SIZE_WIDTH/2) #SETS CENTER TO 0
            
            
            # getting hub distance (not needed hopegfully) #
            #tape_width, _ = tape_dims
            #tape_dist_diag = g_sets.TAPE_ACTUAL_WIDTH * g_sets.CAMERA_FOCAL_LENGTH / tape_width
            #tape_dist_horz = math.cos(g_sets.TAPE_CAMERA_ANGLE) * tape_dist_diag
        except :
            tape_coords = None
        
        
        
        blank_image = np.zeros([g_sets.FRAME_SIZE_HEIGHT, g_sets.FRAME_SIZE_WIDTH, 3])
        image = cv2.drawContours(blank_image, tape, -1, (255, 255, 255))
        
        cv2.imshow('just tape', image)
        
        
        cv2.imshow('tape', image)
        cv2.waitKey(5)

        # start networktables client
        # sd = NetworkTables.getTable('SmartDashboard')
        # NetworkTables.startClientTeam(3324)
        # NetworkTables.startClient(Server)
        # NetworkTables.initialize(server=g_sets.ROBO_RIO_ADDRESS)

        # # push videos to smartdashboard (ball and tape as well for debugging)
        # sd.putNumberArray("VideoFeed", video)
        # sd.putNumberArray("BallProcessing", ball)
        # sd.putNumberArray("TapeProcessing", tape)
        # sd.putNumber("CenterOfBall", M)

        #sd.putNumber('ball_x', ball_x)
        #sd.putNumber('ball_y', ball_y)
        #sd.putNumber('tape_x', tape_x)
        #sd.putNumber('tape_y', tape_y)


        
        cv2.waitKey(5)
        #for displaying the cameras' content / turn on from general settings
        if g_sets.Calibration.is_on:
            g_sets.Calibration.display_screens()