
import cv2

from functions import r
import config


class VehicleDetection:

    def __init__(self, processed_image, tracking_instance=None):
        self.lane = processed_image
        self.lane_tracking = tracking_instance  # TODO remover isso
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.center = 0
        self.detected = False

    def detection(self):
        for i in range(len(self.lane.contours)):
            if cv2.contourArea(self.lane.contours[i]) > r(config.MIN_AREA_FOR_DETEC):

                (self.x, self.y, self.w, self.h) = cv2.boundingRect(
                    self.lane.hull[i])
                self.center = (int(self.x + self.w/2), int(self.y + self.h/2))

                if self.w < r(340) and self.h < r(340):  # ponto que da pra mudar
                    continue
                # Área de medição do Tracking
                if self.center[1] > r(config.BOTTOM_LIMIT_TRACK_L2) or self.center[1] < r(config.UPPER_LIMIT_TRACK_L2):
                    continue

                self.detected = True
