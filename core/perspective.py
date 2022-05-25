import cv2
import numpy as np
from lib.functions import r


class Perspective:
    def __init__(self, points: dict, output_dimensions=(640, 1080)):

        self.origin = None
        self.target = None
        self.output_dimensions = output_dimensions

        self.__resize_output_dimensions(self.output_dimensions)
        self.origin = points["origin"]
        self.target = points["target"]
        self.__resize_points(self.origin)
        self.__resize_points(self.target)
        self.origin = self.__create_points(self.origin)
        self.target = self.__create_points(self.target)

        self.homography_matrix = self.__find_homography_matrix(self.origin, self.target)

    def __resize_output_dimensions(self, size):
        self.output_dimensions = (r(size[0]), r(size[1]))

    def __resize_points(self, points):
        points["bottom_left"] = (
            r(points["bottom_left"][0]),
            r(points["bottom_left"][1]),
        )
        points["bottom_right"] = (
            r(points["bottom_right"][0]),
            r(points["bottom_right"][1]),
        )
        points["top_right"] = (r(points["top_right"][0]), r(points["top_right"][1]))
        points["top_left"] = (r(points["top_left"][0]), r(points["top_left"][1]))

    def __create_points(self, points: dict):
        return np.array(
            [
                points["bottom_left"],
                points["bottom_right"],
                points["top_right"],
                points["top_left"],
            ],
            np.int32,
        )

    def __find_homography_matrix(self, origin, target):
        homography_matrix, _ = cv2.findHomography(origin, target, cv2.RANSAC)
        return homography_matrix

    def apply_perspective(self, frame):
        return cv2.warpPerspective(
            frame, self.homography_matrix, self.output_dimensions
        )


if __name__ == "__main__":
    raise Exception("Wrong File")
