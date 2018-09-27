# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 22:48:07 2018

@author: broch
"""
import cv2

RESIZE_RATIO = 0.35

cap = cv2.VideoCapture('../Dataset/video1.avi')

def get_frame():
	#" Grabs a frame from the video vcture and resizes it. "
	ret, frame = cap.read()
	if ret:
		(h, w) = frame.shape[:2]
		frame = cv2.resize(frame, (int(w * RESIZE_RATIO), int(h * RESIZE_RATIO)), interpolation=cv2.INTER_CUBIC)
	return ret, frame
min_thresh=800
max_thresh=10000

'''
	Args 	: Video object and threshold parameters
  	Returns : None
'''
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.createBackgroundSubtractorMOG2()
connectivity = 4
while(cap.isOpened()):
    ret, frame = get_frame()
    if not ret:
        break
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    output = cv2.connectedComponentsWithStats(fgmask, connectivity, cv2.CV_32S)
    for i in range(output[0]):
        if output[2][i][4] >= min_thresh and output[2][i][4] <= max_thresh:
            cv2.rectangle(frame, (output[2][i][0], output[2][i][1]), (
                output[2][i][0] + output[2][i][2], output[2][i][1] + output[2][i][3]), (0, 255, 0), 2)
            
    cv2.imshow('fgmask', fgmask)
    cv2.imshow('detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): #Pressiona a tecla Q para fechar o video
        break
cap.release()
cv2.destroyAllWindows()
    
