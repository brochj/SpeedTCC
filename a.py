# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 15:10:06 2018

@author: broch
"""
import cv2

def calculate_speed(trails, fps):
    med_area_meter = 3.5  # metros (Valor estimado)
    med_area_pixel = 485
    qntd_frames = len(trails)  # default 11
#    initial_pt, final_pt = t.linearRegression(trails, qntd_frames)  # Usando Regressão Linear
    dist_pixel = cv2.norm(final_pt, initial_pt)
#    dist_pixel1 = cv2.norm(trails[0], trails[10])  # Sem usar Regressão linear
#    if SHOW_LINEAR_REGRESSION:
#        cv2.line(frame, initial_pt, final_pt, t.ORANGE, 5)
#    cv2.line(frame,trails[0],trails[10], t.GREEN, 2)
#    cv2.imwrite('img/regressao1_{}.png'.format(frameCount), frame)
    dist_meter = dist_pixel*(med_area_meter/med_area_pixel)
    speed = (dist_meter*3.6*cf)/(qntd_frames*(1/fps))
    return speed