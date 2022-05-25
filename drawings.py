# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 17:32:50 2020

@author: broch
"""
import cv2
import itertools as it

import configs.config as config
import colors
from lib.functions import r


def xml_speed_values(frame, speed, position):
    # Mostra no video os valores das velocidades do arquivo xml
    text_pos = (r(position[0]), r(position[1]))
    if config.SHOW_REAL_SPEEDS:
        cv2.rectangle(
            frame,
            (text_pos[0] - 10, text_pos[1] - 20),
            (text_pos[0] + 135, text_pos[1] + 10),
            (0, 0, 0),
            -1,
        )
        cv2.putText(frame, "speed: {}".format(speed), text_pos, 2, 0.6, colors.CIAN, 1)


def frame_count(frame, frame_count, total_frames=None):
    if config.SHOW_FRAME_COUNT:
        if total_frames:
            pct = str(int((100 * frame_count) / total_frames)) + "%"
        else:
            pct = ""
        cv2.putText(
            frame,
            f"frame: {frame_count} {pct}",
            (r(14), r(1071)),
            0,
            0.65,
            colors.WHITE,
            2,
        )


def avg_fps(frame, avg_fps):
    cv2.putText(frame, f"FPS {avg_fps}", (r(1600), r(1061)), 0, 0.6, colors.WHITE, 2)


def tracking_area(frame):
    if config.SHOW_TRACKING_AREA:  # Desenha os Limites da Área de Tracking
        cv2.line(
            frame,
            (0, r(config.UPPER_LIMIT_TRACK)),
            (r(1920), r(config.UPPER_LIMIT_TRACK)),
            colors.WHITE,
            2,
        )
        cv2.line(
            frame,
            (0, r(config.BOTTOM_LIMIT_TRACK)),
            (r(1920), r(config.BOTTOM_LIMIT_TRACK)),
            colors.WHITE,
            2,
        )


def car_rectangle(frame, frame_lane, lane_detection, left_padding=0):
    center = lane_detection.center
    x = lane_detection.x
    y = lane_detection.y
    w = lane_detection.w
    h = lane_detection.h

    if config.SHOW_CAR_RECTANGLE:
        if center[1] > r(config.UPPER_LIMIT_TRACK):
            cv2.rectangle(frame_lane, (x, y), (x + w, y + h), colors.GREEN, 2)
            cv2.rectangle(
                frame,
                (x + r(left_padding), y),
                (x + w + r(left_padding), y + h),
                colors.GREEN,
                2,
            )
        else:
            cv2.rectangle(frame_lane, (x, y), (x + w, y + h), colors.PINK, 2)
            cv2.rectangle(
                frame,
                (x + r(left_padding), y),
                (x + w + r(left_padding), y + h),
                colors.PINK,
                2,
            )


def blobs(frame, tracked_blobs):
    if config.SHOW_TRAIL:

        def pairwise(iterable):
            r"s -> (s0, s1), (s1, s2), (s2, s3), ..."
            a, b = it.tee(iterable)
            next(b, None)
            return zip(a, b)

        # for blob in tracked_blobs:  # Desenha os pontos centrais
        try:
            for (a, b) in pairwise(tracked_blobs["trail"]):
                cv2.line(frame, a, b, colors.GREEN, 3)
                cv2.circle(frame, a, 5, colors.RED, -1)
        except KeyError:
            # tracked_blobs is an empty dict -> tracked_blobs = {}
            pass


def result(frame, vehicle_speed, id_car, position):
    if not vehicle_speed.avg_speed:
        return
    avg_speed = vehicle_speed.avg_speed
    abs_error = vehicle_speed.abs_error
    pct_error = vehicle_speed.pct_error

    if abs(abs_error) <= 3:
        color = colors.GREEN
    elif abs(abs_error) > 3 and abs(abs_error) <= 5:
        color = colors.YELLOW
    elif abs(abs_error) > 5 and abs(abs_error) <= 10:
        color = colors.ORANGE
    elif abs(abs_error) > 10:
        color = colors.RED

    x, y = position
    positions = [
        (r(x), r(y)),
        (r(x + 200), r(y)),
        (r(x + 200), r(y + 60)),
        (r(x + 200), r(y + 110)),
    ]

    cv2.putText(
        frame,
        str(float("{0:.2f}".format(avg_speed))),
        positions[0],
        2,
        0.6,
        color,
        thickness=1,
        lineType=2,
    )  # Velocidade Medida
    cv2.putText(
        frame,
        str(float("{0:.2f} ".format(abs_error))),
        positions[1],
        2,
        0.6,
        color,
        thickness=1,
        lineType=2,
    )  # erro absoluto
    cv2.putText(
        frame,
        str(float("{0:.2f}".format(pct_error))) + "%",
        positions[2],
        2,
        0.6,
        color,
        thickness=1,
        lineType=2,
    )  # erro percentual
    cv2.putText(
        frame, f"id: {id_car}", positions[3], 2, 0.6, color, thickness=1, lineType=2
    )


if __name__ == "__main__":
    raise Exception("Wrong File")
