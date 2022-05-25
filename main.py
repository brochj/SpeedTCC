# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:02:46 2020

@author: broch
"""

from sys import exit
import cv2
import datetime
import numpy as np
import os
import time
import uuid

# Created modules
from functions import r
from pre_processing import PreProcessing
from image_processing import ImageProcessing
from tracking import Tracking
from vehicle_detection import VehicleDetection
from vehicle_speed import VehicleSpeed
from perspective import Perspective
import colors
import config
import drawings as draw
import functions as t
import xml_processing


from models.lane_info import Lane

import configs.lane1 as lane1_config
import configs.lane2 as lane2_config
import configs.lane3 as lane3_config

cap = cv2.VideoCapture(config.VIDEO_FILE)

bgsMOG = cv2.createBackgroundSubtractorMOG2(
    history=10, varThreshold=50, detectShadows=0
)

# Variant Values
dict_lane1 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 2
dict_lane2 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 2
dict_lane3 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 3

frame_count = 0
process_times = []
avg_fps = 0

# Dicionário que armazena todas as informações do xml
vehicle = xml_processing.read_xml(config.XML_FILE, config.VIDEO)


lane1_objects = {
    "perspective": Perspective(lane1_config.PERSPECTIVE_POINTS),
    "image_processing": ImageProcessing(
        bgsMOG, lane1_config.KERNEL_ERODE, lane1_config.KERNEL_DILATE_L1
    ),
    "tracking": Tracking(name="lane 1"),
    "vehicle_speed": VehicleSpeed(lane1_config.CF_LANE1),
    "detection": VehicleDetection(),
}

lane2_objects = {
    "perspective": Perspective(lane2_config.PERSPECTIVE_POINTS),
    "image_processing": ImageProcessing(
        bgsMOG, lane2_config.KERNEL_ERODE, lane2_config.KERNEL_DILATE_L2
    ),
    "tracking": Tracking(name="lane 2"),
    "vehicle_speed": VehicleSpeed(lane2_config.CF_LANE2),
    "detection": VehicleDetection(),
}

lane3_objects = {
    "perspective": Perspective(lane3_config.PERSPECTIVE_POINTS),
    "image_processing": ImageProcessing(
        bgsMOG, lane3_config.KERNEL_ERODE, lane3_config.KERNEL_DILATE_L3
    ),
    "tracking": Tracking(name="lane 3"),
    "vehicle_speed": VehicleSpeed(lane3_config.CF_LANE3),
    "detection": VehicleDetection(),
}


lane1 = Lane(lane1_objects)
lane2 = Lane(lane2_objects)
lane3 = Lane(lane3_objects)

while True:
    ret, frame = t.get_frame(cap)
    frame_time = time.time()

    if t.should_skip_this(frame_count):
        frame_count += 1
        continue

    start_frame_time = time.time()
    if ret is True:
        xml_processing.update_info_xml(
            frame_count, vehicle, dict_lane1, dict_lane2, dict_lane3
        )

        frame_gray = PreProcessing.frame_to_grayscale(frame)
        frame_roi = PreProcessing.apply_region_of_interest(frame_gray)
        frame_hist = PreProcessing.apply_histogram_equalization(frame_roi)

        draw.tracking_area(frame)
        draw.avg_fps(frame, avg_fps)
        draw.frame_count(frame, frame_count, vehicle["videoframes"])

        draw.xml_speed_values(frame, dict_lane1.get("speed"), (143, 43))
        draw.xml_speed_values(frame, dict_lane2.get("speed"), (628, 43))
        draw.xml_speed_values(frame, dict_lane3.get("speed"), (1143, 43))

        lane1.start_monitoring(frame, frame_hist, frame_time, dict_lane1, (350, 120))
        lane2.start_monitoring(frame, frame_hist, frame_time, dict_lane2, (830, 120))
        lane3.start_monitoring(frame, frame_hist, frame_time, dict_lane3, (1350, 120))

        print(f"************** END OF FRAME {frame_count} **************")

        # ########## MOSTRA OS VIDEOS  ########################################

        # cv2.imshow("lane1.fgmask", lane1.image_processing.foreground_mask)
        # cv2.imshow("lane1.erodedmask", lane1.image_processing.eroded_mask)
        # cv2.imshow("lane1.dilatedmask", lane1.image_processing.dilated_mask)

        # cv2.imshow("lane2.fgmask", lane2.image_processing.foreground_mask)
        # cv2.imshow("lane2.erodedmask", lane2.image_processing.eroded_mask)
        # cv2.imshow("lane2.dilatedmask", lane2.image_processing.dilated_mask)

        # cv2.imshow("lane3.fgmask", lane3.image_processing.foreground_mask)
        # cv2.imshow("lane3.erodedmask", lane3.image_processing.eroded_mask)
        # cv2.imshow("lane3.dilatedmask", lane3.image_processing.dilated_mask)

        # cv2.imshow("lane1.draw_contours", lane1.draw_contours())
        # cv2.imshow("lane2.draw_contours", lane2.draw_contours())
        # cv2.imshow("lane3.draw_contours", lane3.draw_contours())

        # cv2.imshow("lane1.frame", lane1.frame)
        cv2.imshow("lane2.frame", lane2.frame)
        cv2.imshow("lane3.frame", lane3.frame)
        cv2.imshow("frame", frame)

        frame_count += 1

        end_frame_time = time.time()
        process_times.append(end_frame_time - start_frame_time)
        calculated_fps = int(1 / (end_frame_time - start_frame_time))
        process_times.append(calculated_fps)
        avg_fps = int(np.mean(process_times[-24:]))

        if frame_count == config.CLOSE_VIDEO:  # fecha o video
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Tecla Q para fechar
            break

    else:  # exit from while: ret == False
        break


cap.release()
cv2.destroyAllWindows()
