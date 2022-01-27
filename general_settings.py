import cv2
import numpy
import math
from enum import Enum, auto
 



class Team(Enum):
    RED = auto()
    BLUE = auto()



## CHANGE THIS VALUE FOR CHOOSING TEAM ##
team = Team.BLUE

frame_size_width = 240 #px
frame_size_height = 135 #px



class BlueTeamBall:

    def __init__(self):
        self.threshold_hue = [92, 119]
        self.threshold_saturation = [124, 255]
        self.threshold_value = [37, 255]


class RedTeamBall:

    def __init__(self):
        self.threshold_hue = [162, 180]
        self.threshold_saturation = [83, 255]
        self.threshold_value = [112, 255]


class Tape:
    def __init__(self):
        self.threshold_hue = [58.273381294964025, 111.23938879456708]
        self.threshold_saturation = [206.38489208633095, 255.0]
        self.threshold_value = [52.74280575539568, 255.0]
