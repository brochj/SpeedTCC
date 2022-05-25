# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:32:28 2018

@author: broch
"""
# ##############  FUNÇÕES ####################################################################


import numpy as np
#import os
import itertools as it
#import math
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
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
#    cv2.rectangle(frame, (0, 0), (r(1920), r(120)), BLACK, -1)
    # triângulo lado direito
#    pts = np.array([[r(1920), r(750)], [r(1320), 0], [r(1920), 0]], np.int32)
#    cv2.fillPoly(frame, [pts], BLACK)
    pts = np.array([[r(1920), r(790)], [r(1290), 0], [r(1920), 0]], np.int32)
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
    # Faixa 3
#    pts8 = np.array([[r(1410), r(1080)], [r(990), r(0)],
#                      [r(1320), r(0)], [r(1920), r(750)], [r(1920), r(1080)]], np.int32)
#    cv2.fillPoly(frame, [pts8], RED)
    # Faixa 2
#    pts9 = np.array([[r(570), r(1080)], [r(640), r(0)],
#                     [r(900), r(0)], [r(1310), r(1080)]], np.int32)
#    cv2.fillPoly(frame, [pts9], GREEN)
    # Faixa 1
#    pts10 = np.array([[r(480), r(1080)], [r(560), r(0)],
#                       [r(270), 0], [0, r(620)], [0, 1080]], np.int32)
    # faixa 1 - 4 pontos
#    points = np.array([[[r(-150), r(1080)], [r(480), r(1080)],
#                       [r(560), r(0)], [r(270), 0] ]], np.int32) = np.array([[[r(-150), r(1080)], [r(480), r(1080)],
#                       [r(560), r(0)], [r(270), 0] ]], np.int32)
#    cv2.fillPoly(frame, [pts10], BLUE)
    
    return frame



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
def read_xml(xml_file, video, DATE):
# Funcão que lê o .xml e guarda as informações em um dicionário "iframe"
    tree = ET.parse(xml_file)
    root = tree.getroot()
    iframe = {}
    lane1_count = 0
    lane2_count = 0
    lane3_count = 0
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
                    speed = iframe[child.get('iframe')]['speed']
                    frame_start = iframe[child.get('iframe')]['frame_start']
                    frame_end = iframe[child.get('iframe')]['frame_end']
                    
                    if child.get('lane') == '1':
                        lane1_count += 1
                    if child.get('lane') == '2':
                        lane2_count += 1
                    if child.get('lane') == '3':
                        lane3_count += 1
                    
                    
                    if iframe[child.get('iframe')]['lane'] == '1':
                        file = open(f'results/{DATE}/planilhas/video{video}_real_lane1.csv', 'a')
                        file.write(f'frame_start, {frame_start}, frame_end, {frame_end}, speed, {speed} \n')
                        file.close()
                    if iframe[child.get('iframe')]['lane'] == '2':
                        file = open(f'results/{DATE}/planilhas/video{video}_real_lane2.csv', 'a')
                        file.write(f'frame_start, {frame_start}, frame_end, {frame_end}, speed, {speed} \n')
                        file.close()
                    if iframe[child.get('iframe')]['lane'] == '3':
                        file = open(f'results/{DATE}/planilhas/video{video}_real_lane3.csv', 'a')
                        file.write(f'frame_start, {frame_start}, frame_end, {frame_end}, speed, {speed} \n')
                        file.close()
        if child.tag == 'videoframes':
            iframe[child.tag] = int(child.get('total'))
    
    iframe['total_cars_lane1'] = lane1_count
    iframe['total_cars_lane2'] = lane2_count
    iframe['total_cars_lane3'] = lane3_count
        
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

    return
##### END --- XML FUNCTIONS ###################################################

def skip_video(frameCount, video, frame):
    skip = False
    if video == 1:
        if frameCount < 49: skip = True
        if frameCount > 90 and frameCount < 96: skip = True
        if frameCount > 130 and frameCount < 176: skip = True
        if frameCount > 212 and frameCount < 235: skip = True
        if frameCount > 336 and frameCount < 361: skip = True
        if frameCount > 394 and frameCount < 425: skip = True  # Caminhão
        if frameCount > 460 and frameCount < 467: skip = True
        if frameCount > 499 and frameCount < 563: skip = True
        if frameCount > 598 and frameCount < 614: skip = True
        if frameCount > 644 and frameCount < 696: skip = True
        if frameCount > 731 and frameCount < 739: skip = True
        if frameCount > 781 and frameCount < 794: skip = True
        if frameCount > 829 and frameCount < 857: skip = True
        if frameCount > 856 and frameCount < 895: skip = True # carro preto F3, da pra por (tava com erro altissimo)       
        if frameCount > 894 and frameCount < 925: skip = True
        if frameCount > 958 and frameCount < 1054: skip = True
        if frameCount > 1053 and frameCount < 1101: skip = True  # Caminhão
        if frameCount > 1100 and frameCount < 1140: skip = True
        if frameCount > 1139 and frameCount < 1199: skip = True  # Carro parado
        if frameCount > 1198 and frameCount < 2650: skip = True  # Carro baixa velocidade
        if frameCount > 2689 and frameCount < 2715: skip = True
        if frameCount > 2850 and frameCount < 2870: skip = True
#        if frameCount > 3035 and frameCount < 3045: skip = True # carro taxi
#        if frameCount > 3230 and frameCount < 3242: skip = True
#        if frameCount > 3100 and frameCount < 3115: skip = True
#        if frameCount > 2979 and frameCount < 3018: skip = True
#        if frameCount > 3030 and frameCount < 3050: skip = True
#        if frameCount > 3060 and frameCount < 3090: skip = True
#        if frameCount > 3122 and frameCount < 3166: skip = True
#        if frameCount > 3279 and frameCount < 3328: skip = True
#        if frameCount > 3404 and frameCount < 3459: skip = True
        if frameCount > 3550 and frameCount < 4800: skip = True
#        if frameCount > 5270 and frameCount < 5285: skip = True
#        if frameCount > 5375 and frameCount < 5390: skip = True
#        if frameCount > 5525 and frameCount < 5540: skip = True
#        if frameCount > 5738 and frameCount < 5753: skip = True
#        if frameCount > 5615 and frameCount < 5630: skip = True
        if frameCount > 5322 and frameCount < 5352: skip = True
        if frameCount > 5401 and frameCount < 5507: skip = True # caminhao
        if frameCount > 5554 and frameCount < 5604: skip = True # van no meio da faixa
        if frameCount > 5667 and frameCount < 5698: skip = True
        if frameCount > 5785 and frameCount < 5902: skip = True
        if frameCount > 5934 and frameCount < 6918: skip = True # Carro parado           
    return skip


def write_results_on_image(frame, frameCount, ave_speed, lane, id_car, RESIZE_RATIO, VIDEO,
                        dict_lane1, dict_lane2, dict_lane3):
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
        
    abs_error = 0.0
    per_error = 0.0
    try:
        abs_error = ave_speed - float(dict_lane['speed'])
        per_error = (abs(ave_speed - float(dict_lane['speed']))/float(dict_lane['speed']))*100
    except:
        pass
    try:
        if abs(abs_error) <= 3:
            color = GREEN
        elif abs(abs_error) > 3 and abs(abs_error) <= 5:
            color = YELLOW
        elif abs(abs_error) > 5 and abs(abs_error) <= 10:
            color = ORANGE
        elif abs(abs_error) > 10:
            color = RED
            
        cv2.putText(frame, str(float("{0:.2f}".format(ave_speed))), positions[0],
                    2, .6, color, thickness=1, lineType=2)  # Velocidade Medida
        cv2.putText(frame, str(float("{0:.2f} ".format(abs_error))), positions[1],
                    2, .6, color, thickness=1, lineType=2)  # erro absoluto
        cv2.putText(frame, str(float("{0:.2f}".format(per_error)))+'%', positions[2],
                    2, .6, color, thickness=1, lineType=2)  # erro percentual
        cv2.putText(frame, f'id: {id_car}', positions[3],
                    2, .6, color, thickness=1, lineType=2)
    except:
        pass
    
    return abs_error, per_error

def print_trail(trail, frame):
    for (a, b) in pairwise(trail):
#        cv2.circle(frame, a, 3, BLUE, -1)
#        cv2.line(frame, a, b, WHITE, 1)
        cv2.line(frame, a, b, GREEN, 3)
        cv2.circle(frame, a, 5, RED, -1)
        

def plot_graph(abs_error_list, ave_abs_error, ave_per_error, rate_detec_lane, 
               real_total_lane, total_cars_lane, DATE, lane, VIDEO, cf, SHOW_LIN,
               list_3km, list_5km, list_maior5km):
    
        
    plt.figure(lane, figsize=[9,7])
    plt.plot(abs_error_list, 'o-')
    
    plt.plot([0, len(abs_error_list) + 3], [0, 0], color='k', linestyle='-', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [3, 3], color='k', linestyle=':', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [-3, -3], color='k', linestyle=':', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [5, 5], color='k', linestyle='--', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [-5, -5], color='k', linestyle='--', linewidth=1)
    
    if lane == 'total':
        titulo = 'Resultado Total'
    else:
        titulo = f'Resultados da Faixa {lane}'
    plt.xlabel('Medições')
    plt.ylabel('Erro Absoluto (km/h)')
    plt.title(f'{titulo} - Video {VIDEO} \n\n'
              f'Média dos erros absolutos =  {ave_abs_error} km/h\n'
              f'Média dos erros percentuais = {ave_per_error} % \n'
              f' Qtnd de erros até 3km/h: {len(list_3km)} de {real_total_lane} ({round(len(list_3km)/real_total_lane*100, 2)} %)\n'
              f' Qtnd de erros até 5km/h: {len(list_5km)} de {real_total_lane} ({round(len(list_5km)/real_total_lane*100, 2)} %)\n'
              f' Qtnd de erros > 5km/h: {len(list_maior5km)} de {real_total_lane} ({round(len(list_maior5km)/real_total_lane*100, 2)} %)\n'
              f'Taxa de Detecção: {rate_detec_lane} % \n'
              f'Carros detectados: {total_cars_lane} de {real_total_lane} \n'
              f'Fator de correção: {cf}')
    plt.xlim(0, len(abs_error_list) + 3)
    plt.grid(False)
            
    plt.savefig(f'results/{DATE}/graficos/result_{DATE}_F{lane}.png', bbox_inches='tight', pad_inches=0.3)
    plt.savefig(f'results/{DATE}/graficos/pdfs/result_{DATE}_F{lane}.pdf', bbox_inches='tight', pad_inches=0.3)
    plt.show()
    
    if SHOW_LIN:
        plt.figure('Total', figsize=[9,7])
        abs_list = []
        for value in abs_error_list:
            abs_list.append(abs(value))
        
        font = {'size'   : 16}
        plt.rc('font', **font)
        
        plt.xlabel('Medições')
        plt.ylabel('Erro Absoluto (km/h)')
#        plt.title(f'{titulo} - Video {VIDEO} \n\n'
#              f'Média dos erros absolutos =  {ave_abs_error} km/h\n'
#              f'Média dos erros percentuais = {ave_per_error} % \n'
#              f' Qtnd de erros até 3km/h: {len(list_3km)} de {real_total_lane} ({round(len(list_3km)/real_total_lane*100, 2)} %)\n'
#              f' Qtnd de erros até 5km/h: {len(list_5km)} de {real_total_lane} ({round(len(list_5km)/real_total_lane*100, 2)} %)\n'
#              f' Qtnd de erros > 5km/h: {len(list_maior5km)} de {real_total_lane} ({round(len(list_maior5km)/real_total_lane*100, 2)} %)\n'
#              f'Taxa de Detecção: {rate_detec_lane} % \n'
#              f'Carros detectados: {total_cars_lane} de {real_total_lane} \n'
#              f'Fator de correção: {cf}')
        
        plt.plot([0, len(abs_error_list) + 3], [0, 0], color='k', linestyle='-', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [3, 3], color='k', linestyle=':', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [-3, -3], color='k', linestyle=':', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [5, 5], color='k', linestyle='--', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [-5, -5], color='k', linestyle='--', linewidth=1)
        
        plt.plot(abs_error_list, 'ro-')
        plt.savefig(f'results/{DATE}/graficos/result_{DATE}_F{lane}_lin.png', bbox_inches='tight', pad_inches=0.3)
        plt.savefig(f'results/{DATE}/graficos/pdfs/result_{DATE}_F{lane}_lin.pdf', bbox_inches='tight', pad_inches=0.3)
    
#    if SHOW_LIN:
#        plt.figure('Total', figsize=[9,7])
#        abs_list = []
#        for value in abs_error_list:
#            abs_list.append(abs(value))
#        
#        plt.xlabel('Medições')
#        plt.ylabel('Erro Absoluto (km/h)')
#        plt.title(f'{titulo} - Video {VIDEO} \n\n'
#              f'Média dos erros absolutos =  {ave_abs_error} km/h\n'
#              f'Média dos erros percentuais = {ave_per_error} % \n'
#              f' Qtnd de erros até 3km/h: {len(list_3km)} de {real_total_lane} ({round(len(list_3km)/real_total_lane*100, 2)} %)\n'
#              f' Qtnd de erros até 5km/h: {len(list_5km)} de {real_total_lane} ({round(len(list_5km)/real_total_lane*100, 2)} %)\n'
#              f' Qtnd de erros > 5km/h: {len(list_maior5km)} de {real_total_lane} ({round(len(list_maior5km)/real_total_lane*100, 2)} %)\n'
#              f'Taxa de Detecção: {rate_detec_lane} % \n'
#              f'Carros detectados: {total_cars_lane} de {real_total_lane} \n'
#              f'Fator de correção: {cf}')
#        
#        plt.plot([0, len(abs_list) + 3], [0, 0], color='k', linestyle='-', linewidth=1)
#        plt.plot([0, len(abs_list) + 3], [3, 3], color='k', linestyle=':', linewidth=1)
#        plt.plot([0, len(abs_list) + 3], [5, 5], color='k', linestyle='--', linewidth=1)
#        
#        plt.plot(sorted(abs_list), 'ro-')
#        plt.savefig(f'results/{DATE}/graficos/result_{DATE}_F{lane}_lin.png', bbox_inches='tight', pad_inches=0.3)
#        plt.savefig(f'results/{DATE}/graficos/pdfs/result_{DATE}_F{lane}_lin.pdf', bbox_inches='tight', pad_inches=0.3)


def separar_por_kmh(abs_error_list_mod):
    list_3km = []  # erros até 3km/h
    list_5km = []  # erros até 5km/h
    list_maior5km = []  # maiores que 5km/h    
    for value in abs_error_list_mod:
        if value <= 3:
            list_3km.append(value)
        elif value > 3 and value <=5:
            list_5km.append(value)
        else:
            list_maior5km.append(value)
    return list_3km, list_5km, list_maior5km

def perpective(frame, lane, RESIZE_RATIO):
    def r(numero):  # Faz o ajuste de escala das posições de textos e retangulos
        return int(numero*RESIZE_RATIO)
#    mask_h = frame.shape[0]
#    mask_w = frame.shape[1]
#    mask_crop = np.zeros((mask_h, mask_w), dtype=np.uint8)
    if lane == 1:
        points = np.array([[[r(-150), r(1080)], [r(480), r(1080)],
                           [r(560), r(0)], [r(270), 0] ]], np.int32)
        pt4 = [r(35),0]
        pt3 = [r(610),0]
        pt2 = [r(640), r(1080)]
        pt1 = [0, r(1080)]
        
        width = r(640)
        height = r(1080)
        target_pts = np.array([pt1,pt2,pt3,pt4 ], np.float32)
        H, mask_crop = cv2.findHomography(points, target_pts, cv2.RANSAC)
        warped_frame = cv2.warpPerspective(frame, H, (width, height))
        return warped_frame
        
    elif lane == 2:
        points = np.array([[[r(570), r(1080)],  [r(1310), r(1080)],
                            [r(900), r(0)],[r(640), r(0)]]], np.int32)
        pt4 = [r(50),0]
        pt3 = [r(570),0]
        pt2 = [r(640), r(1080)]
        pt1 = [0, r(1080)]
        
        width = r(640) # 640
        height = r(1080)
        target_pts = np.array([pt1,pt2,pt3,pt4 ], np.float32)
        H, mask_crop = cv2.findHomography(points, target_pts, cv2.RANSAC)
        warped_frame = cv2.warpPerspective(frame, H, (width, height))
        return warped_frame
        
        
    elif lane == 3:
        points = np.array([[[r(1410), r(1080)], [r(2170), r(1080)],
                            [r(1320), r(0)], [r(990), r(0)]]], np.int32)
        pt4 = [r(15),0]
        pt3 = [r(670),0]
        pt2 = [r(640), r(1080)]
        pt1 = [0, r(1080)] 
        # dimensoes da output image    
        width = r(640)
        height = r(1080)
        target_pts = np.array([pt1,pt2,pt3,pt4 ], np.float32)
        H, mask_crop = cv2.findHomography(points, target_pts, cv2.RANSAC)
        warped_frame = cv2.warpPerspective(frame, H, (width, height))
        return warped_frame
    
#    cv2.fillPoly(mask_crop, points, RED)
#    res = cv2.bitwise_and(frame,frame,mask=mask_crop)
#    rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
#    cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
#                # faixa 3 crop
#    frame_crop = frame[0:r(1079), r(990):r(1920)]
        
if __name__ == '__main__':
    print('arquivo ERRADOOOOOOO')
                
          
        