
import cv2

from functions import r
import config


class VehicleDetection:

    def __init__(self):
        self.lane = None
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.center = 0
        self.detected = False

    def reset_data(self):
        # TODO nao to usando
        self.lane = None
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.center = 0
        self.detected = False

    def __update_rectangle_points(self, hull):
        (self.x, self.y, self.w, self.h) = cv2.boundingRect(hull)

    def __create_center_point(self):
        self.center = (int(self.x + self.w/2), int(self.y + self.h/2))

    def __is_outside_of_tracking_area(self):
        below_tracking_area = self.center[1] > r(config.BOTTOM_LIMIT_TRACK_L2)
        above_tracking_area = self.center[1] < r(config.UPPER_LIMIT_TRACK_L2)
        return below_tracking_area or above_tracking_area

    def __is_large_enough(self):
        return self.w < r(340) and self.h < r(340)

    def __is_area_large_enough(self, contour):
        return cv2.contourArea(contour) > r(config.MIN_AREA_FOR_DETEC)

    def detection(self, processed_image):
        self.lane = processed_image
        for i, contour in enumerate(self.lane.contours):
            if self.__is_area_large_enough(contour):

                self.__update_rectangle_points(self.lane.hull[i])
                self.__create_center_point()

                if self.__is_large_enough():
                    continue

                if self.__is_outside_of_tracking_area():
                    continue

                self.detected = True
