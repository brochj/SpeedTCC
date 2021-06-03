# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:02:46 2020

@author: broch
"""

import time
import uuid
import numpy as np
#import matplotlib.pyplot as plt
import os
import cv2
import functions as t
import datetime
import colors
import config
from image_processing import ImageProcessing
from tracking import Tracking
import drawings as draw
# import drawings as draw
from sys import exit
# ########  CONSTANT VALUES ###################################################
VIDEO = 1
VIDEO_FILE = './Dataset/video{}.mp4'.format(VIDEO)
XML_FILE = './Dataset/video{}.xml'.format(VIDEO)

RESIZE_RATIO = config.RESIZE_RATIO
if RESIZE_RATIO > 1:
    exit('ERRO: AJUSTE O RESIZE_RATIO')
CLOSE_VIDEO = 2950  # 2950 #5934  # 1-6917 # 5-36253

SHOW_ROI = config.SHOW_ROI
SHOW_TRACKING_AREA = config.SHOW_TRACKING_AREA
SHOW_TRAIL = config.SHOW_TRAIL
SHOW_CAR_RECTANGLE = config.SHOW_CAR_RECTANGLE

SHOW_REAL_SPEEDS = False
SHOW_FRAME_COUNT = True

SKIP_VIDEO = False
SEE_CUTTED_VIDEO = False  # ver partes retiradas, precisa de SKIP_VIDEO = True
# ---- Tracking Values --------------------------------------------------------
# The maximum distance a blob centroid is allowed to move in order to
# consider it a match to a previous scene's blob.
BLOB_LOCKON_DIST_PX_MAX = 150  # default = 50 p/ ratio 0.35
BLOB_LOCKON_DIST_PX_MIN = 5  # default 5
MIN_AREA_FOR_DETEC = 30000  # Default 40000
# Limites da Área de Medição, área onde é feita o Tracking
# Distancia de medição: default 915-430 = 485

# Faixa 1
BOTTOM_LIMIT_TRACK = 910  # 850  # Default 900
UPPER_LIMIT_TRACK = config.UPPER_LIMIT_TRACK  # 350  # Default 430
# Faixa 2
BOTTOM_LIMIT_TRACK_L2 = 940  # 1095  # Default 940
UPPER_LIMIT_TRACK_L2 = 425  # 408 # Default 420
# Faixa 3
BOTTOM_LIMIT_TRACK_L3 = 930  # 1095  # Default 915
UPPER_LIMIT_TRACK_L3 = 430  # 408 # Default 430

MIN_CENTRAL_POINTS = 10  # Minimum number of points needed to calculate speed
# The number of seconds a blob is allowed to sit around without having
# any new blobs matching it.
BLOB_TRACK_TIMEOUT = 0.1  # Default 0.7
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

prev_len_speed = []
prev_speed = 1.0

frameCount = 0  # Armazena a contagem de frames processados do video

results_lane1 = {}
results_lane2 = {}
results_lane3 = {}

process_times = []


# ##############  FUNÇÕES #####################################################
def r(numero):
    return int(numero*RESIZE_RATIO)


def calculate_speed(trails, fps, correction_factor):
    med_area_meter = 3.9  # metros (Valor estimado)
    med_area_pixel = r(485)
    qntd_frames = 11  # len(trails)  # default 11
    dist_pixel = cv2.norm(trails[0], trails[10])  # Sem usar Regressão linear
    dist_meter = dist_pixel*(med_area_meter/med_area_pixel)
    speed = (dist_meter*3.6*correction_factor)/(qntd_frames*(1/fps))
    return round(speed, 1)


# ########## FIM  FUNÇÕES #####################################################
now = datetime.datetime.now()
DATE = f'video{VIDEO}_{now.day}-{now.month}-{now.year}_{now.hour}-{now.minute}-{now.second}'

# Dicionário que armazena todas as informações do xml
vehicle = t.read_xml(XML_FILE, VIDEO, DATE)

KERNEL_ERODE = np.ones((r(12), r(12)), np.uint8)  # Default (r(12), r(12))
KERNEL_DILATE = np.ones((r(120), r(400)), np.uint8)  # Default (r(120), r(400))

KERNEL_ERODE_L2 = np.ones((r(12), r(12)), np.uint8)  # Default (r(8), r(8))
# Default (r(100), r(400))
KERNEL_DILATE_L2 = np.ones((r(100), r(400)), np.uint8)

KERNEL_ERODE_L3 = np.ones((r(12), r(12)), np.uint8)  # Default (r(12), r(12))
# Default (r(100), r(320))
KERNEL_DILATE_L3 = np.ones((r(100), r(320)), np.uint8)

lane1_tracking = Tracking(
    RESIZE_RATIO, BLOB_LOCKON_DIST_PX_MAX, BLOB_LOCKON_DIST_PX_MIN)
lane2_tracking = Tracking(
    RESIZE_RATIO, BLOB_LOCKON_DIST_PX_MAX, BLOB_LOCKON_DIST_PX_MIN)
lane3_tracking = Tracking(
    RESIZE_RATIO, BLOB_LOCKON_DIST_PX_MAX, BLOB_LOCKON_DIST_PX_MIN)


while True:
    ret, frame = t.get_frame(cap, RESIZE_RATIO)
    frame_time = time.time()

    if SKIP_VIDEO:
        skip = t.skip_video(frameCount, VIDEO, frame)
        if SEE_CUTTED_VIDEO:
            if not skip:
                frameCount += 1
                if frameCount == CLOSE_VIDEO:  # fecha o video
                    break
                continue
        else:
            if skip:
                frameCount += 1
                if frameCount == CLOSE_VIDEO:  # fecha o video
                    break
                continue
    start_frame_time = time.time()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    t.region_of_interest(frameGray, RESIZE_RATIO)

    hist = t.histogram_equalization(frameGray)

    frame_lane1 = t.perspective(hist, 1, RESIZE_RATIO)
    frame_lane2 = t.perspective(hist, 2, RESIZE_RATIO)
    frame_lane3 = t.perspective(hist, 3, RESIZE_RATIO)

    if SHOW_ROI:
        t.region_of_interest(frame, RESIZE_RATIO)
    if SHOW_TRACKING_AREA:  # Desenha os Limites da Área de Tracking
        cv2.line(frame, (0, r(UPPER_LIMIT_TRACK)),
                 (WIDTH, r(UPPER_LIMIT_TRACK)), colors.WHITE, 2)
        cv2.line(frame, (0, r(BOTTOM_LIMIT_TRACK)),
                 (WIDTH, r(BOTTOM_LIMIT_TRACK)), colors.WHITE, 2)
    if SHOW_FRAME_COUNT:
        PERCE = str(int((100*frameCount)/vehicle['videoframes']))
        cv2.putText(frame, f'frame: {frameCount} {PERCE}%', (r(
            14), r(1071)), 0, .65, colors.WHITE, 2)

    if ret is True:
        t.update_info_xml(frameCount, vehicle, dict_lane1,
                          dict_lane2, dict_lane3)
        if SHOW_REAL_SPEEDS:
            t.print_xml_values(frame, RESIZE_RATIO,
                               dict_lane1, dict_lane2, dict_lane3)

        lane1 = ImageProcessing(frame_lane1, RESIZE_RATIO,
                                bgsMOG, KERNEL_ERODE, KERNEL_DILATE)

        # create an empty black image
        drawing = t.convert_to_black_image(frame_lane1)
        out = cv2.drawContours(drawing, lane1.hull, 0, colors.WHITE, -1, 8)

        for i in range(len(lane1.contours)):
            if cv2.contourArea(lane1.contours[i]) > r(MIN_AREA_FOR_DETEC):

                (x, y, w, h) = cv2.boundingRect(lane1.hull[i])
                center = (int(x + w/2), int(y + h/2))
                # out = cv2.rectangle(out, (x, y), (x + w, y + h), colors.GREEN, 2) # printa na mask
                # CONDIÇÕES PARA CONTINUAR COM TRACKING

                if w < r(340) and h < r(340):  # ponto que da pra mudar
                    continue
                # Área de medição do Tracking
                if center[1] > r(BOTTOM_LIMIT_TRACK) or center[1] < r(UPPER_LIMIT_TRACK):
                    continue

                draw.car_rectangle(center, frame, frame_lane1, x, y, w, h)

                # ################## TRACKING #################################
                lane1_tracking.tracking(center, frame_time)

                try:
                    if len(lane1_tracking.closest_blob['trail']) > MIN_CENTRAL_POINTS:
                        lane1_tracking.closest_blob['speed'].insert(0, t.calculate_speed(
                            lane1_tracking.closest_blob['trail'], FPS, CF_LANE1))
                        lane = 1
                        ave_speed = np.mean(
                            lane1_tracking.closest_blob['speed'])
                        abs_error, per_error = t.write_results_on_image(frame, frameCount, ave_speed, lane, lane1_tracking.closest_blob['id'], RESIZE_RATIO, VIDEO,
                                                                        dict_lane1, dict_lane2, dict_lane3)

                        results_lane1[str(lane1_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                                                     speeds=lane1_tracking.closest_blob[
                                                                                         'speed'],
                                                                                     frame=frameCount,
                                                                                     real_speed=float(
                                                                                         dict_lane1['speed']),
                                                                                     abs_error=round(
                                                                                         abs_error, 2),
                                                                                     per_error=round(
                                                                                         per_error, 3),
                                                                                     trail=lane1_tracking.closest_blob[
                                                                                         'trail'],
                                                                                     car_id=lane1_tracking.closest_blob['id'])

                        abs_error = []
                        per_error = []
                except:
                    pass

                # ################# END FAIXA 1  ##############################

        lane2 = ImageProcessing(frame_lane2, RESIZE_RATIO,
                                bgsMOG, KERNEL_ERODE_L2, KERNEL_DILATE_L2)

        drawing_L2 = t.convert_to_black_image(frame_lane2)
        out_L2 = cv2.drawContours(
            drawing_L2, lane2.hull, 0, colors.WHITE, -1, 8)

        for i in range(len(lane2.contours)):
            if cv2.contourArea(lane2.contours[i]) > r(MIN_AREA_FOR_DETEC):

                (x_L2, y_L2, w_L2, h_L2) = cv2.boundingRect(lane2.hull[i])
                center_L2 = (int(x_L2 + w_L2/2), int(y_L2 + h_L2/2))
                # out_L2 = cv2.rectangle(out_L2, (x_L2, y_L2), (x_L2 + w_L2, y_L2 + h_L2), colors.GREEN, 2) # printa na mask
                # CONDIÇÕES PARA CONTINUAR COM TRACKING

                if w_L2 < r(340) and h_L2 < r(340):  # ponto que da pra mudar
                    continue
                # Área de medição do Tracking
                if center_L2[1] > r(BOTTOM_LIMIT_TRACK_L2) or center_L2[1] < r(UPPER_LIMIT_TRACK_L2):
                    continue

                draw.car_rectangle(center_L2, frame, frame_lane2,
                                   x_L2, y_L2, w_L2, h_L2, left_padding=600)

                # ################## TRACKING #################################
                lane2_tracking.tracking(center_L2, frame_time)
                try:
                    if len(lane2_tracking.closest_blob['trail']) > MIN_CENTRAL_POINTS:
                        lane2_tracking.closest_blob['speed'].insert(0, t.calculate_speed(
                            lane2_tracking.closest_blob['trail'], FPS, CF_LANE2))
                        lane = 2
                        ave_speed = np.mean(
                            lane2_tracking.closest_blob['speed'])
                        abs_error, per_error = t.write_results_on_image(frame, frameCount, ave_speed, lane, lane2_tracking.closest_blob['id'], RESIZE_RATIO, VIDEO,
                                                                        dict_lane1, dict_lane2, dict_lane3)

                        results_lane2[str(lane2_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                                                     speeds=lane2_tracking.closest_blob[
                                                                                         'speed'],
                                                                                     frame=frameCount,
                                                                                     real_speed=float(
                                                                                         dict_lane2['speed']),
                                                                                     abs_error=round(
                                                                                         abs_error, 2),
                                                                                     per_error=round(
                                                                                         per_error, 3),
                                                                                     trail=lane2_tracking.closest_blob[
                                                                                         'trail'],
                                                                                     car_id=lane2_tracking.closest_blob['id'])

                        abs_error = []
                        per_error = []
                except:
                    pass

                # ################# END TRACKING ##############################
                # ################# END FAIXA 2  ##############################

        lane3 = ImageProcessing(frame_lane3, RESIZE_RATIO,
                                bgsMOG, KERNEL_ERODE_L3, KERNEL_DILATE_L3)

        drawing_L3 = t.convert_to_black_image(frame_lane3)
        out_L3 = cv2.drawContours(
            drawing_L3, lane3.hull, 0, colors.WHITE, -1, 8)
#        areahull = []
        # draw contours_L3 and hull points
        for i in range(len(lane3.contours)):
            if cv2.contourArea(lane3.contours[i]) > r(MIN_AREA_FOR_DETEC):
                # draw ith contour

                (x_L3, y_L3, w_L3, h_L3) = cv2.boundingRect(lane3.hull[i])
                center_L3 = (int(x_L3 + w_L3/2), int(y_L3 + h_L3/2))
                # out = cv2.rectangle(out, (x_L3, y_L3), (x_L3 + w_L3, y_L3 + h_L3), colors.GREEN, 2) # printa na mask
                #  PARA CONTINUAR COM TRACKING
#                if h_L3 > r(HEIGHT)*.80 or w_L3 > r(WIDTH)*.40:
#                    continue

                if w_L3 < r(340) and h_L3 < r(340):  # ponto que da pra mudar
                    continue
                # Área de medição do Tracking
                if center_L3[1] > r(BOTTOM_LIMIT_TRACK_L3) or center_L3[1] < r(UPPER_LIMIT_TRACK_L3):
                    continue

                draw.car_rectangle(center_L3, frame, frame_lane3,
                                   x_L3, y_L3, w_L3, h_L3, left_padding=1270)

                # ################## TRACKING #################################
                lane3_tracking.tracking(center_L3, frame_time)
                try:
                    if len(lane3_tracking.closest_blob['trail']) > MIN_CENTRAL_POINTS:
                        lane3_tracking.closest_blob['speed'].insert(0, calculate_speed(
                            lane3_tracking.closest_blob['trail'], FPS, CF_LANE3))
                        lane = 3
                        ave_speed = np.mean(
                            lane3_tracking.closest_blob['speed'])
                        abs_error, per_error = t.write_results_on_image(frame, frameCount, ave_speed, lane, lane3_tracking.closest_blob['id'], RESIZE_RATIO, VIDEO,
                                                                        dict_lane1, dict_lane2, dict_lane3)

                        results_lane3[str(lane3_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                                                     speeds=lane3_tracking.closest_blob[
                                                                                         'speed'],
                                                                                     frame=frameCount,
                                                                                     real_speed=float(
                                                                                         dict_lane3['speed']),
                                                                                     abs_error=round(
                                                                                         abs_error, 2),
                                                                                     per_error=round(
                                                                                         per_error, 3),
                                                                                     trail=lane3_tracking.closest_blob[
                                                                                         'trail'],
                                                                                     car_id=lane3_tracking.closest_blob['id'])
                        abs_error = []
                        per_error = []

                except:
                    pass

                # ################# END TRACKING ##############################
                # ################# END FAIXA 3  ##############################

        lane1_tracking.remove_expired_track(
            BLOB_TRACK_TIMEOUT, "lane 1", frame_time)
        lane2_tracking.remove_expired_track(
            BLOB_TRACK_TIMEOUT, "lane 2", frame_time)
        lane3_tracking.remove_expired_track(
            BLOB_TRACK_TIMEOUT, "lane 3", frame_time)

        # ################ PRINTA OS BLOBS ####################################
        for blob in lane1_tracking.tracked_blobs:  # Desenha os pontos centrais
            if SHOW_TRAIL:
                # t.print_trail(blob['trail'], frame)
                t.print_trail(blob['trail'], frame_lane1)

        for blob2 in lane2_tracking.tracked_blobs:  # Desenha os pontos centrais
            if SHOW_TRAIL:
                # t.print_trail(blob2['trail'], frame)
                t.print_trail(blob2['trail'], frame_lane2)

        for blob3 in lane3_tracking.tracked_blobs:  # Desenha os pontos centrais
            if SHOW_TRAIL:
                # t.print_trail(blob3['trail'], frame)
                t.print_trail(blob3['trail'], frame_lane3)

        print(f'************** FIM DO FRAME {frameCount} **************')

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

        cv2.imshow('out', out)
        cv2.imshow('out_L2', out_L2)
        cv2.imshow('out_L3', out_L3)

        cv2.imshow('frame_lane1', frame_lane1)
        cv2.imshow('frame_lane2', frame_lane2)
        cv2.imshow('frame_lane3', frame_lane3)
        cv2.imshow('frame', frame)

        frameCount += 1

        end_frame_time = time.time()
        process_times.append(end_frame_time - start_frame_time)

        # if cv2.waitKey(1) & 0xFF == ord('w'):
        #     SHOW_ROI = not SHOW_ROI

        if frameCount == CLOSE_VIDEO:  # fecha o video
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Tecla Q para fechar
            break

    else:  # exit from while: ret == False
        break


cap.release()
cv2.destroyAllWindows()
