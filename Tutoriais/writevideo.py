# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:44:06 2018

@author: broch
"""

import cv2
 
# Create a VideoCapture object
cap = cv2.VideoCapture('../Dataset/video1.avi')
 

frame_width = 1920
frame_height = 1080
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('out.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 25, (frame_width,frame_height))
 
frameCount = 0
while(True):
  ret, frame = cap.read()
 
  if ret == True: 
     
    # Write the frame into the file 'output.avi'
    if frameCount > 100 and frameCount < 200:
        cv2.putText(frame, 'frame: {}'.format(frameCount),(14, 20), 0, .65, (255,255,255), 2)
        out.write(frame)
        
    if frameCount > 500 and frameCount < 600:
        cv2.putText(frame, 'frame: {}'.format(frameCount),(14, 20), 0, .65, (255,255,255), 2)
        out.write(frame)
    
#    cv2.putText(frame, 'frame: {}'.format(frameCount),(14, 20), 0, .65, (255,255,255), 2)
    # Display the resulting frame    
    cv2.imshow('frame',frame)
        
    frameCount += 1
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else:
    break 
 
# When everything done, release the video capture and video write objects
cap.release()
out.release()
 
# Closes all the frames
cv2.destroyAllWindows() 