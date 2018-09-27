#!/usr/bin/env python

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2


RESIZE_RATIO = 0.40
frameCount = 0


def get_frame():
	" Grabs a frame from the video vcture and resizes it. "
	ret, frame = cap.read()
	if ret:
		(h, w) = frame.shape[:2]
		frame = cv2.resize(frame, (int(w * RESIZE_RATIO), int(h * RESIZE_RATIO)), interpolation=cv2.INTER_CUBIC)
	return ret, frame


if __name__ == '__main__':
    import sys, getopt
    print(__doc__)

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade='])
    try:
        video_src = '../../video01.avi'#video_src[0]
    except:
        print("No video source supplied.")
        exit()
    args = dict(args)
    cascade_fn = args.get('--cascade', "cascade_dir/cascade.xml")

    car_cascade = cv2.CascadeClassifier(cascade_fn)
    cap = cv2.VideoCapture('../../../Dataset/video1.avi')
#    cap = cv2.VideoCapture(0)  # WebCam

    
    
    paused = False
    step = True

    while True:
        if not paused or step:
            flag, img = get_frame()
            #if img == None: break

            height, width, c = img.shape
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # cars = car_cascade.detectMultiScale(gray, 1.5, 10) # Default
            cars = car_cascade.detectMultiScale(img, 1.5, 10)


            for (x,y,w,h) in cars:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
#                crop_img = img[y:y+h , x:x+w]
#                cv2.imwrite('positives/cars{}.jpg'.format(frameCount),crop_img)
#            else:
#                cv2.imwrite('negatives/cars{}.jpg'.format(frameCount),img)
            outputFrame = cv2.putText(img, 'frame: {}'.format(frameCount), (5, 375), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)


            if frameCount == 3000:  # fecha o video
                break


            cv2.imshow('edge', img)
            
            
            frameCount += 1
            
        step = False
        ch = cv2.waitKey(5)
        if ch == 13:
            step = True
        if ch == 32:
            paused = not paused
        if ch == 27:
            break
    cv2.destroyAllWindows()