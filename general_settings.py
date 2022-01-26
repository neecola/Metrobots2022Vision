import cv2
import numpy
import math
from enum import Enum, auto
 



class Team(Enum):
    RED = auto()
    BLUE = auto()



## CHANGE THIS VALUE FOR CHOOSING TEAM ##
team = Team.RED


class BlueTeamBall:

    def __init__(self):
        self.threshold_hue = [69.60431654676259, 111.85828925993331]
        self.threshold_saturation = [87.14028776978417, 222.52971137521223]
        self.threshold_value = [89.43345323741006, 255.0]


class RedTeamBall:

    def __init__(self):
        self.threshold_hue = [69.60431654676259, 111.85828925993331]
        self.threshold_saturation = [87.14028776978417, 222.52971137521223]
        self.threshold_value = [89.43345323741006, 255.0]