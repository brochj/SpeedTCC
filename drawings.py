# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 17:32:50 2020

@author: broch
"""
import cv2
import itertools as it

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


def blobs(frame, tracked_blobs):
    if config.SHOW_TRAIL:

        def pairwise(iterable):
            r"s -> (s0, s1), (s1, s2), (s2, s3), ..."
            a, b = it.tee(iterable)
            next(b, None)
            return zip(a, b)

        for blob in tracked_blobs:  # Desenha os pontos centrais
            for (a, b) in pairwise(blob['trail']):
                cv2.line(frame, a, b, colors.GREEN, 3)
                cv2.circle(frame, a, 5, colors.RED, -1)
