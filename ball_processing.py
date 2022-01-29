import cv2
import numpy
import math
from enum import Enum, auto
import general_settings as g_sets
from general_settings import Team, Calibration

#created to fix the absence of this kind of enum used in the auto generated GRIP code
class BlurType(Enum):
    Box_Blur = auto()
    Gaussian_Blur = auto()
    Median_Filter = auto()



class BallProcessing:

    # asks for team in the main so that it can recognize either blue or red balls
    def __init__(self, team: Team):

        # imports the threshold values from ball_team_settings.py module
        # (needed for indentifying either blue or red balls)
        if team == Team.RED:
            self.__hsv_threshold_hue = g_sets.RedTeamBall.threshold_hue
            self.__hsv_threshold_saturation = g_sets.RedTeamBall.threshold_saturation
            self.__hsv_threshold_value = g_sets.RedTeamBall.threshold_value

        elif team == Team.BLUE:
            self.__hsv_threshold_hue = g_sets.BlueTeamBall.threshold_hue
            self.__hsv_threshold_saturation = g_sets.BlueTeamBall.threshold_saturation
            self.__hsv_threshold_value = g_sets.BlueTeamBall.threshold_value

        # initialization of values for the image processing
        # (it shouldn't be necessary to modify these for tuning the camera)
        self.__blur_type = BlurType.Box_Blur
        self.__blur_radius = 10

        self.blur_output = None

        self.__hsv_threshold_input = self.blur_output
        self.hsv_threshold_output = None

        self.__cv_dilate_src = self.hsv_threshold_output
        self.__cv_dilate_kernel = None
        self.__cv_dilate_anchor = (-1, -1)
        self.__cv_dilate_iterations = 2.0
        self.__cv_dilate_bordertype = cv2.BORDER_CONSTANT
        self.__cv_dilate_bordervalue = (-1)

        self.cv_dilate_output = None

        self.__cv_erode_src = self.cv_dilate_output
        self.__cv_erode_kernel = None
        self.__cv_erode_anchor = (-1, -1)
        self.__cv_erode_iterations = 3.0
        self.__cv_erode_bordertype = cv2.BORDER_CONSTANT
        self.__cv_erode_bordervalue = (-1)

        self.cv_erode_output = None

        self.__find_contours_input = self.cv_erode_output
        self.__find_contours_external_only = False

        self.find_contours_output = None

    # operates the ball processing and returns the final result
    # without modifying the argument
    def process(self, source0):
        
        #ignore if statements in this function, they are for
        #displaying the phases of the processing during calibration
        if g_sets.Calibration.is_on: 
            Calibration.ball_screens.append(source0)
        
        # Step Blur0:
        self.__blur_input = source0
        (self.blur_output) = self.__blur(
            self.__blur_input, self.__blur_type, self.__blur_radius)
        
        #for calibration
        if g_sets.Calibration.is_on: 
            Calibration.ball_screens.append(self.blur_output)


        # Step HSV_Threshold0:
        self.__hsv_threshold_input = self.blur_output
        (self.hsv_threshold_output) = self.__hsv_threshold(self.__hsv_threshold_input,
                                                           self.__hsv_threshold_hue, self.__hsv_threshold_saturation, self.__hsv_threshold_value)
        if g_sets.Calibration.is_on:
            Calibration.ball_screens.append(self.hsv_threshold_output)

        # Step CV_dilate0:
        self.__cv_dilate_src = self.hsv_threshold_output
        (self.cv_dilate_output) = self.__cv_dilate(self.__cv_dilate_src, self.__cv_dilate_kernel,
                                                   self.__cv_dilate_anchor, self.__cv_dilate_iterations, self.__cv_dilate_bordertype, self.__cv_dilate_bordervalue)

        if g_sets.Calibration.is_on:
            Calibration.ball_screens.append(self.cv_dilate_output)        
        
        
        # Step CV_erode0:
        self.__cv_erode_src = self.cv_dilate_output
        (self.cv_erode_output) = self.__cv_erode(self.__cv_erode_src, self.__cv_erode_kernel,
                                                 self.__cv_erode_anchor, self.__cv_erode_iterations, self.__cv_erode_bordertype, self.__cv_erode_bordervalue)
        
        if g_sets.Calibration.is_on:
            Calibration.ball_screens.append(self.cv_erode_output)
        
        return self.cv_erode_output

        # Step Find_Contours0: (not used)
        #self.__find_contours_input = self.cv_erode_output
        #(self.find_contours_output) = self.__find_contours(self.__find_contours_input, self.__find_contours_external_only)

    @staticmethod
    def __blur(src, type, radius):
        """Softens an image using one of several filters.
        Args:
            src: The source mat (numpy.ndarray).
            type: The blurType to perform represented as an int.
            radius: The radius for the blur as a float.
        Returns:
            A numpy.ndarray that has been blurred.
        """
        if(type is BlurType.Box_Blur):
            ksize = int(2 * round(radius) + 1)
            return cv2.blur(src, (ksize, ksize))
        elif(type is BlurType.Gaussian_Blur):
            ksize = int(6 * round(radius) + 1)
            return cv2.GaussianBlur(src, (ksize, ksize), round(radius))
        elif(type is BlurType.Median_Filter):
            ksize = int(2 * round(radius) + 1)
            return cv2.medianBlur(src, ksize)
        else:
            return cv2.bilateralFilter(src, -1, round(radius), round(radius))

    @staticmethod
    def __hsv_threshold(input, hue, sat, val):
        """Segment an image based on hue, saturation, and value ranges.
        Args:
            input: A BGR numpy.ndarray.
            hue: A list of two numbers the are the min and max hue.
            sat: A list of two numbers the are the min and max saturation.
            lum: A list of two numbers the are the min and max value.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
        return cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))

    @staticmethod
    def __cv_dilate(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of higher value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for dilation. A numpy.ndarray.
           iterations: the number of times to dilate.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after dilation.
        """
        return cv2.dilate(src, kernel, anchor, iterations=(int)(iterations + 0.5),
                          borderType=border_type, borderValue=border_value)

    @staticmethod
    def __cv_erode(src, kernel, anchor, iterations, border_type, border_value):
        """Expands area of lower value in an image.
        Args:
           src: A numpy.ndarray.
           kernel: The kernel for erosion. A numpy.ndarray.
           iterations: the number of times to erode.
           border_type: Opencv enum that represents a border type.
           border_value: value to be used for a constant border.
        Returns:
            A numpy.ndarray after erosion.
        """
        return cv2.erode(src, kernel, anchor, iterations=(int)(iterations + 0.5),
                         borderType=border_type, borderValue=border_value)

    @staticmethod
    def __find_contours(input, external_only):
        """Sets the values of pixels in a binary image to their distance to the nearest black pixel.
        Args:
            input: A numpy.ndarray.
            external_only: A boolean. If true only external contours are found.
        Return:
            A list of numpy.ndarray where each one represents a contour.
        """
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_LIST
        method = cv2.CHAIN_APPROX_SIMPLE
        contours, hierarchy = cv2.findContours(
            input, mode=mode, method=method)
        return contours
