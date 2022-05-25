# ---- Perspective ------------------------------------------------------------
PERSPECTIVE_POINTS = {
    "origin": {
        "bottom_left": (-150, 1080),
        "bottom_right": (480, 1080),
        "top_right": (560, 0),
        "top_left": (270, 0),
    },
    "target": {
        "bottom_left": (0, 1080),
        "bottom_right": (640, 1080),
        "top_right": (610, 0),
        "top_left": (35, 0),
    },
}
# ---- Image Processing -------------------------------------------------------
KERNEL_ERODE = (12, 12)
KERNEL_DILATE_L1 = (120, 400)


# ---- Speed Values -----------------------------------------------------------
# Correction Factor
CF_LANE1 = 2.10  # 2.10  # default 2.5869977 # Correction Factor
