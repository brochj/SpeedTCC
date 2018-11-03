# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 19:51:26 2018

@author: broch
"""
import numpy as np
import cv2

BLACK = (0,0,0)
def region_of_interest(frame, resize_ratio):
    def r(numero):  # Faz o ajuste de escala
        return int(numero*resize_ratio)
    # Retângulo superior
    cv2.rectangle(frame, (0, 0), (r(1920), r(120)), BLACK, -1)
    # triângulo lado direito
    pts = np.array([[r(1920), r(750)], [r(1320), 0], [r(1920), 0]], np.int32)
    cv2.fillPoly(frame, [pts], BLACK)
    # triângulo lado esquerdo
    pts3 = np.array([[0, r(620)], [r(270), 0], [0, 0]], np.int32)
    cv2.fillPoly(frame, [pts3], BLACK)
    # Linha entre faixas 1 e 2
    pts1 = np.array([[r(480), r(1080)], [r(560), r(0)],
                     [r(640), r(0)], [r(570), r(1080)]], np.int32)
    cv2.fillPoly(frame, [pts1], BLACK)
    # Linha entre faixas 2 e 3
    pts7 = np.array([[r(1310), r(1080)], [r(900), r(0)],
                     [r(990), r(0)], [r(1410), r(1080)]], np.int32)
    cv2.fillPoly(frame, [pts7], BLACK)
    return frame

img = cv2.imread('img.png')
height = img.shape[0]
width = img.shape[1]

mask = np.zeros((height, width), dtype=np.uint8)

#points = region_of_interest(mask, 0.7697)
points = np.array([[[10,150],[330,100],[310,20],[35,10]]])

cv2.fillPoly(mask, points, (255))

res = cv2.bitwise_and(img,img,mask = mask)

rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]

pt4 = [0,0]
pt3 = [300, 0]
pt2 = [300,70]
pt1 = [0,70]

target_pts = np.array([pt1,pt2,pt3,pt4 ], np.float32)
H, mask = cv2.findHomography(points, target_pts, cv2.RANSAC)

# size target image
hei , wid, _ = cropped.shape
im1Reg = cv2.warpPerspective(cropped, H, (wid+20, hei+20))
#img2 = cv2.perspectiveTransform(np.array([[[cropped.shape[1],cropped.shape[0]]]]), h)

cv2.imshow("im1Reg" , im1Reg )
cv2.imshow("cropped" , cropped )
#cv2.imshow("same size" , res)

cv2.waitKey(0)
#if cv2.waitKey(1) & 0xFF == ord('q'):
cv2.destroyAllWindows()

#%%
#import cv2
#import numpy as np
#def _estimate_homography(image_points, ideal_points):
#        """Find homography matrix.
#        """
#        fp = np.array(image_points)
#        tp = np.array(ideal_points)
#        H, _ = cv2.findHomography(fp, tp, 0)
#        return H 
#%%
#from __future__ import print_function
#import cv2
#import numpy as np
# 
# 
#MAX_FEATURES = 500
#GOOD_MATCH_PERCENT = 0.15
# 
# 
#def alignImages(im1, im2):
# 
#  # Convert images to grayscale
#  im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
#  im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
#   
#  # Detect ORB features and compute descriptors.
#  orb = cv2.ORB_create(MAX_FEATURES)
#  keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
#  keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
#   
#  # Match features.
#  matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
#  matches = matcher.match(descriptors1, descriptors2, None)
#   
#  # Sort matches by score
#  matches.sort(key=lambda x: x.distance, reverse=False)
# 
#  # Remove not so good matches
#  numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
#  matches = matches[:numGoodMatches]
# 
#  # Draw top matches
#  imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
#  cv2.imwrite("matches.jpg", imMatches)
#   
#  # Extract location of good matches
#  points1 = np.zeros((len(matches), 2), dtype=np.float32)
#  points2 = np.zeros((len(matches), 2), dtype=np.float32)
# 
#  for i, match in enumerate(matches):
#    points1[i, :] = keypoints1[match.queryIdx].pt
#    points2[i, :] = keypoints2[match.trainIdx].pt
#   
#  # Find homography
#  h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
# 
#  # Use homography
#  height, width, channels = im2.shape
#  im1Reg = cv2.warpPerspective(im1, h, (width, height))
#   
#  return im1Reg, h
# 
# 
#if __name__ == '__main__':
#   
#  # Read reference image
#  refFilename = "img.png"
#  print("Reading reference image : ", refFilename)
#  imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)
# 
#  # Read image to be aligned
#  imFilename = "img.png"
#  print("Reading image to align : ", imFilename);  
#  im = cv2.imread(imFilename, cv2.IMREAD_COLOR)
#   
#  print("Aligning images ...")
#  # Registered image will be resotred in imReg. 
#  # The estimated homography will be stored in h. 
#  imReg, h = alignImages(im, imReference)
#   
#  # Write aligned image to disk. 
#  outFilename = "aligned.jpg"
#  print("Saving aligned image : ", outFilename); 
#  cv2.imwrite(outFilename, imReg)
# 
#  # Print estimated homography
#  print("Estimated homography : \n",  h)