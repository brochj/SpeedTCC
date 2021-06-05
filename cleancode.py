# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:02:46 2020

@author: broch
"""

import time
import uuid
import numpy as np
import os
import cv2
import functions as t
from functions import r
import datetime
import colors
import config
from image_processing import ImageProcessing
import xml_processing
from tracking import Tracking
import drawings as draw
from sys import exit
# ########  CONSTANT VALUES ###################################################
VIDEO = 1
VIDEO_FILE = './Dataset/video{}.mp4'.format(VIDEO)
XML_FILE = './Dataset/video{}.xml'.format(VIDEO)

if config.RESIZE_RATIO > 1:
    exit('ERRO: AJUSTE O RESIZE_RATIO')
# config.CLOSE_VIDEO = 957  # 2950 #5934  # 1-6917 # 5-36253

# config.SKIP_VIDEO = True
# config.SEE_CUTTED_VIDEO = False  # ver partes retiradas, precisa de config.SKIP_VIDEO = True
# ---- Speed Values -----------------------------------------------------------
CF_LANE1 = 2.10  # 2.10  # default 2.5869977 # Correction Factor
CF_LANE2 = 2.32  # default 2.32    3.758897
CF_LANE3 = 2.3048378  # default 2.304837879578
# ----  Save Results Values ---------------------------------------------------
# ####### END - CONSTANT VALUES ###############################################
cap = cv2.VideoCapture(VIDEO_FILE)
#FPS = cap.get(cv2.CAP_PROP_FPS)
FPS = 30.15
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Retorna a largura do video
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Retorna a largura do video

bgsMOG = cv2.createBackgroundSubtractorMOG2(
    history=10, varThreshold=50, detectShadows=0)

# Variant Values
dict_lane1 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 1
dict_lane2 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 2
dict_lane3 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 3
tracked_blobs = []  # Lista que salva os dicionários dos tracked_blobs
tracked_blobs_lane2 = []  # Lista que salva os dicionários dos tracked_blobs
tracked_blobs_lane3 = []


frame_count = 0  # Armazena a contagem de frames processados do video

process_times = []

now = datetime.datetime.now()
DATE = f'video{VIDEO}_{now.day}-{now.month}-{now.year}_{now.hour}-{now.minute}-{now.second}'

# Dicionário que armazena todas as informações do xml
vehicle = xml_processing.read_xml(XML_FILE, VIDEO, DATE)

KERNEL_ERODE = np.ones((r(12), r(12)), np.uint8)  # Default (r(12), r(12))
KERNEL_DILATE = np.ones((r(120), r(400)), np.uint8)  # Default (r(120), r(400))

KERNEL_ERODE_L2 = np.ones((r(12), r(12)), np.uint8)  # Default (r(8), r(8))
# Default (r(100), r(400))
KERNEL_DILATE_L2 = np.ones((r(100), r(400)), np.uint8)

KERNEL_ERODE_L3 = np.ones((r(12), r(12)), np.uint8)  # Default (r(12), r(12))
# Default (r(100), r(320))
KERNEL_DILATE_L3 = np.ones((r(100), r(320)), np.uint8)

lane1_tracking = Tracking()
lane2_tracking = Tracking()
lane3_tracking = Tracking()


while True:
    ret, frame = t.get_frame(cap)
    frame_time = time.time()

    if config.SKIP_VIDEO:
        skip = t.skip_video(frame_count, VIDEO, frame)
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
    t.region_of_interest(frameGray, config.RESIZE_RATIO)

    hist = t.histogram_equalization(frameGray)

    frame_lane1 = t.perspective(hist, 1)
    frame_lane2 = t.perspective(hist, 2)
    frame_lane3 = t.perspective(hist, 3)

    if config.SHOW_ROI:
        t.region_of_interest(frame, config.RESIZE_RATIO)
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

        for i in range(len(lane1.contours)):
            if cv2.contourArea(lane1.contours[i]) > r(config.MIN_AREA_FOR_DETEC):

                (x, y, w, h) = cv2.boundingRect(lane1.hull[i])
                center = (int(x + w/2), int(y + h/2))
                # CONDIÇÕES PARA CONTINUAR COM TRACKING
                if w < r(340) and h < r(340):  # ponto que da pra mudar
                    continue
                # Área de medição do Tracking
                if center[1] > r(config.BOTTOM_LIMIT_TRACK) or center[1] < r(config.UPPER_LIMIT_TRACK):
                    continue

                draw.car_rectangle(center, frame, frame_lane1, x, y, w, h)

                # ################## TRACKING #################################
                lane1_tracking.tracking(center, frame_time)

                try:
                    if len(lane1_tracking.closest_blob['trail']) > config.MIN_CENTRAL_POINTS:
                        lane1_tracking.closest_blob['speed'].insert(0, t.calculate_speed(
                            lane1_tracking.closest_blob['trail'], FPS, CF_LANE1))
                        ave_speed = t.calculate_avg_speed(
                            lane1_tracking.closest_blob['speed'])
                        abs_error, per_error = t.calculate_errors(
                            ave_speed, dict_lane1['speed'])
                        draw.result(frame, ave_speed, abs_error, per_error,
                                    lane1_tracking.closest_blob['id'], (350, 120))

                        abs_error = []
                        per_error = []
                except:
                    pass

                # ################# END FAIXA 1  ##############################

        lane2 = ImageProcessing(frame_lane2,
                                bgsMOG, KERNEL_ERODE_L2, KERNEL_DILATE_L2)

        for i in range(len(lane2.contours)):
            if cv2.contourArea(lane2.contours[i]) > r(config.MIN_AREA_FOR_DETEC):

                (x_L2, y_L2, w_L2, h_L2) = cv2.boundingRect(lane2.hull[i])
                center_L2 = (int(x_L2 + w_L2/2), int(y_L2 + h_L2/2))

                if w_L2 < r(340) and h_L2 < r(340):  # ponto que da pra mudar
                    continue
                # Área de medição do Tracking
                if center_L2[1] > r(config.BOTTOM_LIMIT_TRACK_L2) or center_L2[1] < r(config.UPPER_LIMIT_TRACK_L2):
                    continue

                draw.car_rectangle(center_L2, frame, frame_lane2,
                                   x_L2, y_L2, w_L2, h_L2, left_padding=600)

                # ################## TRACKING #################################
                lane2_tracking.tracking(center_L2, frame_time)
                try:
                    if len(lane2_tracking.closest_blob['trail']) > config.MIN_CENTRAL_POINTS:
                        lane2_tracking.closest_blob['speed'].insert(0, t.calculate_speed(
                            lane2_tracking.closest_blob['trail'], FPS, CF_LANE2))
                        ave_speed = t.calculate_avg_speed(
                            lane2_tracking.closest_blob['speed'])
                        abs_error, per_error = t.calculate_errors(
                            ave_speed, dict_lane2['speed'])
                        draw.result(frame, ave_speed, abs_error, per_error,
                                    lane2_tracking.closest_blob['id'], (830, 120))

                        abs_error = []
                        per_error = []
                except:
                    pass

                # ################# END TRACKING ##############################
                # ################# END FAIXA 2  ##############################

        lane3 = ImageProcessing(frame_lane3, bgsMOG,
                                KERNEL_ERODE_L3, KERNEL_DILATE_L3)

        # draw contours_L3 and hull points
        for i in range(len(lane3.contours)):
            if cv2.contourArea(lane3.contours[i]) > r(config.MIN_AREA_FOR_DETEC):
                # draw ith contour

                (x_L3, y_L3, w_L3, h_L3) = cv2.boundingRect(lane3.hull[i])
                center_L3 = (int(x_L3 + w_L3/2), int(y_L3 + h_L3/2))

                if w_L3 < r(340) and h_L3 < r(340):  # ponto que da pra mudar
                    continue
                # Área de medição do Tracking
                if center_L3[1] > r(config.BOTTOM_LIMIT_TRACK_L3) or center_L3[1] < r(config.UPPER_LIMIT_TRACK_L3):
                    continue

                draw.car_rectangle(center_L3, frame, frame_lane3,
                                   x_L3, y_L3, w_L3, h_L3, left_padding=1270)

                # ################## TRACKING #################################
                lane3_tracking.tracking(center_L3, frame_time)
                try:
                    if len(lane3_tracking.closest_blob['trail']) > config.MIN_CENTRAL_POINTS:
                        lane3_tracking.closest_blob['speed'].insert(0, t.calculate_speed(
                            lane3_tracking.closest_blob['trail'], FPS, CF_LANE3))
                        ave_speed = t.calculate_avg_speed(
                            lane3_tracking.closest_blob['speed'])
                        abs_error, per_error = t.calculate_errors(
                            ave_speed, dict_lane3['speed'])
                        draw.result(frame, ave_speed, abs_error, per_error,
                                    lane3_tracking.closest_blob['id'], (1350, 120))

                        abs_error = []
                        per_error = []

                except:
                    pass

                # ################# END TRACKING ##############################
                # ################# END FAIXA 3  ##############################

        # Remove timeout trails
        lane1_tracking.remove_expired_track("lane 1", frame_time)
        lane2_tracking.remove_expired_track("lane 2", frame_time)
        lane3_tracking.remove_expired_track("lane 3", frame_time)

        # Draw center points (center of rectangle)
        draw.blobs(frame_lane1, lane1_tracking.tracked_blobs)
        draw.blobs(frame_lane2, lane2_tracking.tracked_blobs)
        draw.blobs(frame_lane3, lane3_tracking.tracked_blobs)

        print(f'************** FIM DO FRAME {frame_count} **************')

        # ########## MOSTRA OS VIDEOS  ########################################
        cv2.imshow('fgmask', lane1.foreground_mask)
        cv2.imshow('erodedmask', lane1.eroded_mask)
        cv2.imshow('dilatedmask', lane1.dilated_mask)

        cv2.imshow('fgmask_lane2', lane2.foreground_mask)
        cv2.imshow('erodedmask_lane2', lane2.eroded_mask)
        cv2.imshow('dilatedmask_lane2', lane2.dilated_mask)

        cv2.imshow('fgmask_L3', lane3.foreground_mask)
        cv2.imshow('erodedmask_L3', lane3.eroded_mask)
        cv2.imshow('dilatedmask_L3', lane3.dilated_mask)

        cv2.imshow('out', lane1.draw_contours())
        cv2.imshow('out_L2', lane2.draw_contours())
        cv2.imshow('out_L3', lane3.draw_contours())

        cv2.imshow('frame_lane1', frame_lane1)
        cv2.imshow('frame_lane2', frame_lane2)
        cv2.imshow('frame_lane3', frame_lane3)
        cv2.imshow('frame', frame)

        frame_count += 1

        process_times.append(time.time() - start_frame_time)

        if frame_count == config.CLOSE_VIDEO:  # fecha o video
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Tecla Q para fechar
            break

    else:  # exit from while: ret == False
        break


cap.release()
cv2.destroyAllWindows()
