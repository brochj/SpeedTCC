# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 17:32:50 2020

@author: broch
"""
import cv2

import config
import colors
from functions import r


def car_rectangle(center, frame, frame_lane, x, y, w, h, left_padding=0):
    if config.SHOW_CAR_RECTANGLE:
        if center[1] > r(config.UPPER_LIMIT_TRACK):
            cv2.rectangle(frame_lane, (x, y), (x + w, y + h), colors.GREEN, 2)
            cv2.rectangle(frame, (x + r(left_padding), y),
                          (x + w + r(left_padding), y + h), colors.GREEN, 2)
        else:
            cv2.rectangle(frame_lane, (x, y), (x + w, y + h), colors.PINK, 2)
            cv2.rectangle(frame, (x + r(left_padding), y),
                          (x + w + r(left_padding), y + h), colors.PINK, 2)
