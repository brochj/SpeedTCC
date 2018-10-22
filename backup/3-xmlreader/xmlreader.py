# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 21:03:24 2018

@author: broch
"""

import cv2
#import numpy as np
#import os
#import time
#import uuid
#import math
#import xml.dom
import xml.etree.ElementTree as ET


# Constant Values
VIDEO_FILE = '../../Dataset/video1.avi' # Local do video a ser analisado
XML_FILE = 'video1.xml'
RESIZE_RATIO = 0.70  # Resize, valores entre 0 e 1 | 1=Tamanho original do video
CLOSE_VIDEO = 600  # Fecha o video no frame 400

# Variant Values
frameCount = 0  # Armazena a contagem de frames processados do video
dict_lane1 = {}  # Buffer que armazena os valores de "speed, frame_start, frame_end" da FAIXA 1
dict_lane2 = {}  # Buffer que armazena os valores de "speed, frame_start, frame_end" da FAIXA 2
dict_lane3 = {}  # Buffer que armazena os valores de "speed, frame_start, frame_end" da FAIXA 3


def get_frame():  # Capta o frame do video e da um resize no frame
    ret, frame = cap.read()
    if ret:
        (h, w) = frame.shape[:2]
        frame = cv2.resize(frame, (int(w*RESIZE_RATIO), int(h*RESIZE_RATIO)), interpolation=cv2.INTER_CUBIC)
    return ret, frame


def read_xml(xml_file):
# Funcão que lê o .xml e guarda as informações em um dicionário "iframe"
    tree = ET.parse(xml_file)
    root = tree.getroot()
    iframe = {}
    for child in root:
        if child.get('radar') == 'True':
            for subchild in child:
#                print('subchild {}'.format(subchild.attrib))                
                if subchild.tag == 'radar':
                    iframe[child.get('iframe')] = subchild.attrib # salva frame_end, frame_start, speed
                    iframe[child.get('iframe')]['lane'] = child.get('lane')
                    iframe[child.get('iframe')]['radar'] = child.get('radar')
                    iframe[child.get('iframe')]['moto'] = child.get('moto')
#                    iframe[child.get('iframe')]['plate'] = child.get('plate')  # Desnecessário
#                    iframe[child.get('iframe')]['sema'] = child.get('sema')  # Desnecessário
        if child.tag == 'videoframes':
            iframe[child.tag] = int(child.get('total'))
    print('Arquivo {} foi armazenado com sucesso !!'.format(xml_file))
    return iframe


def res(numero):  # Faz o ajuste de escala das posições de textos e retangulos
    return int(numero*RESIZE_RATIO)


 # ##############################################################################
cap = cv2.VideoCapture(VIDEO_FILE)
vehicle = read_xml(XML_FILE)  # Dicionário que armazena todas as informações do xml

while True:
    ret, frame = get_frame()

    if ret:
        # Coloca o codigo Principal AQUI
        try:
            # Verifica se naquele frame tem uma chave correspondente no dict vehicle
            if vehicle[str(frameCount)]['frame_start'] == str(frameCount):  # Verifica se naquele frame tem uma chave correspondente no dict vehicle
                lane_state = vehicle[str(frameCount)]['lane']
                
                if lane_state == '1':  # Se for na faixa 1, armazena as seguintes infos
#                    print('Faixa 1')
                    dict_lane1['speed'] = vehicle[str(frameCount)]['speed']
                    dict_lane1['frame_start'] = vehicle[str(frameCount)]['frame_start']
                    dict_lane1['frame_end'] = vehicle[str(frameCount)]['frame_end']
                elif lane_state == '2':
#                    print('Faixa 2')
                    dict_lane2['speed'] = vehicle[str(frameCount)]['speed']
                    dict_lane2['frame_start'] = vehicle[str(frameCount)]['frame_start']
                    dict_lane2['frame_end'] = vehicle[str(frameCount)]['frame_end']
                elif lane_state == '3':
#                    print('Faixa 3')
                    dict_lane3['speed'] = vehicle[str(frameCount)]['speed']
                    dict_lane3['frame_start'] = vehicle[str(frameCount)]['frame_start']
                    dict_lane3['frame_end'] = vehicle[str(frameCount)]['frame_end']
        except KeyError:
#            print('KeyError: Key Não encotrada no dicionário')
            pass
        
        # Escreve o frame atual e a porcentagem do video
        cv2.putText(frame, 'frame: {} {}%'.format(frameCount, str(int((100*frameCount)/vehicle['videoframes']))), (res(14), res(1071)), 0, .65, (255, 255, 255), 1)

        try:  # Posição do texto da FAIXA 1
            text_pos = (res(143), res(43))
            cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20), (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
            cv2.putText(frame, 'speed: {}'.format(dict_lane1['speed']), text_pos, 2, .6, (255, 255, 0), 1)
        except:
            pass
        
        try:  # Posição do texto da FAIXA 2
            text_pos = (res(628), res(43))
            cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20), (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
            cv2.putText(frame, 'speed: {}'.format(str(dict_lane2['speed'])), text_pos, 2, .6, (255, 255, 0), 1)
        except:
            pass
        
        try:  # Posição do texto da FAIXA 3
            text_pos = (res(1143), res(43))
            cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20), (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
            cv2.putText(frame, 'speed: {}'.format(dict_lane3['speed']), text_pos, 2, .6, (255, 255, 0), 1)
        except:
            pass

        if frameCount == CLOSE_VIDEO: #  fecha o video
            break

        cv2.imshow('frame', frame)
        frameCount += 1  # Conta a quantidade de Frames processados

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Pressiona a tecla Q para fechar o video
            break

cap.release()
cv2.destroyAllWindows()
