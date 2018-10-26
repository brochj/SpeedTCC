# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:32:28 2018

@author: broch
"""
# ##############  FUNÇÕES ####################################################################


import numpy as np
import os
import itertools as it
#import math
import xml.etree.ElementTree as ET
import cv2
#from tccfunctions import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)
CIAN = (255, 255, 0)
PINK = (255, 0, 255)
ORANGE = (0, 90, 255)

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


def get_frame(cap, RESIZE_RATIO):
    #" Grabs a frame from the video vcture and resizes it. "
    ret, frame = cap.read()
    if ret:
        (h, w) = frame.shape[:2]
        frame = cv2.resize(frame, (int(w*RESIZE_RATIO), int(h*RESIZE_RATIO)), interpolation=cv2.INTER_CUBIC)
    return ret, frame


def pairwise(iterable):
    r"s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = it.tee(iterable)
    next(b, None)
    return zip(a, b)


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


# #### CSV FUNCTIONS ##########################################################
def remove_old_csv_files():
    for i in range(1, 4):
        if os.path.exists(f"results/mea_speed_lane{i}.csv"):
            os.remove(f"results/mea_speed_lane{i}.csv")
            print(f'Arquivo Deletado: "results/mea_speed_lane{i}.csv"')
        if os.path.exists(f"results/real_speed_lane{i}.csv"):
            os.remove(f"results/real_speed_lane{i}.csv")
            print(f'Arquivo Deletado: "results/real_speed_lane{i}.csv"')


def save_real_speed_in_csv(total_cars, dict_lane1, real_speed_lane1,
                           dict_lane2, real_speed_lane2, dict_lane3,
                           real_speed_lane3):
    for i in range(1, 4):
        if i == 1:
            dict_lane, real_speed_lane = dict_lane1, real_speed_lane1
        elif i == 2:
            dict_lane, real_speed_lane = dict_lane2, real_speed_lane2
        elif i == 3:
            dict_lane, real_speed_lane = dict_lane3, real_speed_lane3
        try:
            if dict_lane['speed'] == real_speed_lane[0]:
                pass
            else:
                real_speed_lane.insert(0, dict_lane['speed'])
                total_cars[f'lane_{i}'] += 1
                file = open(f'results/real_speed_lane{i}.csv', 'a')
                file.write('Carro {}, {} \n'.format(total_cars[f'lane_{i}'], dict_lane['speed']))
                file.close()
        except:
            pass


def save_mea_speed_in_csv(blob, total_cars, prev_len_speed, final_ave_speed,
                          lane,
                          dict_lane1, meas_speed_lane1,
                          dict_lane2, meas_speed_lane2,
                          dict_lane3, meas_speed_lane3):
    try:
        if float("{0:.3f}".format(final_ave_speed)) == meas_speed_lane1[0] or len(blob['speed']) >= 2:
            pass
        elif lane == 1 and prev_len_speed[0] == prev_len_speed[1] and final_ave_speed != 0:
            meas_speed_lane1.insert(0, float("{0:.3f}".format(final_ave_speed)))
            file = open('results/mea_speed_lane1.csv', 'a')
            file.write('Carro {}, {} \n'.format(total_cars['lane_1'], dict_lane1['speed']))
            file.close()
    except:
        pass

    try:
        if float("{0:.3f}".format(final_ave_speed)) == meas_speed_lane2[0] or len(blob['speed']) < 2:
            pass
        elif lane == 2 and prev_len_speed[0] == prev_len_speed[1] and final_ave_speed != 0:
            meas_speed_lane2.insert(0, float("{0:.3f}".format(final_ave_speed)))
            file = open('results/mea_speed_lane2.csv', 'a')
            file.write('Carro {}, {} \n'.format(total_cars['lane_2'], dict_lane2['speed']))
            file.close()
    except:
        pass

    try:
        if float("{0:.3f}".format(final_ave_speed)) == meas_speed_lane3[0] or len(blob['speed']) < 2:
            pass
        elif lane == 3 and prev_len_speed[0] == prev_len_speed[1] and final_ave_speed != 0:
            meas_speed_lane3.insert(0, float("{0:.3f}".format(final_ave_speed)))
            file = open('results/mea_speed_lane3.csv', 'a')
            file.write('Carro {}, {}, {} \n'.format(total_cars['lane_3'], dict_lane3['speed'], meas_speed_lane3[0]))
            file.close()
    except:
        pass
##### END - CSV FUNCTIONS ######################################################################

#### SPEED FUNCTIONS ########################################################################
def linearRegression(pts, frames):
    sqrs_x = []
    sqrs_y = []
    ms_xy = []
    x_values = []
    y_values = []
    for x, y in pts:
        sqr_x = x**2
        sqr_y = y**2
        m_xy = x*y

        x_values.append(x)
        y_values.append(y)

        ms_xy.append(m_xy)
        sqrs_x.append(sqr_x)
        sqrs_y.append(sqr_y)

        sum_x_values = sum(x_values)
        sum_y_values = sum(y_values)
        sum_ms_xy = sum(ms_xy)
        sum_sqrs_x = sum(sqrs_x)

        ave_x = sum_x_values/len(pts)
        ave_y = sum_y_values/len(pts)

    b = (sum_ms_xy - (len(pts)*ave_x*ave_y) )/(sum_sqrs_x - (len(pts)*(ave_x**2)))
    a = ave_y - b*ave_x

    predicted_final_y = a + b*x_values[0]
    predicted_initial_y = a + b*x_values[frames-1]

    final_pt = (x_values[0], int(predicted_final_y))
    initial_pt = (x_values[frames-1], int(predicted_initial_y))

    return initial_pt, final_pt
##### END - SPEED FUNTIONS #####################################################


def show_results_on_screen(frame, frameCount, ave_speed, lane, blob, total_cars, RESIZE_RATIO, VIDEO,
                 dict_lane1, dict_lane2, dict_lane3, SAVE_FRAME_F1, SAVE_FRAME_F2, SAVE_FRAME_F3):
    def r(numero):  # Faz o ajuste de escala das posições de textos e retangulos
        return int(numero*RESIZE_RATIO)
    color = WHITE
    if lane == 1:
        dict_lane = dict_lane1
        positions = [(r(350), r(120)), (r(550), r(120)), (r(550), r(180)), (r(550), r(230))]
    if lane == 2:
        dict_lane = dict_lane2
        positions = [(r(830), r(120)), (r(1030), r(120)), (r(1030), r(180)), (r(1030), r(230))]
    if lane == 3:
        dict_lane = dict_lane3
        positions = [(r(1350), r(120)), (r(1550), r(120)), (r(1550), r(180)), (r(1550), r(230))]

#    cv2.putText(frame, str(float("{0:.2f}".format(ave_speed))), (blob['trail'][0][0] + r(57), blob['trail'][0][1] + r(143)),
#                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, YELLOW, thickness=1, lineType=2)
    # Texto da que fica embaixo da velocidade real
    try:
        dif_lane = ave_speed - float(dict_lane['speed'])
        error_lane = (abs(ave_speed - float(dict_lane['speed']))/float(dict_lane['speed']))*100
    except:
        pass
    try:
        if abs(dif_lane) <= 3:
            color = GREEN
        elif abs(dif_lane) > 3 and abs(dif_lane) <= 5:
            color = YELLOW
        elif abs(dif_lane) > 5 and abs(dif_lane) <= 10:
            color = ORANGE
        elif abs(dif_lane) > 10:
            color = RED
            
        cv2.putText(frame, str(float("{0:.2f}".format(ave_speed))), positions[0],
                    2, .6, color, thickness=1, lineType=2)  # Velocidade Medida
        cv2.putText(frame, str(float("{0:.2f} ".format(dif_lane))), positions[1],
                    2, .6, color, thickness=1, lineType=2)  # erro absoluto
        cv2.putText(frame, str(float("{0:.2f}".format(error_lane)))+'%', positions[2],
                    2, .6, color, thickness=1, lineType=2)  # erro percentual
        cv2.putText(frame, 'Carro ' + str(total_cars['lane_{}'.format(lane)]), positions[3],
                    2, .6, color, thickness=1, lineType=2)
    except:
        pass
    
    if SAVE_FRAME_F1 and lane == 1:
        cv2.imwrite('img/novo/{}-{}_F1_Carro_{}.png'.format(VIDEO, frameCount, total_cars['lane_{}'.format(lane)]), frame)
    if SAVE_FRAME_F2 and lane == 2:
        cv2.imwrite('img/novo/{}-{}_F2_Carro_{}.png'.format(VIDEO, frameCount, total_cars['lane_{}'.format(lane)]), frame)
    if SAVE_FRAME_F3 and lane == 3:
        cv2.imwrite('img/novo/{}-{}_F3_Carro_{}.png'.format(VIDEO, frameCount, total_cars['lane_{}'.format(lane)]), frame)

    # PRINTA FAIXA 2
#    cv2.putText(frame, 'Faixa {}'.format(lane), (blob['trail'][0][0] - r(29), blob['trail'][0][1] + r(200)),
#                cv2.FONT_HERSHEY_COMPLEX_SMALL, .8, WHITE, thickness=1, lineType=2)

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
    file_name = xml_file[xml_file.rfind('/')+1:]
    print('Arquivo "{}" foi armazenado com sucesso !!'.format(file_name))
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

def skip_video(frameCount, video, frame):
    skip = False
    if video == 1:
        if frameCount < 49: skip = True
        if frameCount > 90 and frameCount < 96: skip = True
        if frameCount > 130 and frameCount < 176: skip = True
        if frameCount > 212 and frameCount < 235: skip = True
        if frameCount > 336 and frameCount < 361: skip = True
        if frameCount > 460 and frameCount < 467: skip = True
        if frameCount > 499 and frameCount < 563: skip = True
        if frameCount > 598 and frameCount < 614: skip = True
        if frameCount > 644 and frameCount < 696: skip = True
        if frameCount > 731 and frameCount < 739: skip = True
        if frameCount > 781 and frameCount < 794: skip = True
        if frameCount > 829 and frameCount < 857: skip = True
        if frameCount > 894 and frameCount < 925: skip = True
        if frameCount > 958 and frameCount < 1054: skip = True
        if frameCount > 1053 and frameCount < 1101: skip = True  # Caminhão
        if frameCount > 1100 and frameCount < 1140: skip = True
        if frameCount > 1139 and frameCount < 1199: skip = True  # Carro parado
    
        
        
        
#        if frameCount < 1200: skip = True
    return skip


#def calculate_speed (trails, fps):
#    # distance: distance on the frame
#    # location: x, y coordinates on the frame
#    # fps: framerate
#    # mmp: meter per pixel
##    dist = cv2.norm(trails[0], trails[10])
#    dist_x = trails[0][0] - trails[10][0]
#    dist_y = trails[0][1] - trails[10][1]
#
#    mmp_y = 0.125 / (3 * (1 + (3.22 / 432)) * trails[0][1])
##    mmp_y = 0.2 / (3 * (1 + (3.22 / 432)) * trails[0][1])  # Default
#    mmp_x = 0.125 / (5 * (1 + (1.5 / 773)) * (WIDTH - trails[0][1]))
##    mmp_x = 0.2 / (5 * (1 + (1.5 / 773)) * (width - trails[0][1]))  # Default
#    real_dist = math.sqrt(dist_x * mmp_x * dist_x * mmp_x + dist_y * mmp_y * dist_y * mmp_y)
#
#    return real_dist * fps * 250 / 3.6

# ########## FIM  FUNÇÕES ####################################################################
