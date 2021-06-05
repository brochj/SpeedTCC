results_lane1[str(lane1_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                             speeds=lane1_tracking.closest_blob[
    'speed'],
    frame=frameCount,
    real_speed=float(
    dict_lane1['speed']),
    abs_error=round(
    abs_error, 2),
    per_error=round(
    per_error, 3),
    trail=lane1_tracking.closest_blob[
    'trail'],
    car_id=lane1_tracking.closest_blob['id'])


results_lane2[str(lane2_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                             speeds=lane2_tracking.closest_blob['speed'],
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


results_lane3[str(lane3_tracking.closest_blob['id'])] = dict(ave_speed=round(ave_speed, 2),
                                                             speeds=lane3_tracking.closest_blob[
    'speed'],
    frame=frameCount,
    real_speed=float(
    dict_lane3['speed']),
    abs_error=round(
    abs_error, 2),
    per_error=round(
    per_error, 3),
    trail=lane3_tracking.closest_blob[
    'trail'],
    car_id=lane3_tracking.closest_blob['id'])
