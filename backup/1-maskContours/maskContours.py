
"""
Created on Mon Sep 17 13:24:34 2018

@author: broch




"""

import cv2
import numpy as np


cap = cv2.VideoCapture("../../video01.avi")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))      # Retorna a largura do video
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    # Retorna a altura do video
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))     # Retorna a quantidade de frames

kernel1 = np.ones((3,3), np.uint8) # Matriz (3,3) com 1 em seus valores -- Usa na funcao de erode
kernel2 = np.ones((15,15), np.uint8) # # Matriz (8,8) com 1 em seus valores -- Usa na funcao de dilate

RESIZE_RATIO = 0.35 # U


bgsMOG = cv2.createBackgroundSubtractorMOG2(history=10, varThreshold = 50, detectShadows=0)

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
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if ret == True:
        # Cria a máscara
        fgmask = bgsMOG.apply(frame, None, -1)
        erodedmask = cv2.erode(fgmask, kernel1, iterations=1) # usa pra tirar os pixels isolados (ruídos)
        dilatedmask = cv2.dilate(erodedmask, kernel2, iterations=1) # usa para evidenciar o objeto em movimento
        # Fim da máscara
        
        _, contours, hierarchy = cv2.findContours(dilatedmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Identifica os contornos
        
        # outputFrame = cv2.drawContours(frame, contours, -1, (0,255,0),3)

        try: hierarchy = hierarchy[0]
        except: hierarchy = []
        a = []
        for contour, hier in zip(contours, hierarchy):
            (x, y, w, h) = cv2.boundingRect(contour)

            if w < 60 and h < 60:
                continue

            center = (int(x + w/2), int(y + h/2))

            if center[1] > 320 or center[1] < 150:
                continue

            # Optionally draw the rectangle around the blob on the frame that we'll show in a UI later
            # frame1 = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Corta e grava as imagens dos carros detectados
            crop_img = frame[y:y+h, x:x+w]
            cv2.imwrite('imagens/frame{}.jpg'.format(frameCount), crop_img)

        outputFrame = cv2.putText(frame, 'frame: {}'.format(frameCount), (5, 375), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)
        
        # cv2.imshow('fgmask', fgmask)
        # cv2.imshow('dilatedmask', dilatedmask)
        # cv2.imshow('outputFrame', outputFrame)

        # Salva imagens
        if frameCount == 68:
            cv2.imwrite('fgmask.jpg', fgmask)
            cv2.imwrite('erodedmask.jpg', erodedmask)
            cv2.imwrite('dilatedmask.jpg', dilatedmask)
            cv2.imwrite('outputFrame.jpg', outputFrame)

        if frameCount == 2000:  # fecha o video
            break

        frameCount = frameCount + 1    # Conta a quantidade de Frames
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Pressiona a tecla Q para fechar o video
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
