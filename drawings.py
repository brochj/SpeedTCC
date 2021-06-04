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


def result(frame, avg_speed, abs_error, pct_error, id_car, position):
    if abs(abs_error) <= 3:
        color = colors.GREEN
    elif abs(abs_error) > 3 and abs(abs_error) <= 5:
        color = colors.YELLOW
    elif abs(abs_error) > 5 and abs(abs_error) <= 10:
        color = colors.ORANGE
    elif abs(abs_error) > 10:
        color = colors.RED

    x, y = position
    positions = [(r(x), r(y)), (r(x + 200), r(y)),
                 (r(x + 200), r(y + 60)), (r(x + 200), r(y + 110))]

    cv2.putText(frame, str(float("{0:.2f}".format(avg_speed))), positions[0],
                2, .6, color, thickness=1, lineType=2)  # Velocidade Medida
    cv2.putText(frame, str(float("{0:.2f} ".format(abs_error))), positions[1],
                2, .6, color, thickness=1, lineType=2)  # erro absoluto
    cv2.putText(frame, str(float("{0:.2f}".format(pct_error)))+'%', positions[2],
                2, .6, color, thickness=1, lineType=2)  # erro percentual
    cv2.putText(frame, f'id: {id_car}', positions[3],
                2, .6, color, thickness=1, lineType=2)
