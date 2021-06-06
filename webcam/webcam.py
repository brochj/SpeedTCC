# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 23:25:46 2020

@author: broch
"""

import time
import uuid
import numpy as np
import cv2
import functions as t
import datetime
from image_processing import ImageProcessing
from tracking import Tracking
from sys import exit

# ########  CONSTANT VALUES ###################################################
# RESIZE_RATIO: From 1080p capture ->  720p=.6667 480p=.4445 360p=.33333 240p=.22222 144p=.13333
RESIZE_RATIO = 0.6667
if RESIZE_RATIO > 1 and RESIZE_RATIO < 0:
    exit("ERROR: RESIZE_RATIO must be 0 to 1 only")
CLOSE_VIDEO = 3000  # Closes the video when frame counter reaches the given value

SHOW_ROI = True
SHOW_TRACKING_AREA = True
SHOW_TRAIL = True
SHOW_CAR_RECTANGLE = True

SHOW_FRAME_COUNT = True

# ---- Tracking Values ----
# The maximum distance a blob centroid is allowed to move in order to
# consider it a match to a previous scene's blob.
BLOB_LOCKON_DIST_PX_MAX = 150  # default = 50 p/ ratio 0.35
BLOB_LOCKON_DIST_PX_MIN = 5  # default 5
MIN_AREA_FOR_DETEC = 20000  # Default 3000

# Tracking area limits
BOTTOM_LIMIT_TRACK = 430
UPPER_LIMIT_TRACK = 50

MIN_CENTRAL_POINTS = (
    5  # Minimum number of points needed to calculate speed | default 10
)
# The number of seconds a blob is allowed to sit around without having
# any new blobs matching it.
BLOB_TRACK_TIMEOUT = 0.5  # Default 0.7 or 0.1

# FIRST_PCT and SECND_PCT delimit the Region of Interest (ROI)
FIRST_PCT = 5
SECND_PCT = 20

# ---- Speed Values ----
CORRECTION_FACTOR = 1  # Default 2.10
# ####### END - CONSTANT VALUES ###############################################

# #### Variable Values #### DO NOT CHANGE
avg_speed = 0.0
calculated_fps = 0
avg_fps = 0
frameCounter = 0

object_area = []
process_times = []

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
FPS = 30
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # returns webcam's width
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # returns webcam's height

bgsMOG = cv2.createBackgroundSubtractorMOG2(
    history=10, varThreshold=50, detectShadows=0
)

# ##############  FUNCTIONS #####################################################


def r(numero):
    return int(numero * RESIZE_RATIO)


def calculate_speed(trails, fps, correction_factor):
    med_area_meter = 3.9  # Estimated value
    med_area_pixel = r(BOTTOM_LIMIT_TRACK - UPPER_LIMIT_TRACK)
    qntd_frames = MIN_CENTRAL_POINTS + 1  # len(trails)  # default 11
    dist_pixel = cv2.norm(trails[0], trails[MIN_CENTRAL_POINTS])
    dist_meter = dist_pixel * (med_area_meter / med_area_pixel)
    speed = (dist_meter * 3.6 * correction_factor) / (qntd_frames * (1 / fps))
    return round(speed, 1)


# ########## END  FUNCTIONS #####################################################
now = datetime.datetime.now()

KERNEL_ERODE = np.ones((r(5), r(5)), np.uint8)  # Default (r(12), r(12))
# Default (r(120), r(400))
KERNEL_DILATE = np.ones((r(120), r(1280)), np.uint8)

object_tracking = Tracking(
    RESIZE_RATIO, BLOB_LOCKON_DIST_PX_MAX, BLOB_LOCKON_DIST_PX_MIN
)

while True:
    ret, frame = t.get_frame(cap, RESIZE_RATIO)
    frame_time = time.time()

    start_frame_time = time.time()
    frame = cv2.flip(frame, 1)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    t.region_of_interest(frame_gray, RESIZE_RATIO, WIDTH,
                         HEIGHT, FIRST_PCT, SECND_PCT)

    hist = t.histogram_equalization(frame_gray)

    if SHOW_ROI:
        t.region_of_interest(frame, RESIZE_RATIO, FIRST_PCT, SECND_PCT)
    if SHOW_TRACKING_AREA:  # Draw the limits of Tracking Area
        cv2.line(
            frame, (0, r(UPPER_LIMIT_TRACK)), (WIDTH,
                                               r(UPPER_LIMIT_TRACK)), t.WHITE, 2
        )
        cv2.line(
            frame,
            (0, r(BOTTOM_LIMIT_TRACK)),
            (WIDTH, r(BOTTOM_LIMIT_TRACK)),
            t.WHITE,
            2,
        )
    if ret is True:

        lane1 = ImageProcessing(
            hist, RESIZE_RATIO, bgsMOG, KERNEL_ERODE, KERNEL_DILATE)

        drawing = t.convert_to_black_image(
            frame)  # create an empty black image
        convex_hull = cv2.drawContours(drawing, lane1.hull, 0, t.WHITE, -1, 8)

        for i in range(len(lane1.contours)):
            if cv2.contourArea(lane1.contours[i]) > r(MIN_AREA_FOR_DETEC):

                (x, y, w, h) = cv2.boundingRect(lane1.hull[i])
                center = (int(x + w / 2), int(y + h / 2))
                # convex_hull = cv2.rectangle(convex_hull, (x, y), (x + w, y + h), t.GREEN, 2) # printa na mask
                # Conditions to continue the tracking
                if w < r(340) and h < r(340):
                    continue
                if center[1] > r(BOTTOM_LIMIT_TRACK) or center[1] < r(
                    UPPER_LIMIT_TRACK
                ):
                    continue
                if SHOW_CAR_RECTANGLE:
                    if center[1] > r(UPPER_LIMIT_TRACK):
                        object_area.append(w * h)
                        cv2.rectangle(
                            frame, (x, y), (x + w, y + h), t.GREEN, 2)
                        cv2.rectangle(convex_hull, (x, y),
                                      (x + w, y + h), t.GREEN, 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), t.PINK, 2)
                # ################## START TRACKING #################################
                object_tracking.tracking(center, frame_time)

                try:
                    if len(object_tracking.closest_blob["trail"]) > MIN_CENTRAL_POINTS:
                        object_tracking.closest_blob["speed"].insert(
                            0,
                            calculate_speed(
                                object_tracking.closest_blob["trail"],
                                FPS,
                                CORRECTION_FACTOR,
                            ),
                        )
                        lane = 1
                        avg_speed = round(
                            np.mean(object_tracking.closest_blob["speed"]), 1
                        )
                except:
                    pass
                # ################# END TRACKING  ##############################
        object_tracking.remove_expired_track(
            BLOB_TRACK_TIMEOUT, "lane 1", frame_time)
        cv2.putText(
            frame,
            f"speed {avg_speed}",
            (r(10), r(470)),
            2,
            0.9,
            t.GREEN,
            thickness=1,
            lineType=2,
        )
        cv2.putText(
            frame,
            f"fps {avg_fps}",
            (r(300), r(470)),
            2,
            0.6,
            t.WHITE,
            thickness=1,
            lineType=2,
        )
        if not object_tracking.tracked_blobs:
            avg_speed = 0.0
        # ################ PRINT BLOBS ####################################
        for blob in object_tracking.tracked_blobs:
            if SHOW_TRAIL:
                t.print_trail(blob["trail"], frame)  # Draw the center points
        print(f"************** FIM DO FRAME {frameCounter} **************")

        # ########## Show the outputs  ########################################
        # cv2.imshow("1: frame_gray", frame_gray)
        # cv2.imshow("2: histogram_equalization", hist)
        cv2.imshow("3: foreground_mask", lane1.foreground_mask)
        cv2.imshow("4: eroded_mask", lane1.eroded_mask)
        cv2.imshow("5: dilated_mask", lane1.dilated_mask)
        # cv2.imshow("6: convex_hull", convex_hull)
        cv2.imshow("frame", frame)

        frameCounter += 1

        end_frame_time = time.time()
        calculated_fps = int(1 / (end_frame_time - start_frame_time))
        process_times.append(calculated_fps)
        avg_fps = int(np.mean(process_times[-24:]))

        if frameCounter == CLOSE_VIDEO:  # Closes the video in the specified frame
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press Q to close
            break
    else:  # exit from while: ret == False
        break
cap.release()
cv2.destroyAllWindows()
