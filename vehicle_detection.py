import cv2
from functions import r
import config


class VehicleDetection:
    def __init__(self, bottom_limit=None, upper_limit=None):
        self.bottom_limit = bottom_limit or config.BOTTOM_LIMIT_TRACK
        self.upper_limit = upper_limit or config.UPPER_LIMIT_TRACK
        self.lane = None
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.center = 0
        self.detected = False

    def reset(self, bottom_limit=None, upper_limit=None):
        self.bottom_limit = bottom_limit or config.BOTTOM_LIMIT_TRACK
        self.upper_limit = upper_limit or config.UPPER_LIMIT_TRACK
        self.lane = None
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.center = 0
        self.detected = False

    def detection(self, processed_image):
        self.lane = processed_image
        for i, contour in enumerate(self.lane.contours):
            if self.__is_usable_contour(i, contour):
                self.detected = True

    def __is_usable_contour(self, index, contour):
        if self.__is_area_large_enough(contour):
            self.__update_rectangle_points(self.lane.hull[index])
            self.__create_center_point()

            if self.__is_not_large_enough():
                return False

            if self.__is_outside_of_tracking_area():
                return False

            return True

    def __is_area_large_enough(self, contour):
        return cv2.contourArea(contour) > r(config.MIN_AREA_FOR_DETEC)

    def __update_rectangle_points(self, hull):
        (self.x, self.y, self.w, self.h) = cv2.boundingRect(hull)

    def __create_center_point(self):
        self.center = (int(self.x + self.w / 2), int(self.y + self.h / 2))

    def __is_not_large_enough(self):
        return self.w < r(340) and self.h < r(340)

    def __is_outside_of_tracking_area(self):
        is_below_tracking_area = self.center[1] > r(self.bottom_limit)
        is_above_tracking_area = self.center[1] < r(self.upper_limit)
        return is_below_tracking_area or is_above_tracking_area


if __name__ == "__main__":
    raise Exception("Wrong File")
