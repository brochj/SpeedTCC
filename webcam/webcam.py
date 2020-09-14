# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 23:25:46 2020

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
from image_processing import ImageProcessing
from tracking import Tracking
# import drawings as draw
from sys import exit
# ########  CONSTANT VALUES ###################################################
VIDEO = 1

RESIZE_RATIO = .6667 #0.7697  720p=.6667 480p=.4445 360p=.33333 240p=.22222 144p=.13333
if RESIZE_RATIO > 1:
    exit('ERRO: AJUSTE O RESIZE_RATIO')
CLOSE_VIDEO = 2950 #2950 #5934  # 1-6917 # 5-36253

SHOW_ROI = True
SHOW_TRACKING_AREA = True
SHOW_TRAIL = True
SHOW_CAR_RECTANGLE = True

SHOW_REAL_SPEEDS = False
SHOW_FRAME_COUNT = True

SKIP_VIDEO = False
SEE_CUTTED_VIDEO = False  # ver partes retiradas, precisa de SKIP_VIDEO = True
# ---- Tracking Values --------------------------------------------------------
# The maximum distance a blob centroid is allowed to move in order to
# consider it a match to a previous scene's blob.
BLOB_LOCKON_DIST_PX_MAX = 150  # default = 50 p/ ratio 0.35
BLOB_LOCKON_DIST_PX_MIN = 5  # default 5
MIN_AREA_FOR_DETEC = 20000  # Default 40000 
# Limites da Área de Medição, área onde é feita o Tracking
# Distancia de medição: default 915-430 = 485

# Faixa 1
BOTTOM_LIMIT_TRACK = 470  #850  # Default 900
UPPER_LIMIT_TRACK = 10 #350  # Default 430


MIN_CENTRAL_POINTS = 5 # Minimum number of points needed to calculate speed | default 10
# The number of seconds a blob is allowed to sit around without having
# any new blobs matching it.
BLOB_TRACK_TIMEOUT = 0.5  # Default 0.7 e 0.1
# ---- Speed Values -----------------------------------------------------------
CF_LANE1 = 2.10 #2.10  # default 2.5869977 # Correction Factor

# ----  Save Results Values ---------------------------------------------------
# ####### END - CONSTANT VALUES ###############################################
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#FPS = cap.get(cv2.CAP_PROP_FPS)
FPS = 30.15
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Retorna a largura do video 480
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Retorna a largura do video 640



bgsMOG = cv2.createBackgroundSubtractorMOG2(history=10, varThreshold=50, detectShadows=0)

# Variant Values
dict_lane1 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 1
tracked_blobs = []  # Lista que salva os dicionários dos tracked_blobs


prev_len_speed = []
prev_speed = 1.0
ave_speed = 0.0

frameCount = 0  # Armazena a contagem de frames processados do video

results_lane1 = {}


area_L1 = []
process_times = []


# ##############  FUNÇÕES #####################################################
def r(numero):
    return int(numero*RESIZE_RATIO)

def calculate_speed(trails, fps, correction_factor):
    med_area_meter = 3.9  # metros (Valor estimado)
    med_area_pixel = r(485)
    qntd_frames =  MIN_CENTRAL_POINTS + 1 #len(trails)  # default 11
    dist_pixel = cv2.norm(trails[0], trails[MIN_CENTRAL_POINTS])  # Sem usar Regressão linear
    dist_meter = dist_pixel*(med_area_meter/med_area_pixel)
    speed = (dist_meter*3.6*correction_factor)/(qntd_frames*(1/fps))
    return round(speed,1)


# ########## FIM  FUNÇÕES #####################################################
now = datetime.datetime.now()
DATE = f'video{VIDEO}_{now.day}-{now.month}-{now.year}_{now.hour}-{now.minute}-{now.second}'


KERNEL_ERODE = np.ones((r(5), r(5)), np.uint8)  # Default (r(12), r(12))
KERNEL_DILATE = np.ones((r(120), r(1280)), np.uint8)  # Default (r(120), r(400))


lane1_tracking = Tracking(RESIZE_RATIO, BLOB_LOCKON_DIST_PX_MAX, BLOB_LOCKON_DIST_PX_MIN)



while True:
    ret, frame = t.get_frame(cap, RESIZE_RATIO)
    frame_time = time.time()
    
    start_frame_time = time.time()   
    frame = cv2.flip(frame,1)     
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    t.region_of_interest(frameGray, RESIZE_RATIO)

    hist = t.histogram_equalization(frameGray)
    
    # frame_lane1 = t.perspective(hist, 1, RESIZE_RATIO)

    
    if SHOW_ROI:
        t.region_of_interest(frameGray, RESIZE_RATIO)
    if SHOW_TRACKING_AREA:  # Desenha os Limites da Área de Tracking
        cv2.line(frame, (0, r(UPPER_LIMIT_TRACK)), (WIDTH, r(UPPER_LIMIT_TRACK)), t.WHITE, 2)
        cv2.line(frame, (0, r(BOTTOM_LIMIT_TRACK)), (WIDTH, r(BOTTOM_LIMIT_TRACK)), t.WHITE, 2)
        
    
    if ret is True:
          
        
        lane1 = ImageProcessing(hist, RESIZE_RATIO, bgsMOG, KERNEL_ERODE, KERNEL_DILATE)
        
        # create an empty black image
        drawing = t.convert_to_black_image(frame)
        out = cv2.drawContours(drawing, lane1.hull, 0, t.WHITE, -1, 8)

        for i in range(len(lane1.contours)):
            if cv2.contourArea(lane1.contours[i]) > r(MIN_AREA_FOR_DETEC):

                (x, y, w, h) = cv2.boundingRect(lane1.hull[i])
                center = (int(x + w/2), int(y + h/2))
                # out = cv2.rectangle(out, (x, y), (x + w, y + h), t.GREEN, 2) # printa na mask
                # CONDIÇÕES PARA CONTINUAR COM TRACKING

                if w < r(340) and h < r(340):  # ponto que da pra mudar
                    continue
                # Área de medição do Tracking
                if center[1] > r(BOTTOM_LIMIT_TRACK) or center[1] < r(UPPER_LIMIT_TRACK):
                    continue
                
                
                if SHOW_CAR_RECTANGLE:
                    if center[1] > r(UPPER_LIMIT_TRACK):
                        area_L1.append(w*h)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), t.GREEN, 2)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), t.GREEN, 2)
                        cv2.rectangle(out, (x, y), (x + w, y + h), t.GREEN, 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), t.PINK, 2)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), t.PINK, 2)

                # ################## TRACKING #################################
                lane1_tracking.tracking(center, frame_time)
                            
                try:
                    if len(lane1_tracking.closest_blob['trail']) > MIN_CENTRAL_POINTS:
                        lane1_tracking.closest_blob['speed'].insert(0, calculate_speed(lane1_tracking.closest_blob['trail'], FPS, CF_LANE1))
                        lane = 1
                        ave_speed = round(np.mean(lane1_tracking.closest_blob['speed']),1)
                                           
                        abs_error = []
                        per_error = []
                except:
                    pass
              
                # ################# END FAIXA 1  ##############################


        

        lane1_tracking.remove_expired_track(BLOB_TRACK_TIMEOUT, "lane 1", frame_time)
        cv2.putText(frame, f'speed {ave_speed}', (r(10),r(470)), 2, .9, t.GREEN, thickness=1, lineType=2)
        if not lane1_tracking.tracked_blobs:
           ave_speed = 0.0     
 
        # ################ PRINTA OS BLOBS ####################################
        for blob in lane1_tracking.tracked_blobs:  # Desenha os pontos centrais
            if SHOW_TRAIL:
                # t.print_trail(blob['trail'], frame)
                t.print_trail(blob['trail'], frame)


        print(f'************** FIM DO FRAME {frameCount} **************')
        
       
        
        # ########## MOSTRA OS VIDEOS  ########################################
        cv2.imshow('fgmask', lane1.foreground_mask)
        cv2.imshow('erodedmask',lane1.eroded_mask)
        cv2.imshow('dilatedmask', lane1.dilated_mask)
        

        cv2.imshow('out',out)


        # cv2.imshow('frame_lane1', frame_lane1)

        cv2.imshow('frame', frame)
    
        frameCount += 1    
        
        end_frame_time = time.time()
        process_times.append(end_frame_time - start_frame_time)
        
        
       
        if frameCount == CLOSE_VIDEO:  # fecha o video
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Tecla Q para fechar
            break
        
            
    else:  # exit from while: ret == False
        break



cap.release()
cv2.destroyAllWindows()

