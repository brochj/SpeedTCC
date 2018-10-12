# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:32:28 2018

@author: broch
"""
# ##############  FUNÇÕES ####################################################################

import cv2
import numpy as np
#import math
import xml.etree.ElementTree as ET
#from tccfunctions import *


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
        
                    
def get_frame(cap,RESIZE_RATIO):
	#" Grabs a frame from the video vcture and resizes it. "
	ret, frame = cap.read()
	if ret:
		(h, w) = frame.shape[:2]
		frame = cv2.resize(frame, (int(w * RESIZE_RATIO), int(h * RESIZE_RATIO)), interpolation=cv2.INTER_CUBIC)
	return ret, frame


from itertools import *
def pairwise(iterable):
    r"s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

##### XML FUNCTIONS ###########################################################
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


def update_info_xml(frameCount, vehicle, dict_lane1, dict_lane2, dict_lane3):
    try:
        # Verifica se naquele frame tem uma chave correspondente no dicionário "vehicle"
        if vehicle[str(frameCount)]['frame_start'] == str(frameCount):  
            lane_state = vehicle[str(frameCount)]['lane']
            
            if lane_state == '1':  # Se for na faixa 1, armazena as seguintes infos
                # print('Faixa 1')
                dict_lane1['speed'] = vehicle[str(frameCount)]['speed']
                dict_lane1['frame_start'] = vehicle[str(frameCount)]['frame_start']
                dict_lane1['frame_end'] = vehicle[str(frameCount)]['frame_end']
            elif lane_state == '2':
                #print('Faixa 2')
                dict_lane2['speed'] = vehicle[str(frameCount)]['speed']
                dict_lane2['frame_start'] = vehicle[str(frameCount)]['frame_start']
                dict_lane2['frame_end'] = vehicle[str(frameCount)]['frame_end']
            elif lane_state == '3':
                #print('Faixa 3')
                dict_lane3['speed'] = vehicle[str(frameCount)]['speed']
                dict_lane3['frame_start'] = vehicle[str(frameCount)]['frame_start']
                dict_lane3['frame_end'] = vehicle[str(frameCount)]['frame_end']
    except KeyError:
#            print('KeyError: Key Não encotrada no dicionário')
        pass
    


def print_xml_values(frame, ratio, dict_lane1, dict_lane2, dict_lane3):
    def r(numero):  # Faz o ajuste de escala das posições de textos e retangulos
        return int(numero*ratio)
    # Mostra no video os valores das velocidades das 3 Faixas.
    try:  # Posição do texto da FAIXA 1
        text_pos = (r(143), r(43))
        cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20), (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
        cv2.putText(frame, 'speed: {}'.format(dict_lane1['speed']), text_pos, 2, .6, (255, 255, 0), 1)
    except:
        pass
    
    try:  # Posição do texto da FAIXA 2
        text_pos = (r(628), r(43))
        cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20), (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
        cv2.putText(frame, 'speed: {}'.format(str(dict_lane2['speed'])), text_pos, 2, .6, (255, 255, 0), 1)
    except:
        pass
    
    try:  # Posição do texto da FAIXA 3
        text_pos = (r(1143), r(43))
        cv2.rectangle(frame, (text_pos[0] - 10, text_pos[1] - 20), (text_pos[0] + 135, text_pos[1] + 10), (0, 0, 0), -1)
        cv2.putText(frame, 'speed: {}'.format(dict_lane3['speed']), text_pos, 2, .6, (255, 255, 0), 1)
    except:
        pass

##### END --- XML FUNCTIONS ###################################################

# ########## FIM  FUNÇÕES ####################################################################