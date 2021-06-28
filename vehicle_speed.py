
import cv2
import numpy as np

from functions import r
import config


class VehicleSpeed:
    def __init__(self):
        self.abs_error = 0
        self.pct_error = 0
        self.avg_speed = 0
        self.lane_tracking = None
        self.measured_speed_xml = None
        self.vehicle_speeds = {
            'speeds': [],
        }

    def reset_values(self):
        self.abs_error = 0
        self.pct_error = 0
        self.avg_speed = 0
        self.lane_tracking = None
        self.measured_speed_xml = None
        self.vehicle_speeds = {
            'speeds': [],
        }

    def calculate_speed(self, trails, correction_factor):
        med_area_meter = 3.9  # metros (Valor estimado)
        med_area_pixel = r(485)
        qntd_frames = 11  # len(trails)  # default 11
        # Sem usar Regressão linear
        dist_pixel = cv2.norm(trails[0], trails[10])
        dist_meter = dist_pixel*(med_area_meter/med_area_pixel)
        speed = (dist_meter*3.6*correction_factor)/(qntd_frames*(1/config.FPS))
        return round(speed, 1)

    def calculate_avg_speed(self, speeds):
        self.avg_speed = np.mean(speeds)
        return self.avg_speed

    def calc_abs_error(self):
        self.abs_error = self.avg_speed - float(self.measured_speed_xml)
        self.abs_error = round(self.abs_error, 2)

    def calc_pct_error(self):
        numerator = abs(self.avg_speed - float(self.measured_speed_xml))
        denominator = float(self.measured_speed_xml)
        self.pct_error = (numerator/denominator)*100
        self.pct_error = round(self.pct_error, 2)

    def update_values(self):
        self.vehicle_speeds = {
            'avg_speed': self.avg_speed,
            'abs_error': self.abs_error,
            'pct_error': self.pct_error,
            'measured_speed_xml': self.measured_speed_xml,
        }

    def calc_speed(self, lane_tracking, measured_speed_xml):
        self.lane_tracking = lane_tracking
        self.measured_speed_xml = measured_speed_xml.get('speed')
        if len(lane_tracking.tracked_blobs['trail']) > config.MIN_CENTRAL_POINTS:
            speed = self.calculate_speed(
                lane_tracking.tracked_blobs['trail'], config.CF_LANE3)
            lane_tracking.tracked_blobs['speed'].insert(0, speed)
            print('vehicle_speeds: ', self.vehicle_speeds)
            self.calculate_avg_speed(lane_tracking.tracked_blobs['speed'])
            # self.vehicle_speeds['speeds'].insert(0, speed)
            # self.calculate_avg_speed(self.vehicle_speeds['speeds'])
            self.calc_abs_error()
            self.calc_pct_error()
            self.update_values()
