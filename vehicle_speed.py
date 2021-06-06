
import cv2
import numpy as np

from functions import r

import config


class VehicleSpeed:
    def __init__(self):
        self.abs_error = None
        self.pct_error = None
        self.avg_speed = None

    def calculate_speed(self, trails, fps, correction_factor):
        med_area_meter = 3.9  # metros (Valor estimado)
        med_area_pixel = r(485)
        qntd_frames = 11  # len(trails)  # default 11
        # Sem usar Regressão linear
        dist_pixel = cv2.norm(trails[0], trails[10])
        dist_meter = dist_pixel*(med_area_meter/med_area_pixel)
        speed = (dist_meter*3.6*correction_factor)/(qntd_frames*(1/fps))
        return round(speed, 1)

    def calculate_avg_speed(self, speeds):
        self.avg_speed = np.mean(speeds)
        return self.avg_speed

    def calculate_errors(self, calculated_speed, measured_speed):
        try:
            self.abs_error = calculated_speed - float(measured_speed)
            self.pct_error = (
                abs(calculated_speed - float(measured_speed))/float(measured_speed))*100
            return self.abs_error, self.pct_error
        except Exception as e:
            print('Erro dentro de calculate_errors()')
            print(e)

    def calc_speed(self, lane_tracking, dict_lane):
        try:
            if len(lane_tracking.closest_blob['trail']) > config.MIN_CENTRAL_POINTS:
                lane_tracking.closest_blob['speed'].insert(0, self.calculate_speed(
                    lane_tracking.closest_blob['trail'], config.FPS, config.CF_LANE3))
                self.calculate_avg_speed(lane_tracking.closest_blob['speed'])
                self.calculate_errors(self.avg_speed, dict_lane['speed'])

        except (TypeError, KeyError):
            pass
