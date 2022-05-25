## Dados
```python

dict_lane1 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 1
dict_lane2 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 2
dict_lane3 = {}  # Armazena os valores de "speed, frame_start, frame_end" da FAIXA 3

KERNEL_DILATE_L1 = (120, 400)
KERNEL_DILATE_L2 = (100, 400)
KERNEL_DILATE_L3 = (100, 320)

lane1_perspective = Perspective(lane=1)
lane2_perspective = Perspective(lane=2)
lane3_perspective = Perspective(lane=3)


lane1 = ImageProcessing(bgsMOG, KERNEL_ERODE, KERNEL_DILATE_L1)
lane2 = ImageProcessing(bgsMOG, KERNEL_ERODE, KERNEL_DILATE_L2)
lane3 = ImageProcessing(bgsMOG, KERNEL_ERODE, KERNEL_DILATE_L3)

lane1_tracking = Tracking(name='lane 1')
lane2_tracking = Tracking(name='lane 2')
lane3_tracking = Tracking(name='lane 3')

lane1_vehicle_speed = VehicleSpeed(config.CF_LANE1)
lane2_vehicle_speed = VehicleSpeed(config.CF_LANE2)
lane3_vehicle_speed = VehicleSpeed(config.CF_LANE3)

frame_lane1 = lane1_perspective.apply_perspective(frame_hist)
frame_lane2 = lane2_perspective.apply_perspective(frame_hist)
frame_lane3 = lane3_perspective.apply_perspective(frame_hist)


```

```py

dict_lane1 = {speed, frame_start, frame_end}  # {'speed': '56.65', 'frame_start': '71', 'frame_end': '111'}

KERNEL_DILATE_L1 = (120, 400)

lane1_perspective = Perspective(lane=1)

lane1 = ImageProcessing(bgsMOG, KERNEL_ERODE, KERNEL_DILATE_L1)

lane1_tracking = Tracking(name='lane 1')

lane1_vehicle_speed = VehicleSpeed(config.CF_LANE1)

frame_lane1 = lane1_perspective.apply_perspective(frame_hist)
```

