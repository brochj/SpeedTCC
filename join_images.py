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
PATH_OUT = 'img/'

NEW_VALUES = os.listdir(PATH_VALOR_NOVO)
OLD_VALUES = os.listdir(PATH_VALOR_VELHO)
array = []
for i in range(len(NEW_VALUES)):
    array.append((OLD_VALUES[i], NEW_VALUES[i]))


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
