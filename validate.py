

import cv2
import config


class Validate():
    pass

    for i in range(len(lane2.contours)):
        if cv2.contourArea(lane2.contours[i]) > r(MIN_AREA_FOR_DETEC):

            (x_L2, y_L2, w_L2, h_L2) = cv2.boundingRect(lane2.hull[i])
            center_L2 = (int(x_L2 + w_L2/2), int(y_L2 + h_L2/2))
            # out_L2 = cv2.rectangle(out_L2, (x_L2, y_L2), (x_L2 + w_L2, y_L2 + h_L2), colors.GREEN, 2) # printa na mask
            # CONDIÇÕES PARA CONTINUAR COM TRACKING

            if w_L2 < r(340) and h_L2 < r(340):  # ponto que da pra mudar
                continue
            # Área de medição do Tracking
            if center_L2[1] > r(BOTTOM_LIMIT_TRACK_L2) or center_L2[1] < r(UPPER_LIMIT_TRACK_L2):
                continue

            draw.car_rectangle(center_L2, frame, frame_lane2,
                               x_L2, y_L2, w_L2, h_L2, left_padding=600)

            # ################## TRACKING #################################
            lane2_tracking.tracking(center_L2, frame_time)
            try:
                if len(lane2_tracking.closest_blob['trail']) > MIN_CENTRAL_POINTS:
                    lane2_tracking.closest_blob['speed'].insert(0, t.calculate_speed(
                        lane2_tracking.closest_blob['trail'], FPS, CF_LANE2))
                    lane = 2
                    ave_speed = np.mean(
                        lane2_tracking.closest_blob['speed'])
                    abs_error, per_error = t.write_results_on_image(frame, frameCount, ave_speed, lane, lane2_tracking.closest_blob['id'], RESIZE_RATIO, VIDEO,
                                                                    dict_lane1, dict_lane2, dict_lane3)

                    results_lane2[str(lane2_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                                                 speeds=lane2_tracking.closest_blob[
                        'speed'],
                        frame=frameCount,
                        real_speed=float(
                        dict_lane2['speed']),
                        abs_error=round(
                        abs_error, 2),
                        per_error=round(
                        per_error, 3),
                        trail=lane2_tracking.closest_blob[
                        'trail'],
                        car_id=lane2_tracking.closest_blob['id'])

                    abs_error = []
                    per_error = []
            except:
                pass
