# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 18:31:55 2018

@author: broch
"""
import os
import cv2
import numpy as np


PATH_VALOR_NOVO = 'img/novo'
PATH_VALOR_VELHO = 'img/velho'
PATH_OUT = 'img/comparacao/'

new_values = os.listdir(PATH_VALOR_NOVO)
old_values = os.listdir(PATH_VALOR_VELHO)
a = []
b = []

array = []
for i in range(len(new_values)):
    frame_a = int(new_values[i][new_values[i].find('-')+1:new_values[i].find('_')])
    frame_b = int(old_values[i][old_values[i].find('-')+1:old_values[i].find('_')])
    a.append((frame_a, new_values[i]))
    b.append((frame_b, old_values[i]))
    array.append((old_values[i], new_values[i]))
a.sort()
b.sort()

frameCount = int(old_values[0][old_values[0].find('-')+1:old_values[0].find('_')])
def abc(ele):
    ele = ele[0][ele[0].find('-')+1:ele[0].find('_')]
    return ele

for new_img, old_img in array:
    if new_img == old_img:
        file_name = new_img[:new_img.find('.')]
        new_image = cv2.imread(f'{PATH_VALOR_NOVO}/{new_img}')
        old_image = cv2.imread(f'{PATH_VALOR_VELHO}/{old_img}')

        cv2.putText(new_image, 'New values', (20, 20), 2, .6, (255, 255, 255), 1)
        cv2.putText(old_image, 'Old values', (20, 20), 2, .6, (255, 255, 255), 1)

        frame = np.vstack((old_image, new_image))

        cv2.imwrite(f'{PATH_OUT}{file_name}_result.png', frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # tecla Q para fechar o video
            break
cv2.destroyAllWindows()
