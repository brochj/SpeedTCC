# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 21:26:30 2020

@author: broch
"""
import cv2
import uuid


class Tracking:
    def __init__(self, resize_ratio, lock_on_max, lock_on_min):
        self.lock_on_max = lock_on_max
        self.lock_on_min = lock_on_min
        self.resize_ratio = resize_ratio
        self.closest_blob = None
        self.tracked_blobs = []
        self.frame_time = 0.0

    def r(self, number):
        return int(number * self.resize_ratio)

    def __lock_on(self, center, close_blob):
        """ Check if the distance between centers is close enough to "lock on" """
        distance = cv2.norm(center, close_blob["trail"][0])
        if distance < self.r(self.lock_on_max) and distance > self.r(self.lock_on_min):
            self.closest_blob = close_blob

    def __add_new_center_to_trail(self, center):
        """ Checks if the new center is above the last center then add it to trail """
        if self.__is_moving_up(center):
            self.closest_blob["trail"].insert(0, center)  # Add point
            self.closest_blob["last_seen"] = self.frame_time

    def __is_moving_up(self, center):
        """Checks if the new center is above the last center
        returns: True if the object is moving up
        """
        if self.closest_blob:
            previous_center = self.closest_blob["trail"][0]
            return center[1] < previous_center[1]

    def __create_tracked_blobs_dict(self, center):
        """ If we didn't find a blob, let's make a new one and add the first center value """
        if not self.closest_blob:
            b = dict(
                id=str(uuid.uuid4())[:8],
                first_seen=self.frame_time,
                last_seen=self.frame_time,
                trail=[center],
                speed=[0],
            )
            self.tracked_blobs.append(b)  # Now tracked_blobs won't be False anymore

    def tracking(self, center, frame_time):
        self.frame_time = frame_time
        # Look for existing blobs that match this one
        self.closest_blob = None
        if self.tracked_blobs:
            print(f"self.tracked_blobs: {self.tracked_blobs}")
            # Sort the blobs we have seen in previous frames by pixel distance from this one
            # FIXME sorted_blobs = sorted(self.tracked_blobs, key=lambda b: cv2.norm(b['trail'][0], center)) # Sorted Not working
            sorted_blobs = self.tracked_blobs
            print(f"sorted_blobs: {sorted_blobs}")

            self.__lock_on(center, sorted_blobs[0])

            self.__add_new_center_to_trail(center)
        else:
            self.__create_tracked_blobs_dict(center)

    def remove_expired_track(self, blob_track_timeout, name, frame_time):
        if self.tracked_blobs:
            # Prune out the blobs that haven't been seen in some amount of time
            for i in range(len(self.tracked_blobs) - 1, -1, -1):
                if (
                    frame_time - self.tracked_blobs[i]["last_seen"] > blob_track_timeout
                ):  # delete if timeout
                    print(
                        f'Removing expired track from {name} | id: {self.tracked_blobs[i]["id"]} |'
                    )
                    del self.tracked_blobs[i]


if __name__ == "__main__":
    print("Wrong file: tracking.py executed")
