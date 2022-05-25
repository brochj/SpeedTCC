from core.perspective import Perspective
from core.image_processing import ImageProcessing
from core.tracking import Tracking
from core.vehicle_speed import VehicleSpeed
from core.vehicle_detection import VehicleDetection
import lib.drawings as draw

Objects = dict[
    "perspective":Perspective,
    "image_processing":ImageProcessing,
    "tracking":Tracking,
    "vehicle_speed":VehicleSpeed,
    "detection":VehicleDetection,
]


class Lane:
    def __init__(self, obj: Objects) -> None:

        self.perspective = obj["perspective"]
        self.image_processing = obj["image_processing"]
        self.tracking = obj["tracking"]
        self.vehicle_speed = obj["vehicle_speed"]
        self.detection = obj["detection"]
        self.frame = None
        self.vehicle_detected = False

    def start_monitoring(
        self,
        frame,
        frame_hist,
        frame_time: float,
        dict_lane: dict,
        positionOfResult: tuple = (0, 0),
    ):
        self.apply_perspective(frame_hist)
        self.apply_morphological_operations()
        self.start_detection()

        if self.vehicle_detected:
            self.start_tracking(frame_time)
            self.calculate_speed(dict_lane)

            draw.result(
                frame,
                self.vehicle_speed,
                self.tracking.tracked_blobs["id"],
                positionOfResult,
            )
            draw.car_rectangle(frame, self.frame, self.detection, positionOfResult[0])

        # Remove timeout trails
        self.remove_expired_track(frame_time)
        draw.blobs(self.frame, self.tracking.tracked_blobs)

    def apply_perspective(self, frame_hist):
        self.frame = self.perspective.apply_perspective(frame_hist)
        return self.frame

    def apply_morphological_operations(self):
        self.image_processing.apply_morphological_operations(self.frame)

    def start_detection(self):
        self.detection.reset()
        self.detection.detection(self.image_processing)
        self.vehicle_detected = self.detection.detected

    def start_tracking(self, frame_time: float):
        self.tracking.tracking(self.detection.center, frame_time)

    def calculate_speed(self, dict_lane: dict):
        self.vehicle_speed.calc_speed(self.tracking, dict_lane)

    def remove_expired_track(self, frame_time: float):
        self.tracking.remove_expired_track(frame_time, self.vehicle_speed)
