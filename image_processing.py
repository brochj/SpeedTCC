# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 14:50:08 2020

@author: broch
"""
import cv2
import numpy as np

import colors
import configs.config as config
from lib.functions import r


class ImageProcessing:
    def __init__(self, background_subtractor, kernel_erode, kernel_dilate):
        self.frame = None
        self.foreground_mask = None
        self.eroded_mask = None
        self.dilated_mask = None
        self.contours = None
        self.hull = None
        self.bg_subtractor = background_subtractor
        self.kernel_erode = self.__create_kernel(kernel_erode)
        self.kernel_dilate = self.__create_kernel(kernel_dilate)

    def __create_kernel(self, size):
        height = r(size[0])
        width = r(size[1])
        return np.ones((height, width), np.uint8)

    def apply_morphological_operations(self, frame):
        self.frame = frame
        self.apply_bg_subtractor()
        self.apply_erode()
        self.apply_dilate()
        self.apply_contourns()
        self.apply_convex_hull()

    def apply_bg_subtractor(self):
        self.foreground_mask = self.bg_subtractor.apply(self.frame, None, 0.01)
        return self.foreground_mask

    def apply_erode(self):
        self.eroded_mask = cv2.erode(
            self.foreground_mask, self.kernel_erode, iterations=1
        )
        return self.eroded_mask

    def apply_dilate(self):
        self.dilated_mask = cv2.dilate(
            self.eroded_mask, self.kernel_dilate, iterations=1
        )
        return self.dilated_mask

    def apply_contourns(self):
        self.contours, _ = cv2.findContours(
            self.dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        return self.contours

    def apply_convex_hull(self):
        self.hull = []
        for i in range(len(self.contours)):  # calculate points for each contour
            # creating convex hull object for each contour
            self.hull.append(cv2.convexHull(self.contours[i], False))

    def draw_contours(self):
        black_image = self.__convert_to_black_image(self.frame)
        return cv2.drawContours(black_image, self.hull, 0, colors.WHITE, -1, 8)

    def __convert_to_black_image(self, frame):
        return np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)


if __name__ == "__main__":
    raise Exception("Wrong File")
