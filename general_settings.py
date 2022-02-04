import cv2
import numpy as np
import math
from enum import Enum, auto


class Team(Enum):
    RED = auto()
    BLUE = auto()


## CHANGE THIS VALUE FOR CHOOSING TEAM ##
TEAM = Team.BLUE

FRAME_SIZE_WIDTH = 240  # px
FRAME_SIZE_HEIGHT = 135  # px

ROBO_RIO_ADDRESS = ''




class BlueTeamBall:
    threshold_hue = [92, 119]
    threshold_saturation = [124, 255]
    threshold_value = [37, 255]


class RedTeamBall:
    threshold_hue = [162, 180]
    threshold_saturation = [83, 255]
    threshold_value = [112, 255]


class Tape:
    threshold_hue = [58.273381294964025, 111.23938879456708]
    threshold_saturation = [206.38489208633095, 255.0]
    threshold_value = [52.74280575539568, 255.0]


# CALIBRATION THINGS #
class Calibration:
    is_on = True
    ball_screens = list()
    tape_screens = list()


    @staticmethod
    def display_screens():
        
        for i in range(len(Calibration.ball_screens)):
            try:
                Calibration.ball_screens[i] = cv2.cvtColor(Calibration.ball_screens[i], cv2.COLOR_GRAY2BGR)
            except:
                continue
        
        ball_line = np.hstack(tuple(screen for screen in Calibration.ball_screens))

        for i in range(len(Calibration.tape_screens)):
            try:
                Calibration.tape_screens[i] = cv2.cvtColor(Calibration.tape_screens[i], cv2.COLOR_GRAY2BGR)
            except:
                continue
        tape_line = np.hstack(tuple(screen for screen in Calibration.tape_screens))

        cv2.imshow('Ball processing screens', ball_line)
        cv2.imshow('Tape processing screens', tape_line)
        
        cv2.waitKey(5)
        Calibration.ball_screens.clear()
        Calibration.tape_screens.clear()
