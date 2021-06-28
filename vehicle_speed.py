
import cv2
import numpy as np

from functions import r
import config


class VehicleSpeed:
    def __init__(self, correction_factor):
        self.correction_factor = correction_factor
        self.abs_error = None
        self.pct_error = None
        self.avg_speed = None
        self.lane_tracking = None
        self.measured_speed_xml = None
        self.vehicle_speeds = {
            'speeds': [],
        }

        self.pixel_size_in_meters = self.__calc_pixel_size_in_meters()
        self.delta_t = self.__calc_delta_t()

    def __calc_pixel_size_in_meters(self):
        MED_AREA_METER = 3.9  # meters (estimated value)
        MED_AREA_PIXEL = r(485)
        return (MED_AREA_METER/MED_AREA_PIXEL)

    def __calc_delta_t(self):
        FRAME_QUANTITY = 11
        return (FRAME_QUANTITY * (1/config.FPS))

    def calculate_speed(self, trail):
        distance_in_pixel = self.__calc_distance_in_pixel(trail)
        distance_in_meters = distance_in_pixel * self.pixel_size_in_meters
        speed = self.__calc_delta_s(distance_in_meters) / self.delta_t
        return round(speed, 1)

    def __calc_distance_in_pixel(self, trail):
        last_point = trail[0]
        first_point = trail[10]
        return cv2.norm(last_point, first_point)

    def __calc_delta_s(self, distance_in_meters):
        return (distance_in_meters*3.6*self.correction_factor)

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
                lane_tracking.tracked_blobs['trail'])
            lane_tracking.tracked_blobs['speed'].insert(0, speed)
            print('vehicle_speeds: ', self.vehicle_speeds)
            self.calculate_avg_speed(lane_tracking.tracked_blobs['speed'])
            # self.vehicle_speeds['speeds'].insert(0, speed)
            # self.calculate_avg_speed(self.vehicle_speeds['speeds'])
            self.calc_abs_error()
            self.calc_pct_error()
            self.update_values()

    def reset_values(self):
        self.abs_error = None
        self.pct_error = None
        self.avg_speed = None
        self.lane_tracking = None
        self.measured_speed_xml = None
        self.vehicle_speeds = {
            'speeds': [],
        }
