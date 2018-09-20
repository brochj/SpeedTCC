
"""
Created on Mon Sep 17 13:24:34 2018

@author: broch
"""

import cv2
import numpy as np
#import os
#import time
#import uuid
#import math

cap = cv2.VideoCapture("../video01.avi")
#width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))      # Retorna a largura do video
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    # Retorna a altura do video
#length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))     # Retorna a quantidade de frames

kernel1 = np.ones((3,3), np.uint8) # Matriz (3,3) com 1 em seus valores -- Usa na funcao de erode
kernel2 = np.ones((8,8), np.uint8) # # Matriz (8,8) com 1 em seus valores -- Usa na funcao de dilate
kernel3 = np.ones((3,3), np.uint8) # # Matriz (8,8) com 1 em seus valores -- Usa na funcao de dilate

RESIZE_RATIO = 0.35 # 


bgsMOG = cv2.createBackgroundSubtractorMOG2(history=10, varThreshold = 50, detectShadows=0)

frameCount = 0
rectCount = 0

def get_frame():
	" Grabs a frame from the video vcture and resizes it. "
	ret, frame = cap.read()
	if ret:
		(h, w) = frame.shape[:2]
		frame = cv2.resize(frame, (int(w * RESIZE_RATIO), int(h * RESIZE_RATIO)), interpolation=cv2.INTER_CUBIC)
	return ret, frame

while(True):
#    ret , frame = cap.read()
    ret, frame = get_frame()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    edged = cv2.Canny(frameGray, 30, 200)
    
    if ret == True:
        # Cria a máscara
        fgmask = bgsMOG.apply(frameGray, None, 0.01)
        erodedmask = cv2.erode(fgmask, kernel1 ,iterations=1) # usa pra tirar os pixels isolados (ruídos)
        dilatedmask = cv2.dilate(erodedmask, kernel2 ,iterations=1) # usa para evidenciar o objeto em movimento
#        erodedmask = cv2.erode(fgmask, kernel3 ,iterations=1) # usa pra tirar os pixels isolados (ruídos)
        # Fim da máscara
        _, contours, hierarchy = cv2.findContours(dilatedmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
#        outputFrame = cv2.drawContours(frame, contours, -1, (0,255,0),3)
        
        
        try: hierarchy = hierarchy[0]
        except: hierarchy = []
        a = []
        for contour, hier in zip(contours, hierarchy):
            (x, y, w, h) = cv2.boundingRect(contour)

            if w < 60 and h < 60:
                continue
            if w > 400 and h > 280:
                continue
            area = h * w
            if area > 10000 :
                continue

            center = (int(x + w/2), int(y + h/2))

            if center[1] > 320 or center[1] < 150:
                continue

				# Optionally draw the rectangle around the blob on the frame that we'll show in a UI later
            outputFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rectCount += 1
        
        outputFrame = cv2.putText(frame, 'frame: {}'.format(frameCount), (5,375), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2)
        outputFrame = cv2.putText(frame, 'Retangulos: {}'.format(rectCount), (200,375), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2)
        
        if frameCount >= 71 and frameCount <= 111:
            outputFrame=  cv2.putText(frame, '56.65', (100,375), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2)

        if frameCount == 400: #fecha o video
            break
        
        
        
#        cv2.imshow('erodedmask',erodedmask)
#        cv2.imshow('dilatedmask', dilatedmask)
        cv2.imshow('outputFrame', outputFrame)
        
        frameCount = frameCount + 1    # Conta a quantidade de Frames
        
        
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'): #Pressiona a tecla Q para fechar o video
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
