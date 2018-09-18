
"""
Created on Mon Sep 17 13:24:34 2018

@author: broch
"""

import cv2
import numpy as np


cap = cv2.VideoCapture("video01.avi")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))      # Retorna a largura do video
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    # Retorna a altura do video
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))     # Retorna a quantidade de frames

kernel1 = np.ones((3,3), np.uint8) # Matriz (3,3) com 1 em seus valores -- Usa na funcao de erode
kernel2 = np.ones((20,20), np.uint8) # # Matriz (8,8) com 1 em seus valores -- Usa na funcao de dilate
kernel3 = np.ones((3,3), np.uint8) # # Matriz (8,8) com 1 em seus valores -- Usa na funcao de dilate


bgsMOG = cv2.createBackgroundSubtractorMOG2(history=10, varThreshold = 50, detectShadows=0)

frameCount = 0

while(True):
    ret , frame = cap.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if ret == True:
        # Cria a máscara
        fgmask = bgsMOG.apply(frame, None, -1)
        erodedmask = cv2.erode(fgmask, kernel1 ,iterations=1) # usa pra tirar os pixels isolados (ruídos)
        dilatedmask = cv2.dilate(erodedmask, kernel2 ,iterations=1) # usa para evidenciar o objeto em movimento
        erodedmask = cv2.erode(fgmask, kernel3 ,iterations=1) # usa pra tirar os pixels isolados (ruídos)
        # Fim da máscara
        
        _, contours, hierarchy = cv2.findContours(dilatedmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        frame1 = cv2.drawContours(frame, contours, -1, (0,255,0),3)
        
        
#        try: hierarchy = hierarchy[0]
#        except: hierarchy = []
#        a = []
#        for contour, hier in zip(contours, hierarchy):
#            (x, y, w, h) = cv2.boundingRect(contour)
#
#            if w < 10 and h < 10:
#                continue
#
#            center = (int(x + w/2), int(y + h/2))
#
#            if center[1] > 320 or center[1] < 150:
#                continue
#
#				# Optionally draw the rectangle around the blob on the frame that we'll show in a UI later
#            frame1 = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        
        cv2.imshow('frame', frame1)
        frameCount = frameCount + 1         
        if cv2.waitKey(1) & 0xFF == ord('q'): #Pressiona a tecla Q para fechar o video
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
