# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 14:27:03 2018

@author: broch
"""
import math
import cv2
trails = [(308, 154), (307, 166), (311, 185), (314, 192), (317, 199), (324, 218), 
          (327, 246), (329, 261), (329, 269), (333, 277), (333, 285), (326, 294), 
          (343, 304), (339, 315)]

fps = 25
WIDTH = 1920

#def calculate_speed (trails, fps):
    # distance: distance on the frame
	# location: x, y coordinates on the frame
	# fps: framerate
	# mmp: meter per pixel
#	dist = cv2.norm(trails[0], trails[10])
dist_x = trails[0][0] - trails[10][0]
dist_y = trails[0][1] - trails[10][1]
dist = cv2.norm(trails[0], trails[10])


d = (3.5/485)*dist
speeds = []

mmp_y = 0.125 / (3 * (1 + (3.22 / 432)) * trails[0][1])
#    mmp_y = 0.2 / (3 * (1 + (3.22 / 432)) * trails[0][1])  # Default
mmp_x = 0.125 / (5 * (1 + (1.5 / 773)) * (WIDTH - trails[0][1]))  
#    mmp_x = 0.2 / (5 * (1 + (1.5 / 773)) * (width - trails[0][1]))  # Default
real_dist = math.sqrt(dist_x * mmp_x * dist_x * mmp_x + dist_y * mmp_y * dist_y * mmp_y)

speed = real_dist * fps * 250 / 3.6
#for i in range(1,300):
#    mmp_y = 0.125 / (3 * (1 + (3.22 / 432)) * i)
#    #    mmp_y = 0.2 / (3 * (1 + (3.22 / 432)) * trails[0][1])  # Default
#    mmp_x = 0.125 / (5 * (1 + (1.5 / 773)) * (WIDTH - i))  
#    #    mmp_x = 0.2 / (5 * (1 + (1.5 / 773)) * (width - trails[0][1]))  # Default
#    real_dist = math.sqrt(dist_x * mmp_x * dist_x * mmp_x + dist_y * mmp_y * dist_y * mmp_y)
#    
#    speed = real_dist * fps * 250 / 3.6
#    speeds.append((i,speed))



def calculate_speed (trails, fps):
    med_area_meter = 3.5 # tamanho da area de medição em metros [eixo y]
    med_area_pixel = 485 # tamanho da area de medição em pixels
    frames = 10
#    c = 0.055383
    c = 0.045383 # fator de correção
    
    dist_pixel = cv2.norm(trails[0], trails[10]) # Distancia entre o ponto 0 e 10
    dist_meter = dist_pixel*(med_area_meter/med_area_pixel)
    speed1 = dist_meter/(frames*(1/fps)*c)
    return speed1

print(calculate_speed(trails, fps))

 



