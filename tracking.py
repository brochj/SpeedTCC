# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 21:26:30 2020

@author: broch
"""
import cv2
import uuid

from functions import r
import config


class Tracking:
    def __init__(self, name, resize_ratio=None, lock_on_max=None, lock_on_min=None):
        self.name = name
        self.lock_on_max = lock_on_max or config.BLOB_LOCKON_DIST_PX_MAX
        self.lock_on_min = lock_on_min or config.BLOB_LOCKON_DIST_PX_MIN
        self.resize_ratio = resize_ratio or config.RESIZE_RATIO
        self.tracked_blobs = {}
        self.frame_time = 0.0

    def r(self, number):
        return int(number*self.resize_ratio)

    def __lock_on(self, new_center, last_center):
        """ Check if the distance between centers is close enough to "lock on" """
        distance = cv2.norm(new_center, last_center)
        if distance < r(self.lock_on_max) and distance > r(self.lock_on_min):
            self.__add_new_center_to_trail(new_center)

    def __add_new_center_to_trail(self, center):
        """ Checks if the new center is above the last center then add it to trail """
        if self.__is_moving_up(center):
            self.tracked_blobs['trail'].insert(0, center)  # Add point
            self.tracked_blobs['last_seen'] = self.frame_time

    def __is_moving_up(self, center):
        """ Checks if the new center is above the last center 
            returns: True if the object is moving up
        """
        if self.tracked_blobs:
            last_center = self.tracked_blobs['trail'][0]
            return center[1] < last_center[1]

    def __create_tracked_blobs_dict(self, center):
        """ If we didn't find a blob, let's make a new one and add the first center value """
        if not self.tracked_blobs:
            self.tracked_blobs = dict(id=str(uuid.uuid4())[:8], first_seen=self.frame_time,
                                      last_seen=self.frame_time, trail=[center], speed=[])

    def is_there_minimum_points(self):
        if self.tracked_blobs:
            return len(self.tracked_blobs['trail']) > config.MIN_CENTRAL_POINTS

    def tracking(self, center, frame_time):
        self.frame_time = frame_time
        # Look for existing blobs that match this one
        if self.tracked_blobs:
            print(
                f"tracked_blobs: {self.tracked_blobs['id']} | trail points: {len(self.tracked_blobs['trail'])} | speed:{self.tracked_blobs['speed']} ")

            self.__lock_on(center, self.tracked_blobs['trail'][0])
        else:
            self.__create_tracked_blobs_dict(center)

    def remove_expired_track(self, frame_time, vehicle_speed, blob_track_timeout=config.BLOB_TRACK_TIMEOUT):
        if self.tracked_blobs:
            # Prune out the blobs that haven't been seen in some amount of time
            # Deleta caso de timeout
            if frame_time - self.tracked_blobs['last_seen'] > blob_track_timeout:
                print("Removing expired trail tracking from {} | id: {} |".format(
                    self.name, self.tracked_blobs['id']))
                self.tracked_blobs = {}
                vehicle_speed.reset_values()


if __name__ == '__main__':
    raise Exception('Wrong File')
