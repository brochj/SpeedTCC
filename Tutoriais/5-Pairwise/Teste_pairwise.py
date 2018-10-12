# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 10:11:18 2018

@author: broch
"""
#%%
LINE_THICKNESS = 1
from itertools import *
def pairwise(iterable):
	r"s -> (s0,s1), (s1,s2), (s2, s3), ..."
	a, b = tee(iterable)
	next(b, None)
	return zip(a, b)

tracked_blobs = [(1,2), (3,4), (5,6), (7,8)]
for blob in tracked_blobs:
    d=0
    for (a, b) in pairwise(tracked_blobs):
        c = a,b
        d +=1
        print('a = {}'.format(a))
        print('b = {}'.format(b))
        print(c)
        print('-------------')

#%%
import math
def calculate_speed (trails, fps):
    # distance: distance on the frame
	# location: x, y coordinates on the frame
	# fps: framerate
	# mmp: meter per pixel
#	dist = cv2.norm(trails[0], trails[10])
	dist_x = trails[0][0] - trails[10][0]
	dist_y = trails[0][1] - trails[10][1]

	mmp_y = 0.2 / (3 * (1 + (3.22 / 432)) * trails[0][1])
	mmp_x = 0.2 / (5 * (1 + (1.5 / 773)) * (width - trails[0][1]))
	real_dist = math.sqrt(dist_x * mmp_x * dist_x * mmp_x + dist_y * mmp_y * dist_y * mmp_y)

	return real_dist * fps * 250 / 3.6

width = 1920.0
trails = [(346, 203), (351, 223), (367, 244), (371, 267), (376, 285), 
          (378, 294), (380, 302), (383, 310), (384, 319), (387, 322), (390, 325)]
fps = 25.0
dist_x = trails[0][0] - trails[10][0]
dist_y = trails[0][1] - trails[10][1]
mmp_y = 0.2/(3 * (1 + (3.22 / 432)))
mmp_x = 0.2 / (5 * (1 + (1.5 / 773)) * (width - trails[0][1]))
real_dist = math.sqrt(dist_x * mmp_x * dist_x * mmp_x + dist_y * mmp_y * dist_y * mmp_y)

if True:
    pass
    mmp_x = 0.2 / (5 * (1 + (1.5 / 773)) * (width - trails[0][1]))

    
print(calculate_speed (trails, fps))

