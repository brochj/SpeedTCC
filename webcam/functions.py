# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:21:59 2020

@author: broch
"""
import numpy as np
import itertools as it
import cv2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)
CIAN = (255, 255, 0)
PINK = (255, 0, 255)
ORANGE = (0, 90, 255)


def get_frame(cap, RESIZE_RATIO):
    # Grabs a frame from the video capture and resizes it.
    ret, frame = cap.read()
    if ret:
        (h, w) = frame.shape[:2]
        frame = cv2.resize(
            frame,
            (int(w * RESIZE_RATIO), int(h * RESIZE_RATIO)),
            interpolation=cv2.INTER_CUBIC,
        )
    return ret, frame


def pairwise(iterable):
    r"s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = it.tee(iterable)
    next(b, None)
    return zip(a, b)


def region_of_interest(
    frame, resize_ratio, width=0, height=0, first_pct=15, secnd_pct=30
):
    def r(number):  # video scale adjust
        return int(number * resize_ratio)

    first_point = (round(first_pct, 0) / 100) * width
    secnd_point = (round(secnd_pct, 0) / 100) * width

    # left black bar
    pts1 = np.array(
        [
            [r(0), r(0)],
            [r(first_point), r(0)],
            [r(first_point), r(height)],
            [r(0), r(height)],
        ],
        np.int32,
    )
    cv2.fillPoly(frame, [pts1], BLACK)
    # right black bar
    pts3 = np.array(
        [
            [r(secnd_point), r(0)],
            [r(width), r(0)],
            [r(width), r(height)],
            [r(secnd_point), r(height)],
        ],
        np.int32,
    )
    cv2.fillPoly(frame, [pts3], BLACK)
    return frame


def histogram_equalization(frame_gray):
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    hist_equalization = clahe.apply(frame_gray)
    return hist_equalization


def convert_to_black_image(frame):
    return np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)


def print_trail(trail, frame):
    for (a, b) in pairwise(trail):
        cv2.line(frame, a, b, GREEN, 3)
        cv2.circle(frame, a, 5, RED, -1)


if __name__ == "__main__":
    print("Wrong file: functions.py executed")
