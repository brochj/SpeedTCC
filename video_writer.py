# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:02:46 2020

@author: broch

Esse arquivo é para salvar trechos em videos
"""

from sys import exit
import cv2
import datetime
import numpy as np
import os
import time
import uuid

# Created modules
from lib.functions import r
from image_processing import ImageProcessing
from tracking import Tracking
from vehicle_detection import VehicleDetection
from vehicle_speed import VehicleSpeed
import lib.colors as colors
import configs.config as config
import lib.drawings as draw
import lib.functions as t
import xml_processing

if config.RESIZE_RATIO > 1:
    exit("ERROR: The RESIZE_RATIO cannot be greater than 1")

cap = cv2.VideoCapture(config.VIDEO_FILE)
FPS = 25  # cap.get(cv2.CAP_PROP_FPS)
WIDTH = int(r(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
HEIGHT = int(r(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

START = 100
END = 200

FOURCC = cv2.VideoWriter_fourcc("m", "p", "4", "v")

# Video Writers
frame_writer = cv2.VideoWriter("videos/frame_writer.mp4", FOURCC, FPS, (WIDTH, HEIGHT))
final_frame_writer = cv2.VideoWriter(
    "videos/final_frame_writer.avi", FOURCC, FPS, (WIDTH, HEIGHT)
)


frame_gray_writer = cv2.VideoWriter(
    "videos/frame_gray_writer.mp4", FOURCC, FPS, (WIDTH, HEIGHT), False
)
frame_roi_writer = cv2.VideoWriter(
    "videos/frame_roi_writer.mp4", FOURCC, FPS, (WIDTH, HEIGHT), False
)
frame_hist_writer = cv2.VideoWriter(
    "videos/frame_hist_writer.mp4", FOURCC, FPS, (WIDTH, HEIGHT), False
)

frame_perspective_1 = cv2.VideoWriter(
    "videos/frame_perspective_1.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_perspective_2 = cv2.VideoWriter(
    "videos/frame_perspective_2.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_perspective_3 = cv2.VideoWriter(
    "videos/frame_perspective_3.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_perspective = cv2.VideoWriter(
    "videos/frame_perspective.mp4", FOURCC, FPS, (r(1920), r(1080)), False
)

frame_bgs_1 = cv2.VideoWriter(
    "videos/frame_bgs_1.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_bgs_2 = cv2.VideoWriter(
    "videos/frame_bgs_2.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_bgs_3 = cv2.VideoWriter(
    "videos/frame_bgs_3.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_bgs = cv2.VideoWriter(
    "videos/frame_bgs.mp4", FOURCC, FPS, (r(1920), r(1080)), False
)

frame_eroded_1 = cv2.VideoWriter(
    "videos/frame_eroded_1.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_eroded_2 = cv2.VideoWriter(
    "videos/frame_eroded_2.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_eroded_3 = cv2.VideoWriter(
    "videos/frame_eroded_3.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_eroded = cv2.VideoWriter(
    "videos/frame_eroded.mp4", FOURCC, FPS, (r(1920), r(1080)), False
)

frame_dilated_1 = cv2.VideoWriter(
    "videos/frame_dilated_1.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_dilated_2 = cv2.VideoWriter(
    "videos/frame_dilated_2.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_dilated_3 = cv2.VideoWriter(
    "videos/frame_dilated_3.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_dilated = cv2.VideoWriter(
    "videos/frame_dilated.mp4", FOURCC, FPS, (r(1920), r(1080)), False
)

frame_contours_1 = cv2.VideoWriter(
    "videos/frame_contours_1.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_contours_2 = cv2.VideoWriter(
    "videos/frame_contours_2.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_contours_3 = cv2.VideoWriter(
    "videos/frame_contours_3.mp4", FOURCC, FPS, (r(640), r(1080)), False
)
frame_contours = cv2.VideoWriter(
    "videos/frame_contours.mp4", FOURCC, FPS, (r(1920), r(1080)), False
)

bgs_ero_dila = cv2.VideoWriter(
    "videos/bgs_ero_dila.mp4", FOURCC, FPS, (r(1920), r(1080)), False
)


bgsMOG = cv2.createBackgroundSubtractorMOG2(
    history=10, varThreshold=50, detectShadows=0
)

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

KERNEL_ERODE = np.ones((r(12), r(12)), np.uint8)  # Default (r(12), r(12))
KERNEL_DILATE = np.ones((r(120), r(400)), np.uint8)  # Default (r(120), r(400))

KERNEL_ERODE_L2 = np.ones((r(12), r(12)), np.uint8)  # Default (r(8), r(8))
# Default (r(100), r(400))
KERNEL_DILATE_L2 = np.ones((r(100), r(400)), np.uint8)

KERNEL_ERODE_L3 = np.ones((r(12), r(12)), np.uint8)  # Default (r(12), r(12))
# Default (r(100), r(320))
KERNEL_DILATE_L3 = np.ones((r(100), r(320)), np.uint8)

lane1_tracking = Tracking("lane 1")
lane2_tracking = Tracking("lane 2")
lane3_tracking = Tracking("lane 3")


while True:
    ret, frame = t.get_frame(cap)
    frame_time = time.time()

    if config.SKIP_VIDEO:
        skip = t.skip_video(frame_count, config.VIDEO, frame)
        if config.SEE_CUTTED_VIDEO:
            if not skip:
                frame_count += 1
                if frame_count == config.CLOSE_VIDEO:  # fecha o video
                    break
                continue
        else:
            if skip:
                frame_count += 1
                if frame_count == config.CLOSE_VIDEO:  # fecha o video
                    break
                continue
    start_frame_time = time.time()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if frame_count > START and frame_count < END:
        frame_gray_writer.write(frameGray)

    t.region_of_interest(frameGray, config.RESIZE_RATIO)

    hist = t.histogram_equalization(frameGray)

    frame_lane1 = t.perspective(hist, 1)
    frame_lane2 = t.perspective(hist, 2)
    frame_lane3 = t.perspective(hist, 3)

    if frame_count > START and frame_count < END:
        frame_writer.write(frame)
        frame_roi_writer.write(frameGray)
        frame_hist_writer.write(hist)
        frame_perspective_1.write(frame_lane1)
        frame_perspective_2.write(frame_lane2)
        frame_perspective_3.write(frame_lane3)
        frame_perspective.write(
            np.concatenate((frame_lane1, frame_lane2, frame_lane3), axis=1)
        )

    if config.SHOW_ROI:
        t.region_of_interest(frame, config.RESIZE_RATIO)
    draw.tracking_area(frame)
    draw.frame_count(frame, frame_count, vehicle["videoframes"])

    if ret is True:
        xml_processing.update_info_xml(
            frame_count, vehicle, dict_lane1, dict_lane2, dict_lane3
        )

        try:
            draw.xml_speed_values(frame, dict_lane1["speed"], (143, 43))
        except KeyError:
            pass
        try:
            draw.xml_speed_values(frame, dict_lane2["speed"], (628, 43))
        except KeyError:
            pass
        try:
            draw.xml_speed_values(frame, dict_lane3["speed"], (1143, 43))
        except KeyError:
            pass

        lane1 = ImageProcessing(frame_lane1, bgsMOG, KERNEL_ERODE, KERNEL_DILATE)

        lane1_detection = VehicleDetection(lane1)
        lane1_vehicle_speed = VehicleSpeed()

        lane1_detection.detection()

        if lane1_detection.detected:
            lane1_tracking.tracking(lane1_detection.center, frame_time)
            lane1_vehicle_speed.calc_speed(lane1_tracking, dict_lane1)

            draw.result(
                frame,
                lane1_vehicle_speed,
                lane1_tracking.tracked_blobs["id"],
                (350, 120),
            )
            draw.car_rectangle(frame, frame_lane1, lane1_detection)
            # ################# END LANE 1  ##############################

        lane2 = ImageProcessing(frame_lane2, bgsMOG, KERNEL_ERODE_L2, KERNEL_DILATE_L2)

        lane2_detection = VehicleDetection(lane2)
        lane2_vehicle_speed = VehicleSpeed()

        lane2_detection.detection()

        if lane2_detection.detected:
            lane2_tracking.tracking(lane2_detection.center, frame_time)
            lane2_vehicle_speed.calc_speed(lane2_tracking, dict_lane2)

            draw.result(
                frame,
                lane2_vehicle_speed,
                lane2_tracking.tracked_blobs["id"],
                (830, 120),
            )
            draw.car_rectangle(frame, frame_lane2, lane2_detection, 600)
            # ################# END LANE 2  ##############################

        lane3 = ImageProcessing(frame_lane3, bgsMOG, KERNEL_ERODE_L3, KERNEL_DILATE_L3)

        lane3_detection = VehicleDetection(lane3)
        lane3_vehicle_speed = VehicleSpeed()

        lane3_detection.detection()

        if lane3_detection.detected:
            lane3_tracking.tracking(lane3_detection.center, frame_time)
            lane3_vehicle_speed.calc_speed(lane3_tracking, dict_lane3)

            draw.result(
                frame,
                lane3_vehicle_speed,
                lane3_tracking.tracked_blobs["id"],
                (1350, 120),
            )
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

        # draw.avg_fps(frame, avg_fps)

        print(f"************** FIM DO FRAME {frame_count} **************")

        if frame_count > START and frame_count < END:
            frame_bgs_1.write(lane1.foreground_mask)
            frame_bgs_2.write(lane2.foreground_mask)
            frame_bgs_3.write(lane3.foreground_mask)
            frame_bgs.write(
                np.concatenate(
                    (
                        lane1.foreground_mask,
                        lane2.foreground_mask,
                        lane3.foreground_mask,
                    ),
                    axis=1,
                )
            )

            frame_eroded_1.write(lane1.eroded_mask)
            frame_eroded_2.write(lane2.eroded_mask)
            frame_eroded_3.write(lane3.eroded_mask)
            frame_eroded.write(
                np.concatenate(
                    (lane1.eroded_mask, lane2.eroded_mask, lane3.eroded_mask), axis=1
                )
            )

            frame_dilated_1.write(lane1.dilated_mask)
            frame_dilated_2.write(lane2.dilated_mask)
            frame_dilated_3.write(lane3.dilated_mask)
            frame_dilated.write(
                np.concatenate(
                    (lane1.dilated_mask, lane2.dilated_mask, lane3.dilated_mask), axis=1
                )
            )

            frame_contours_1.write(lane1.draw_contours())
            frame_contours_2.write(lane2.draw_contours())
            frame_contours_3.write(lane3.draw_contours())
            frame_contours.write(
                np.concatenate(
                    (
                        lane1.draw_contours(),
                        lane2.draw_contours(),
                        lane3.draw_contours(),
                    ),
                    axis=1,
                )
            )

            bgs_ero_dila.write(
                np.concatenate(
                    (lane3.foreground_mask, lane3.eroded_mask, lane3.dilated_mask),
                    axis=1,
                )
            )

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
        cv2.imshow("frame", frame)

        if frame_count > START and frame_count < END:
            final_frame_writer.write(frame)

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
# videos releases

frame_writer.release()
final_frame_writer.release()
frame_gray_writer.release()
frame_roi_writer.release()
frame_hist_writer.release()
frame_perspective_1.release()
frame_perspective_2.release()
frame_perspective_3.release()
frame_perspective.release()
frame_bgs_1.release()
frame_bgs_2.release()
frame_bgs_3.release()
frame_bgs.release()
frame_eroded_1.release()
frame_eroded_2.release()
frame_eroded_3.release()
frame_eroded.release()
frame_dilated_1.release()
frame_dilated_2.release()
frame_dilated_3.release()
frame_dilated.release()
frame_contours_1.release()
frame_contours_2.release()
frame_contours_3.release()
frame_contours.release()
bgs_ero_dila.release()

cv2.destroyAllWindows()
