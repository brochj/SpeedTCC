# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 14:50:08 2020

@author: broch
"""
# import numpy as np
import cv2

class ImageProcessing:
    def __init__(self, frame, resize_ratio, background_subtractor, kernel_erode, kernel_dilate):
        self.resize_ratio = resize_ratio
        self.frame = frame
        self.bg_subtractor = background_subtractor
        self.kernel_erode = kernel_erode
        self.kernel_dilate = kernel_dilate
        self.foreground_mask = None
        self.eroded_mask = None
        self.dilated_mask = None
        self.contours = None
        self.hierarchy = None
        self.hull = None
        
        self.apply_bg_subtractor()
        self.apply_erode()
        self.apply_dilate()
        self.apply_contourns()
        self.apply_convex_hull()
        
    
    def apply_bg_subtractor(self):
        self.foreground_mask = self.bg_subtractor.apply(self.frame, None, 0.01)
        return self.foreground_mask

    
    def apply_erode(self):
        self.eroded_mask = cv2.erode(self.foreground_mask, self.kernel_erode, iterations=1)
        return self.eroded_mask

    
    def apply_dilate(self):
        self.dilated_mask = cv2.dilate(self.eroded_mask, self.kernel_dilate, iterations=1)
        return self.dilated_mask

    
    def apply_contourns(self):
        self.contours, self.hierarchy = cv2.findContours(self.dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return self.contours

    
    def draw_contourns(self):
        pass
    
   
    def apply_convex_hull(self):
        self.hull = []
        for i in range(len(self.contours)):  # calculate points for each contour
            # creating convex hull object for each contour
            self.hull.append(cv2.convexHull(self.contours[i], False))
        
    
    

if __name__ == '__main__':
    print('arquivo ERRADO')