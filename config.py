RESIZE_RATIO = .22222  # 0.7697  720p=.6667 480p=.4445 360p=.33333 240p=.22222 144p=.13333

# Faixa 1
UPPER_LIMIT_TRACK = 395

SHOW_ROI = True
SHOW_TRACKING_AREA = True
SHOW_TRAIL = True
SHOW_CAR_RECTANGLE = True

# ---- Tracking Values --------------------------------------------------------
# The maximum distance a blob centroid is allowed to move in order to
# consider it a match to a previous scene's blob.
BLOB_LOCKON_DIST_PX_MAX = 150  # default = 50 p/ ratio 0.35
BLOB_LOCKON_DIST_PX_MIN = 5  # default 5
MIN_AREA_FOR_DETEC = 30000  # Default 40000
# Limites da Área de Medição, área onde é feita o Tracking
# Distancia de medição: default 915-430 = 485
