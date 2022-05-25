# ---- Perspective ------------------------------------------------------------
PERSPECTIVE_POINTS = {
    "origin": {
        "bottom_left": (1410, 1080),
        "bottom_right": (2170, 1080),
        "top_right": (1320, 0),
        "top_left": (990, 0),
    },
    "target": {
        "bottom_left": (0, 1080),
        "bottom_right": (640, 1080),
        "top_right": (670, 0),
        "top_left": (15, 0),
    },
}
# ---- Image Processing -------------------------------------------------------
KERNEL_ERODE = (12, 12)
KERNEL_DILATE_L3 = (100, 320)


# ---- Speed Values -----------------------------------------------------------
# Correction Factor
CF_LANE3 = 2.3048378  # default 2.304837879578
