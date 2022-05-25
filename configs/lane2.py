# ---- Perspective ------------------------------------------------------------
PERSPECTIVE_POINTS = {
    "origin": {
        "bottom_left": (570, 1080),
        "bottom_right": (1310, 1080),
        "top_right": (900, 0),
        "top_left": (640, 0),
    },
    "target": {
        "bottom_left": (0, 1080),
        "bottom_right": (640, 1080),
        "top_right": (570, 0),
        "top_left": (50, 0),
    },
}
# ---- Image Processing -------------------------------------------------------
KERNEL_ERODE = (12, 12)
KERNEL_DILATE_L2 = (100, 400)


# ---- Speed Values -----------------------------------------------------------
# Correction Factor
CF_LANE2 = 2.32  # default 2.32    3.758897
