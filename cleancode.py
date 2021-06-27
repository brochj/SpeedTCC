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
import colors
import config
import drawings as draw
import functions as t
import xml_processing

cap = cv2.VideoCapture(config.VIDEO_FILE)

bgsMOG = cv2.createBackgroundSubtractorMOG2(
    history=10, varThreshold=50, detectShadows=0)

# Variant Values
dict_lane1 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 1
dict_lane2 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 2
dict_lane3 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 3

frame_count = 0  # Armazena a contagem de frames processados do video
process_times = []
avg_fps = 0

now = datetime.datetime.now()

# Dicionário que armazena todas as informações do xml
vehicle = xml_processing.read_xml(config.XML_FILE, config.VIDEO)

KERNEL_ERODE = np.ones((r(12), r(12)), np.uint8)
KERNEL_DILATE = np.ones((r(120), r(400)), np.uint8)

KERNEL_ERODE_L2 = np.ones((r(12), r(12)), np.uint8)
KERNEL_DILATE_L2 = np.ones((r(100), r(400)), np.uint8)

KERNEL_ERODE_L3 = np.ones((r(12), r(12)), np.uint8)
KERNEL_DILATE_L3 = np.ones((r(100), r(320)), np.uint8)


def create_kernel(height, width):
    return np.ones((height, width), np.uint8)


lane1_tracking = Tracking('lane 1')
lane2_tracking = Tracking('lane 2')
lane3_tracking = Tracking('lane 3')


while True:
    ret, frame = t.get_frame(cap)
    frame_time = time.time()

    if t.should_skip_this(frame_count):
        frame_count += 1
        continue

    start_frame_time = time.time()
    frame_gray = PreProcessing.frame_to_grayscale(frame)
    frame_roi = PreProcessing.apply_region_of_interest(frame_gray)
    frame_hist = PreProcessing.apply_histogram_equalization(frame_roi)

    frame_lane1 = t.perspective(frame_hist, 1)
    frame_lane2 = t.perspective(frame_hist, 2)
    frame_lane3 = t.perspective(frame_hist, 3)

    draw.tracking_area(frame)
    draw.frame_count(frame, frame_count, vehicle['videoframes'])

    if ret is True:
        xml_processing.update_info_xml(frame_count, vehicle, dict_lane1,
                                       dict_lane2, dict_lane3)

        try:
            draw.xml_speed_values(frame, dict_lane1['speed'], (143, 43))
        except KeyError:
            pass
        try:
            draw.xml_speed_values(frame, dict_lane2['speed'], (628, 43))
        except KeyError:
            pass
        try:
            draw.xml_speed_values(frame, dict_lane3['speed'], (1143, 43))
        except KeyError:
            pass

        lane1 = ImageProcessing(frame_lane1,
                                bgsMOG, KERNEL_ERODE, KERNEL_DILATE)

        lane1_detection = VehicleDetection(lane1)
        lane1_vehicle_speed = VehicleSpeed()

        lane1_detection.detection()

        if lane1_detection.detected:
            lane1_tracking.tracking(lane1_detection.center, frame_time)
            lane1_vehicle_speed.calc_speed(lane1_tracking, dict_lane1)

            draw.result(frame, lane1_vehicle_speed,
                        lane1_tracking.tracked_blobs['id'], (350, 120))
            draw.car_rectangle(frame, frame_lane1, lane1_detection)
            # ################# END LANE 1  ##############################

        lane2 = ImageProcessing(frame_lane2,
                                bgsMOG, KERNEL_ERODE_L2, KERNEL_DILATE_L2)

        lane2_detection = VehicleDetection(lane2)
        lane2_vehicle_speed = VehicleSpeed()

        lane2_detection.detection()

        if lane2_detection.detected:
            lane2_tracking.tracking(lane2_detection.center, frame_time)
            lane2_vehicle_speed.calc_speed(lane2_tracking, dict_lane2)

            draw.result(frame, lane2_vehicle_speed,
                        lane2_tracking.tracked_blobs['id'], (830, 120))
            draw.car_rectangle(frame, frame_lane2, lane2_detection, 600)
            # ################# END LANE 2  ##############################

        lane3 = ImageProcessing(frame_lane3, bgsMOG,
                                KERNEL_ERODE_L3, KERNEL_DILATE_L3)

        lane3_detection = VehicleDetection(lane3)
        lane3_vehicle_speed = VehicleSpeed()

        lane3_detection.detection()

        if lane3_detection.detected:
            lane3_tracking.tracking(lane3_detection.center, frame_time)
            lane3_vehicle_speed.calc_speed(lane3_tracking, dict_lane3)

            draw.result(frame, lane3_vehicle_speed,
                        lane3_tracking.tracked_blobs['id'], (1350, 120))
            draw.car_rectangle(frame, frame_lane3, lane3_detection, 1270)
            # ################# END LANE 3  ##############################

        # Remove timeout trails
        lane1_tracking.remove_expired_track(frame_time)
        lane2_tracking.remove_expired_track(frame_time)
        lane3_tracking.remove_expired_track(frame_time)

        # Draw center points (center of rectangle)
        draw.blobs(frame_lane1, lane1_tracking.tracked_blobs)
        draw.blobs(frame_lane2, lane2_tracking.tracked_blobs)
        draw.blobs(frame_lane3, lane3_tracking.tracked_blobs)

        draw.avg_fps(frame, avg_fps)

        print(f'************** FIM DO FRAME {frame_count} **************')

        # ########## MOSTRA OS VIDEOS  ########################################
        # cv2.imshow('fgmask', lane1.foreground_mask)
        # cv2.imshow('erodedmask', lane1.eroded_mask)
        # cv2.imshow('dilatedmask', lane1.dilated_mask)

        # cv2.imshow('fgmask_lane2', lane2.foreground_mask)
        # cv2.imshow('erodedmask_lane2', lane2.eroded_mask)
        # cv2.imshow('dilatedmask_lane2', lane2.dilated_mask)

        # cv2.imshow('fgmask_L3', lane3.foreground_mask)
        # cv2.imshow('erodedmask_L3', lane3.eroded_mask)
        # cv2.imshow('dilatedmask_L3', lane3.dilated_mask)

        # cv2.imshow('out', lane1.draw_contours())
        # cv2.imshow('out_L2', lane2.draw_contours())
        # cv2.imshow('out_L3', lane3.draw_contours())

        # cv2.imshow('frame_lane1', frame_lane1)
        # cv2.imshow('frame_lane2', frame_lane2)
        # cv2.imshow('frame_lane3', frame_lane3)
        cv2.imshow('frame', frame)

        frame_count += 1

        end_frame_time = time.time()
        process_times.append(end_frame_time - start_frame_time)
        calculated_fps = int(1 / (end_frame_time - start_frame_time))
        process_times.append(calculated_fps)
        avg_fps = int(np.mean(process_times[-24:]))

        if frame_count == config.CLOSE_VIDEO:  # fecha o video
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Tecla Q para fechar
            break

    else:  # exit from while: ret == False
        break


cap.release()
cv2.destroyAllWindows()
