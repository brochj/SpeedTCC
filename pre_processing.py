import cv2
import numpy as np
import colors
from copy import deepcopy
import config


class PreProcessing:

    @staticmethod
    def frame_to_grayscale(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def apply_region_of_interest(frame):
        frame_roi = deepcopy(frame)

        def r(numero):  # Faz o ajuste de escala
            return int(numero*config.RESIZE_RATIO)

        # triângulo lado direito
        pts = np.array(
            [[r(1920), r(790)], [r(1290), 0], [r(1920), 0]], np.int32)
        cv2.fillPoly(frame_roi, [pts], colors.BLACK)
        # triângulo lado esquerdo
        pts3 = np.array([[0, r(620)], [r(270), 0], [0, 0]], np.int32)
        cv2.fillPoly(frame_roi, [pts3], colors.BLACK)
        # Linha entre faixas 1 e 2
        pts1 = np.array([[r(480), r(1080)], [r(560), r(0)],
                         [r(640), r(0)], [r(570), r(1080)]], np.int32)
        cv2.fillPoly(frame_roi, [pts1], colors.BLACK)
        # Linha entre faixas 2 e 3
        pts7 = np.array([[r(1310), r(1080)], [r(900), r(0)],
                         [r(990), r(0)], [r(1410), r(1080)]], np.int32)
        cv2.fillPoly(frame_roi, [pts7], colors.BLACK)
        # Faixa 3
        return frame_roi

    @staticmethod
    def apply_histogram_equalization(frame_gray):
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        hist_equalization = clahe.apply(frame_gray)
        return hist_equalization


if __name__ == '__main__':
    raise Exception('Wrong File')
