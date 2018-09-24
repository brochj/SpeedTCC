import os
import cv2
# import numpy as np

#

for file_type in ['positive_images']:  # Colocar o nome da pasta aqui: positives ou negatives

    for img in os.listdir(file_type):

        if file_type == 'negatives':
            image = cv2.imread(file_type + '/' + img)
            h, w = image.shape[:2]

            line = './' + file_type + '/' + img + '\n'
            print(line)
            with open('negatives.txt', 'a') as f:
                f.write(line)
        elif file_type == 'positive_images':
            image = cv2.imread(file_type + '/' + img)
            h, w = image.shape[:2]
            # Só pra evitar de pegar a imagem inteira, fiz os cmds abaixo
            numberOfObjects = 1
            x = 1
            y = 1
            h1 = h-1
            w1 = w-1

            line = img + ' {} {} {} {} {}'.format(numberOfObjects, x, y, w1, h1) + '\n'
            print(line)
            with open('positives.txt', 'a') as f:
                f.write(line)
