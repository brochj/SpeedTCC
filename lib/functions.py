# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:21:59 2020

@author: broch
"""

# ##############  FUNÇÕES ###########
import numpy as np
import itertools as it
import lib.colors as colors
import matplotlib.pyplot as plt
import cv2
import configs.config as config


def r(number):  # Faz o ajuste de escala
    return int(number * config.RESIZE_RATIO)


def get_frame(cap, resize_ratio=config.RESIZE_RATIO):
    # " Grabs a frame from the video vcture and resizes it. "
    ret, frame = cap.read()
    if ret:
        (h, w) = frame.shape[:2]
        frame = cv2.resize(
            frame,
            (int(w * resize_ratio), int(h * resize_ratio)),
            interpolation=cv2.INTER_CUBIC,
        )
    return ret, frame


def show_results_on_screen(
    frame,
    frameCount,
    ave_speed,
    lane,
    blob,
    total_cars,
    RESIZE_RATIO,
    VIDEO,
    dict_lane1,
    dict_lane2,
    dict_lane3,
    SAVE_FRAME_F1,
    SAVE_FRAME_F2,
    SAVE_FRAME_F3,
):
    def r(numero):  # Faz o ajuste de escala das posições de textos e retangulos
        return int(numero * RESIZE_RATIO)

    color = colors.WHITE
    if lane == 1:
        dict_lane = dict_lane1
        positions = [
            (r(350), r(120)),
            (r(550), r(120)),
            (r(550), r(180)),
            (r(550), r(230)),
        ]
    if lane == 2:
        dict_lane = dict_lane2
        positions = [
            (r(830), r(120)),
            (r(1030), r(120)),
            (r(1030), r(180)),
            (r(1030), r(230)),
        ]
    if lane == 3:
        dict_lane = dict_lane3
        positions = [
            (r(1350), r(120)),
            (r(1550), r(120)),
            (r(1550), r(180)),
            (r(1550), r(230)),
        ]

    #    cv2.putText(frame, str(float("{0:.2f}".format(ave_speed))), (blob['trail'][0][0] + r(57), blob['trail'][0][1] + r(143)),
    #                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, colors.YELLOW, thickness=1, lineType=2)
    # Texto da que fica embaixo da velocidade real
    try:
        dif_lane = ave_speed - float(dict_lane["speed"])
        error_lane = (
            abs(ave_speed - float(dict_lane["speed"])) / float(dict_lane["speed"])
        ) * 100
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

        cv2.putText(
            frame,
            str(float("{0:.2f}".format(ave_speed))),
            positions[0],
            2,
            0.6,
            color,
            thickness=1,
            lineType=2,
        )  # Velocidade Medida
        cv2.putText(
            frame,
            str(float("{0:.2f} ".format(dif_lane))),
            positions[1],
            2,
            0.6,
            color,
            thickness=1,
            lineType=2,
        )  # erro absoluto
        cv2.putText(
            frame,
            str(float("{0:.2f}".format(error_lane))) + "%",
            positions[2],
            2,
            0.6,
            color,
            thickness=1,
            lineType=2,
        )  # erro percentual
        cv2.putText(
            frame,
            "Carro " + str(total_cars["lane_{}".format(lane)]),
            positions[3],
            2,
            0.6,
            color,
            thickness=1,
            lineType=2,
        )
    except:
        pass

    if SAVE_FRAME_F1 and lane == 1:
        cv2.imwrite(
            "img/novo/{}-{}_F1_Carro_{}.png".format(
                VIDEO, frameCount, total_cars["lane_{}".format(lane)]
            ),
            frame,
        )
    if SAVE_FRAME_F2 and lane == 2:
        cv2.imwrite(
            "img/novo/{}-{}_F2_Carro_{}.png".format(
                VIDEO, frameCount, total_cars["lane_{}".format(lane)]
            ),
            frame,
        )
    if SAVE_FRAME_F3 and lane == 3:
        cv2.imwrite(
            "img/novo/{}-{}_F3_Carro_{}.png".format(
                VIDEO, frameCount, total_cars["lane_{}".format(lane)]
            ),
            frame,
        )

    # PRINTA FAIXA 2


#    cv2.putText(frame, 'Faixa {}'.format(lane), (blob['trail'][0][0] - r(29), blob['trail'][0][1] + r(200)),
#                cv2.FONT_HERSHEY_COMPLEX_SMALL, .8, colors.WHITE, thickness=1, lineType=2)


def skip_video(frameCount, video, frame):
    skip = False
    if video == 1:
        if frameCount < 49:
            skip = True
        elif frameCount > 90 and frameCount < 96:
            skip = True
        elif frameCount > 130 and frameCount < 176:
            skip = True
        elif frameCount > 212 and frameCount < 235:
            skip = True
        elif frameCount > 336 and frameCount < 361:
            skip = True
        elif frameCount > 394 and frameCount < 425:
            skip = True  # Caminhão
        elif frameCount > 460 and frameCount < 467:
            skip = True
        elif frameCount > 499 and frameCount < 563:
            skip = True
        elif frameCount > 598 and frameCount < 614:
            skip = True
        elif frameCount > 644 and frameCount < 696:
            skip = True
        elif frameCount > 731 and frameCount < 739:
            skip = True
        elif frameCount > 781 and frameCount < 794:
            skip = True
        elif frameCount > 829 and frameCount < 857:
            skip = True
        elif frameCount > 856 and frameCount < 895:
            skip = True  # carro preto F3, da pra por (tava com erro altissimo)
        elif frameCount > 894 and frameCount < 925:
            skip = True
        elif frameCount > 958 and frameCount < 1054:
            skip = True
        elif frameCount > 1053 and frameCount < 1101:
            skip = True  # Caminhão
        elif frameCount > 1100 and frameCount < 1140:
            skip = True
        elif frameCount > 1139 and frameCount < 1199:
            skip = True  # Carro parado
        elif frameCount > 1198 and frameCount < 2650:
            skip = True  # Carro baixa velocidade
        elif frameCount > 2689 and frameCount < 2715:
            skip = True
        elif frameCount > 2850 and frameCount < 2870:
            skip = True
        #        elif frameCount > 3035 and frameCount < 3045: skip = True # carro taxi
        #        elif frameCount > 3230 and frameCount < 3242: skip = True
        #        elif frameCount > 3100 and frameCount < 3115: skip = True
        #        elif frameCount > 2979 and frameCount < 3018: skip = True
        #        elif frameCount > 3030 and frameCount < 3050: skip = True
        #        elif frameCount > 3060 and frameCount < 3090: skip = True
        #        elif frameCount > 3122 and frameCount < 3166: skip = True
        #        elif frameCount > 3279 and frameCount < 3328: skip = True
        #        elif frameCount > 3404 and frameCount < 3459: skip = True
        elif frameCount > 3550 and frameCount < 4800:
            skip = True
        #        elif frameCount > 5270 and frameCount < 5285: skip = True
        #        elif frameCount > 5375 and frameCount < 5390: skip = True
        #        elif frameCount > 5525 and frameCount < 5540: skip = True
        #        elif frameCount > 5738 and frameCount < 5753: skip = True
        #        elif frameCount > 5615 and frameCount < 5630: skip = True
        elif frameCount > 5322 and frameCount < 5352:
            skip = True
        elif frameCount > 5401 and frameCount < 5507:
            skip = True  # caminhao
        elif frameCount > 5554 and frameCount < 5604:
            skip = True  # van no meio da faixa
        elif frameCount > 5667 and frameCount < 5698:
            skip = True
        elif frameCount > 5785 and frameCount < 5902:
            skip = True
        elif frameCount > 5934 and frameCount < 6918:
            skip = True  # Carro parado
    return skip


def should_skip_this(frame_count):
    if config.SKIP_VIDEO:
        skip = skip_video(frame_count, config.VIDEO, frame_count)
        if skip:
            return True
        return False


if __name__ == "__main__":
    print("Arquivo Errado")
