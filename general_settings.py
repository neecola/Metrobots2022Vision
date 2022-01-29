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
    screens = dict()

    @staticmethod
    def display_screens(self):
        final_image = list()
        for screen in self.screens:
            final_image = np.concatenate((final_image, screen), axis=1)

        cv2.imshow('All screens', final_image)
        cv2.waitKey(5)
