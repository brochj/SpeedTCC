# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:03:34 2018

@author: broch
"""
import cv2
import numpy as np
 
src = cv2.imread("sample2.jpg", 1) # read input image
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) # convert to grayscale
blur = cv2.blur(gray, (3, 3)) # blur the image
ret, thresh = cv2.threshold(blur,70, 255, cv2.THRESH_BINARY)

# Finding contours for the thresholded image
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# create hull array for convex hull points
hull = []
approx = []
# calculate points for each contour
for i in range(len(contours)):
        # creating convex hull object for each contour
    hull.append(cv2.convexHull(contours[i], False))

    
    # create an empty black image
drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)

#crop_img = frame[y:y+h, x:x+w]
#cv2.imwrite('drawing.jpg', drawing)

area = []
areahull = []

#draw contours and hull points
for i in range(len(contours)):
    if cv2.contourArea(contours[i]) > 1000:
        color_contours = (0, 255, 0) # green - color for contours
        color = (255, 255, 255) # blue - color for convex hull
        # draw ith contour
        cv2.drawContours(drawing, contours, i, color_contours, 0, 8, hierarchy)
        # draw ith convex hull object
        out = cv2.drawContours(drawing, hull, i, color, -1, 8)
        area.append(cv2.contourArea(contours[i]))
        areahull.append(cv2.contourArea(hull[i]))

#OR
drawing2 = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
out2 = cv2.drawContours(drawing2, contours, -1, (0, 255, 0), 0, 8, hierarchy)
out2 = cv2.drawContours(drawing2, hull, -1, (255, 255, 255), 0, 8)

drawing4 = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
cont = cv2.drawContours(drawing4, contours, -1, (0, 255, 0), 0, 8, hierarchy)

drawing3 = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
out3 = cv2.drawContours(drawing3, hull, -1, (255, 255, 255), -1, 8)


cv2.imshow('Parte 1 -  Mask', thresh)
cv2.imshow('Parte 2 : Desenhando os Contornos', cont)
cv2.imshow('Parte 3 : ConvexHull(linha branca) engloba os contornos (linha verde)', out2)
cv2.imshow('Parte 4 : Preenchendo a area do ConvexHull', out3)
cv2.imshow('Parte 5 : Definindo limites de area a serem mostrados', out)


cv2.waitKey(0)
cv2.destroyAllWindows()