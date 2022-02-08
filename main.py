from cmath import sqrt
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
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    video.set(cv2.CAP_PROP_EXPOSURE, 0)
    #assert video.set(cv2.CAP_PROP_EXPOSURE, 0) is not False, 'Error: Camera does not support exposure'      

    while True:
        # for timing the process #
        #begin_time = datetime.datetime.now()

        # gets frame and resizes it #
        _, frame = video.read()
        frame = cv2.resize(
            frame, (g_sets.FRAME_SIZE_WIDTH, g_sets.FRAME_SIZE_HEIGHT))



        ball = settings.process(frame)


        # finding center of the ball #
        m = cv2.moments(ball)
        try:
            cX = int(m['m10'] / m['m00']) - (g_sets.FRAME_SIZE_WIDTH/2)
            cY = abs(int(m['m01'] / m['m00']) -
                     g_sets.FRAME_SIZE_HEIGHT) - (g_sets.FRAME_SIZE_HEIGHT / 2)
            ball_coords = (cX, cY)
        except ZeroDivisionError:
            ball_coords = None

        #ball_x, ball_y = ball_coords
        #print(ball_coords)




        # now tape #
        tape = TapeProcessing().process(frame)       

        try:
            rect = cv2.minAreaRect(tape)
            tape_coords, tape_dims, _ = rect
            
            
            # getting hub angle #
            tape_x, _ = tape_coords
            tape_x -= (g_sets.FRAME_SIZE_WIDTH/2) #SETS CENTER TO 0
            tape_angle = tape_x * g_sets.CAMERA_VIEW_ANGLE_HOR / g_sets.FRAME_SIZE_WIDTH
            
            
            
            # getting hub distance #
            tape_width, _ = tape_dims
            tape_dist_diag = g_sets.TAPE_ACTUAL_WIDTH * g_sets.CAMERA_FOCAL_LENGTH / tape_width
            
            # hz distance with cos#
            #tape_dist_hz = math.cos(g_sets.TAPE_CAMERA_ANGLE) * tape_dist_diag
            
            # hz distance with pythagorean theorem #
            tape_dist_hz = sqrt(tape_dist_diag**2 - (g_sets.HUB_ACTUAL_HEIGHT - g_sets.CAMERA_HEIGTH_ON_GROUND)**2)
        except :
            tape_angle = None
        
        


        NetworkTables.initialize(server=g_sets.ROBO_RIO_ADDRESS)
        sd = NetworkTables.getTable('SmartDashboard')
        sd.putNumber('hubAngle', tape_angle)
        
        
        #sd.putNumber('ball_x', ball_x)
        #sd.putNumber('ball_y', ball_y)
        #sd.putNumber('tape_x', tape_x)
        #sd.putNumber('tape_y', tape_y)


        # for timing the process #
        #print(datetime.datetime.now() - begin_time)

        
        #for displaying the cameras' content / turn on from general settings
        if g_sets.Calibration.is_on:
            g_sets.Calibration.display_screens()