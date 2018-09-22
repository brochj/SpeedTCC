# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 21:03:24 2018

@author: broch
"""

import cv2
import numpy as np
import os
import time
import uuid
import math
import xml.dom

cap = cv2.VideoCapture("../video01.avi")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))      # Retorna a largura do video
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    # Retorna a altura do video
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))     # Retorna a quantidade de frames

RESIZE_RATIO = 0.35 # U
frameCount = 0

def get_frame():
	" Grabs a frame from the video vcture and resizes it. "
	ret, frame = cap.read()
	if ret:
		(h, w) = frame.shape[:2]
		frame = cv2.resize(frame, (int(w * RESIZE_RATIO), int(h * RESIZE_RATIO)), interpolation=cv2.INTER_CUBIC)
	return ret, frame

while(True):
    ret, frame = get_frame()
    
    if ret == True:
        # Coloca o codigo AQUI watchh

        frame = cv2.putText(frame, 'frame: {}'.format(frameCount), (5, 375), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)

        if frameCount >= 71 and frameCount <= 111:
            outputFrame = cv2.putText(frame, '56.65', (100, 375), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)
        
        if frameCount == 600: # fecha o video
            break
        
        cv2.imshow('frame', frame)
        
        frameCount += 1    # Conta a quantidade de Frames

        if cv2.waitKey(1) & 0xFF == ord('q'): # Pressiona a tecla Q para fechar o video
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()