
import cv2
import numpy as np
from functions import r


class Perspective:
    lane1 = {
        "origin": {
            'bottom_left': (-150, 1080),
            'bottom_right': (480, 1080),
            'top_right': (560, 0),
            'top_left': (270, 0),
        },
        "target": {
            'bottom_left': (0, 1080),
            'bottom_right': (640, 1080),
            'top_right': (610, 0),
            'top_left': (35, 0),
        }
    }
    lane2 = {
        "origin": {
            'bottom_left': (570, 1080),
            'bottom_right': (1310, 1080),
            'top_right': (900, 0),
            'top_left': (640, 0),
        },
        "target": {
            'bottom_left': (0, 1080),
            'bottom_right': (640, 1080),
            'top_right': (570, 0),
            'top_left': (50, 0),
        }
    }
    lane3 = {
        "origin": {
            'bottom_left': (1410, 1080),
            'bottom_right': (2170, 1080),
            'top_right': (1320, 0),
            'top_left': (990, 0),
        },
        "target": {
            'bottom_left': (0, 1080),
            'bottom_right': (640, 1080),
            'top_right': (670, 0),
            'top_left': (15, 0),
        }
    }

    def __init__(self, lane):
        self.origin = None
        self.target = None
        self.output_dimensions = (640, 1080)

        self.__resize_output_dimensions(self.output_dimensions)
        self.__select_points(lane)
        self.__resize_points(self.origin)
        self.__resize_points(self.target)
        self.origin = self.__create_points(self.origin)
        self.target = self.__create_points(self.target)

        self.homography_matrix = self.__find_homography_matrix(
            self.origin, self.target)

    def __resize_output_dimensions(self, size):
        self.output_dimensions = (r(size[0]), r(size[1]))

    def __select_points(self, lane):
        if lane == 1:
            self.origin = self.lane1["origin"]
            self.target = self.lane1["target"]
        if lane == 2:
            self.origin = self.lane2["origin"]
            self.target = self.lane2["target"]
        if lane == 3:
            self.origin = self.lane3["origin"]
            self.target = self.lane3["target"]

    def __resize_points(self, points):
        points["bottom_left"] = (
            r(points["bottom_left"][0]),
            r(points["bottom_left"][1]))
        points["bottom_right"] = (
            r(points["bottom_right"][0]),
            r(points["bottom_right"][1]))
        points["top_right"] = (
            r(points["top_right"][0]),
            r(points["top_right"][1]))
        points["top_left"] = (
            r(points["top_left"][0]),
            r(points["top_left"][1]))

    def __create_points(self, points: dict):
        return np.array([
            points["bottom_left"],
            points["bottom_right"],
            points["top_right"],
            points["top_left"]], np.int32)

    def __find_homography_matrix(self, origin, target):
        homography_matrix, _ = cv2.findHomography(origin, target, cv2.RANSAC)
        return homography_matrix

    def apply_perspective(self, frame):
        return cv2.warpPerspective(frame, self.homography_matrix, self.output_dimensions)


if __name__ == '__main__':
    raise Exception('Wrong File')
