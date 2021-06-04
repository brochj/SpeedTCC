# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:21:59 2020

@author: broch
"""

# ##############  FUNÇÕES ###########
import numpy as np
import itertools as it
import colors
import matplotlib.pyplot as plt
import cv2
import config


def r(number):  # Faz o ajuste de escala
    return int(number*config.RESIZE_RATIO)


def get_frame(cap, resize_ratio=config.RESIZE_RATIO):
    #" Grabs a frame from the video vcture and resizes it. "
    ret, frame = cap.read()
    if ret:
        (h, w) = frame.shape[:2]
        frame = cv2.resize(frame, (int(w*resize_ratio),
                                   int(h*resize_ratio)), interpolation=cv2.INTER_CUBIC)
    return ret, frame


def region_of_interest(frame, resize_ratio):
    def r(numero):  # Faz o ajuste de escala
        return int(numero*resize_ratio)
    # Retângulo superior
#    cv2.rectangle(frame, (0, 0), (r(1920), r(120)), colors.BLACK, -1)
    # triângulo lado direito
    pts = np.array([[r(1920), r(790)], [r(1290), 0], [r(1920), 0]], np.int32)
    cv2.fillPoly(frame, [pts], colors.BLACK)
    # triângulo lado esquerdo
    pts3 = np.array([[0, r(620)], [r(270), 0], [0, 0]], np.int32)
    cv2.fillPoly(frame, [pts3], colors.BLACK)
    # Linha entre faixas 1 e 2
    pts1 = np.array([[r(480), r(1080)], [r(560), r(0)],
                     [r(640), r(0)], [r(570), r(1080)]], np.int32)
    cv2.fillPoly(frame, [pts1], colors.BLACK)
    # Linha entre faixas 2 e 3
    pts7 = np.array([[r(1310), r(1080)], [r(900), r(0)],
                     [r(990), r(0)], [r(1410), r(1080)]], np.int32)
    cv2.fillPoly(frame, [pts7], colors.BLACK)
    # Faixa 3
    return frame


def histogram_equalization(frame_gray):
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    hist_equalization = clahe.apply(frame_gray)
    return hist_equalization


#### SPEED FUNCTIONS ########################################################################
def calculate_speed(trails, fps, correction_factor):

    med_area_meter = 3.9  # metros (Valor estimado)
    med_area_pixel = r(485)
    qntd_frames = 11  # len(trails)  # default 11
    dist_pixel = cv2.norm(trails[0], trails[10])  # Sem usar Regressão linear
    dist_meter = dist_pixel*(med_area_meter/med_area_pixel)
    speed = (dist_meter*3.6*correction_factor)/(qntd_frames*(1/fps))
    return round(speed, 1)


def calculate_avg_speed(speed_array):
    return np.mean(speed_array)


def calculate_errors(calculated_speed, measured_speed):
    try:
        abs_error = calculated_speed - float(measured_speed)
        per_error = (
            abs(calculated_speed - float(measured_speed))/float(measured_speed))*100
        return abs_error, per_error
    except Exception as e:
        print('Erro dentro de calculate_errors()')
        print(e)


##### END - SPEED FUNTIONS #####################################################


def show_results_on_screen(frame, frameCount, ave_speed, lane, blob, total_cars, RESIZE_RATIO, VIDEO,
                           dict_lane1, dict_lane2, dict_lane3, SAVE_FRAME_F1, SAVE_FRAME_F2, SAVE_FRAME_F3):
    def r(numero):  # Faz o ajuste de escala das posições de textos e retangulos
        return int(numero*RESIZE_RATIO)
    color = colors.WHITE
    if lane == 1:
        dict_lane = dict_lane1
        positions = [(r(350), r(120)), (r(550), r(120)),
                     (r(550), r(180)), (r(550), r(230))]
    if lane == 2:
        dict_lane = dict_lane2
        positions = [(r(830), r(120)), (r(1030), r(120)),
                     (r(1030), r(180)), (r(1030), r(230))]
    if lane == 3:
        dict_lane = dict_lane3
        positions = [(r(1350), r(120)), (r(1550), r(120)),
                     (r(1550), r(180)), (r(1550), r(230))]

#    cv2.putText(frame, str(float("{0:.2f}".format(ave_speed))), (blob['trail'][0][0] + r(57), blob['trail'][0][1] + r(143)),
#                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, colors.YELLOW, thickness=1, lineType=2)
    # Texto da que fica embaixo da velocidade real
    try:
        dif_lane = ave_speed - float(dict_lane['speed'])
        error_lane = (
            abs(ave_speed - float(dict_lane['speed']))/float(dict_lane['speed']))*100
    except:
        pass
    try:
        if abs(dif_lane) <= 3:
            color = colors.GREEN
        elif abs(dif_lane) > 3 and abs(dif_lane) <= 5:
            color = colors.YELLOW
        elif abs(dif_lane) > 5 and abs(dif_lane) <= 10:
            color = colors.ORANGE
        elif abs(dif_lane) > 10:
            color = colors.RED

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
        cv2.imwrite('img/novo/{}-{}_F1_Carro_{}.png'.format(VIDEO,
                                                            frameCount, total_cars['lane_{}'.format(lane)]), frame)
    if SAVE_FRAME_F2 and lane == 2:
        cv2.imwrite('img/novo/{}-{}_F2_Carro_{}.png'.format(VIDEO,
                                                            frameCount, total_cars['lane_{}'.format(lane)]), frame)
    if SAVE_FRAME_F3 and lane == 3:
        cv2.imwrite('img/novo/{}-{}_F3_Carro_{}.png'.format(VIDEO,
                                                            frameCount, total_cars['lane_{}'.format(lane)]), frame)

    # PRINTA FAIXA 2
#    cv2.putText(frame, 'Faixa {}'.format(lane), (blob['trail'][0][0] - r(29), blob['trail'][0][1] + r(200)),
#                cv2.FONT_HERSHEY_COMPLEX_SMALL, .8, colors.WHITE, thickness=1, lineType=2)


def skip_video(frameCount, video, frame):
    skip = False
    if video == 1:
        if frameCount < 49:
            skip = True
        if frameCount > 90 and frameCount < 96:
            skip = True
        if frameCount > 130 and frameCount < 176:
            skip = True
        if frameCount > 212 and frameCount < 235:
            skip = True
        if frameCount > 336 and frameCount < 361:
            skip = True
        if frameCount > 394 and frameCount < 425:
            skip = True  # Caminhão
        if frameCount > 460 and frameCount < 467:
            skip = True
        if frameCount > 499 and frameCount < 563:
            skip = True
        if frameCount > 598 and frameCount < 614:
            skip = True
        if frameCount > 644 and frameCount < 696:
            skip = True
        if frameCount > 731 and frameCount < 739:
            skip = True
        if frameCount > 781 and frameCount < 794:
            skip = True
        if frameCount > 829 and frameCount < 857:
            skip = True
        if frameCount > 856 and frameCount < 895:
            skip = True  # carro preto F3, da pra por (tava com erro altissimo)
        if frameCount > 894 and frameCount < 925:
            skip = True
        if frameCount > 958 and frameCount < 1054:
            skip = True
        if frameCount > 1053 and frameCount < 1101:
            skip = True  # Caminhão
        if frameCount > 1100 and frameCount < 1140:
            skip = True
        if frameCount > 1139 and frameCount < 1199:
            skip = True  # Carro parado
        if frameCount > 1198 and frameCount < 2650:
            skip = True  # Carro baixa velocidade
        if frameCount > 2689 and frameCount < 2715:
            skip = True
        if frameCount > 2850 and frameCount < 2870:
            skip = True
#        if frameCount > 3035 and frameCount < 3045: skip = True # carro taxi
#        if frameCount > 3230 and frameCount < 3242: skip = True
#        if frameCount > 3100 and frameCount < 3115: skip = True
#        if frameCount > 2979 and frameCount < 3018: skip = True
#        if frameCount > 3030 and frameCount < 3050: skip = True
#        if frameCount > 3060 and frameCount < 3090: skip = True
#        if frameCount > 3122 and frameCount < 3166: skip = True
#        if frameCount > 3279 and frameCount < 3328: skip = True
#        if frameCount > 3404 and frameCount < 3459: skip = True
        if frameCount > 3550 and frameCount < 4800:
            skip = True
#        if frameCount > 5270 and frameCount < 5285: skip = True
#        if frameCount > 5375 and frameCount < 5390: skip = True
#        if frameCount > 5525 and frameCount < 5540: skip = True
#        if frameCount > 5738 and frameCount < 5753: skip = True
#        if frameCount > 5615 and frameCount < 5630: skip = True
        if frameCount > 5322 and frameCount < 5352:
            skip = True
        if frameCount > 5401 and frameCount < 5507:
            skip = True  # caminhao
        if frameCount > 5554 and frameCount < 5604:
            skip = True  # van no meio da faixa
        if frameCount > 5667 and frameCount < 5698:
            skip = True
        if frameCount > 5785 and frameCount < 5902:
            skip = True
        if frameCount > 5934 and frameCount < 6918:
            skip = True  # Carro parado
    return skip


def plot_graph(abs_error_list, ave_abs_error, ave_per_error, rate_detec_lane,
               real_total_lane, total_cars_lane, DATE, lane, VIDEO, cf, SHOW_LIN,
               list_3km, list_5km, list_maior5km):

    plt.figure(lane, figsize=[9, 7])
    plt.plot(abs_error_list, 'o-')

    plt.plot([0, len(abs_error_list) + 3], [0, 0],
             color='k', linestyle='-', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [3, 3],
             color='k', linestyle=':', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [-3, -3],
             color='k', linestyle=':', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [5, 5],
             color='k', linestyle='--', linewidth=1)
    plt.plot([0, len(abs_error_list) + 3], [-5, -5],
             color='k', linestyle='--', linewidth=1)

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

    plt.savefig(f'results/{DATE}/graficos/result_{DATE}_F{lane}.png',
                bbox_inches='tight', pad_inches=0.3)
    plt.savefig(f'results/{DATE}/graficos/pdfs/result_{DATE}_F{lane}.pdf',
                bbox_inches='tight', pad_inches=0.3)
    plt.show()

    if SHOW_LIN:
        plt.figure('Total', figsize=[9, 7])
        abs_list = []
        for value in abs_error_list:
            abs_list.append(abs(value))

        font = {'size': 16}
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

        plt.plot([0, len(abs_error_list) + 3], [0, 0],
                 color='k', linestyle='-', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [3, 3],
                 color='k', linestyle=':', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [-3, -3],
                 color='k', linestyle=':', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [5, 5],
                 color='k', linestyle='--', linewidth=1)
        plt.plot([0, len(abs_error_list) + 3], [-5, -5],
                 color='k', linestyle='--', linewidth=1)

        plt.plot(abs_error_list, 'ro-')
        plt.savefig(f'results/{DATE}/graficos/result_{DATE}_F{lane}_lin.png',
                    bbox_inches='tight', pad_inches=0.3)
        plt.savefig(f'results/{DATE}/graficos/pdfs/result_{DATE}_F{lane}_lin.pdf',
                    bbox_inches='tight', pad_inches=0.3)

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
        elif value > 3 and value <= 5:
            list_5km.append(value)
        else:
            list_maior5km.append(value)
    return list_3km, list_5km, list_maior5km


def perspective(frame, lane, RESIZE_RATIO):
    def r(numero):  # Faz o ajuste de escala das posições de textos e retangulos
        return int(numero*RESIZE_RATIO)
#    mask_h = frame.shape[0]
#    mask_w = frame.shape[1]
#    mask_crop = np.zeros((mask_h, mask_w), dtype=np.uint8)
    if lane == 1:
        points = np.array([[[r(-150), r(1080)], [r(480), r(1080)],
                            [r(560), r(0)], [r(270), 0]]], np.int32)
        pt4 = [r(35), 0]
        pt3 = [r(610), 0]
        pt2 = [r(640), r(1080)]
        pt1 = [0, r(1080)]

        width = r(640)
        height = r(1080)
        target_pts = np.array([pt1, pt2, pt3, pt4], np.float32)
        H, mask_crop = cv2.findHomography(points, target_pts, cv2.RANSAC)
        warped_frame = cv2.warpPerspective(frame, H, (width, height))
        return warped_frame

    elif lane == 2:
        points = np.array([[[r(570), r(1080)],  [r(1310), r(1080)],
                            [r(900), r(0)], [r(640), r(0)]]], np.int32)
        pt4 = [r(50), 0]
        pt3 = [r(570), 0]
        pt2 = [r(640), r(1080)]
        pt1 = [0, r(1080)]

        width = r(640)  # 640
        height = r(1080)
        target_pts = np.array([pt1, pt2, pt3, pt4], np.float32)
        H, mask_crop = cv2.findHomography(points, target_pts, cv2.RANSAC)
        warped_frame = cv2.warpPerspective(frame, H, (width, height))
        return warped_frame

    elif lane == 3:
        points = np.array([[[r(1410), r(1080)], [r(2170), r(1080)],
                            [r(1320), r(0)], [r(990), r(0)]]], np.int32)
        pt4 = [r(15), 0]
        pt3 = [r(670), 0]
        pt2 = [r(640), r(1080)]
        pt1 = [0, r(1080)]
        # dimensoes da output image
        width = r(640)
        height = r(1080)
        target_pts = np.array([pt1, pt2, pt3, pt4], np.float32)
        H, mask_crop = cv2.findHomography(points, target_pts, cv2.RANSAC)
        warped_frame = cv2.warpPerspective(frame, H, (width, height))
        return warped_frame


if __name__ == '__main__':
    print('arquivo ERRADO')
