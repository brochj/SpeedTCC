# -*- coding: utf-8 -*-
import cv2
# Create a VideoCapture object
cap = cv2.VideoCapture('../../Dataset/video1.avi')
 
FPS = 25
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Retorna a largura do video
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Retorna a largura do video
frameCount = 0
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('out.avi',cv2.VideoWriter_fourcc('M','J','P','G'), FPS, (WIDTH,HEIGHT))
 
while(True):
  ret, frame = cap.read()
  if ret == True: 
  
    # Write the frame into the file 'output.avi'
    if frameCount > 2000 and frameCount < 4000:
        cv2.putText(frame, 'frame: {}'.format(frameCount),(14, 25), 0, 1, (255,255,255), 2)
        out.write(frame)  # Salva o Frame
        
    #if frameCount > 500 and frameCount < 600:
        
       #cv2.putText(frame, 'frame: {}'.format(frameCount),(14, 25), 0, 1, (255,255,255), 2)
       # out.write(frame) # Salva o Frame
    
    
    
    cv2.putText(frame, 'frame: {}'.format(frameCount),(14, 25), 0, 1, (255,255,255), 2)
    # Display the resulting frame    
    cv2.imshow('frame',frame)
        
    frameCount += 1
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break 
  # Break the loop
  else:
    break 
 
cap.release()
out.release()
cv2.destroyAllWindows() 
