# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 18:31:55 2018

@author: broch
"""
import cv2
import numpy as np
#import matplotlib.pyplot as plt
#from shutil import copy2

#import os
x = 4
y = 5
for i in range(10):

    if i < x:  # ponto que da pra mudar
        continue
    # Área de medição do Tracking
    if i > y:
        continue

points = np.array([[[-150, 1080], [480, 1080],
                           [560, 0], [270, 0] ]], np.int32)
pt4 = [70,0]
pt3 = [570,0]
pt2 = [640, 1080]
pt1 = [0, 1080]

width = 640
height = 1080
target_pts = np.array([pt1,pt2,pt3,pt4 ], np.float32)
H, mask_crop = cv2.findHomography(points, target_pts, cv2.RANSAC)
warped_frame = cv2.warpPerspective(frame, H, (width, height))