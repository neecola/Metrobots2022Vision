from turtle import goto
import cv2
import numpy as np
import math
from enum import Enum, auto


class Team(Enum):
    RED = auto()
    BLUE = auto()


## CHANGE THIS VALUE FOR CHOOSING TEAM ##
team = Team.BLUE

frame_size_width = 240  # px
frame_size_height = 135  # px


class BlueTeamBall:
    threshold_hue = [92, 119]
    threshold_saturation = [124, 255]
    threshold_value = [37, 255]


class RedTeamBall:
    threshold_hue = [162, 180]
    threshold_saturation = [83, 255]
    threshold_value = [112, 255]


class Tape:
    selfthreshold_hue = [58.273381294964025, 111.23938879456708]
    threshold_saturation = [206.38489208633095, 255.0]
    threshold_value = [52.74280575539568, 255.0]


# CALIBRATION THINGS #
class Calibration:
    is_on = True
    screens = list()

    @staticmethod
    def display_screens():
        
        for i in range(len(Calibration.screens)):
            try:
                Calibration.screens[i] = cv2.cvtColor(Calibration.screens[i], cv2.COLOR_GRAY2BGR)
            except:
                continue

        final_image = np.hstack(tuple(screen for screen in Calibration.screens))
        
        cv2.imshow('Ball processing screens', final_image)
        
        
        cv2.waitKey(5)
        Calibration.screens.clear()
