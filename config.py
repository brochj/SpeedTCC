
VIDEO = 1
VIDEO_FILE = './Dataset/video{}.mp4'.format(VIDEO)
XML_FILE = './Dataset/video{}.xml'.format(VIDEO)

FPS = 30.15

CLOSE_VIDEO = 500  # 2950 #5934  # 1-6917 # 5-36253

SKIP_VIDEO = True

RESIZE_RATIO = .33333  # 0.7697  720p=.6667 480p=.4445 360p=.33333 240p=.22222 144p=.13333

# Faixa 1
BOTTOM_LIMIT_TRACK = 910  # 850  # Default 900
UPPER_LIMIT_TRACK = 395  # 350  # Default 430
# Faixa 2
BOTTOM_LIMIT_TRACK_L2 = 940  # 1095  # Default 940
UPPER_LIMIT_TRACK_L2 = 425  # 408 # Default 420
# Faixa 3
BOTTOM_LIMIT_TRACK_L3 = 930  # 1095  # Default 915
UPPER_LIMIT_TRACK_L3 = 430  # 408 # Default 430

SHOW_ROI = True
SHOW_TRACKING_AREA = True
SHOW_TRAIL = True
SHOW_CAR_RECTANGLE = True

SHOW_REAL_SPEEDS = True
SHOW_FRAME_COUNT = True

# ---- Tracking Values --------------------------------------------------------
# The maximum distance a blob centroid is allowed to move in order to
# consider it a match to a previous scene's blob.
BLOB_LOCKON_DIST_PX_MAX = 150  # default = 50 p/ ratio 0.35
BLOB_LOCKON_DIST_PX_MIN = 5  # default 5
MIN_AREA_FOR_DETEC = 30000  # Default 40000
# Limites da Área de Medição, área onde é feita o Tracking
# Distancia de medição: default 915-430 = 485
MIN_CENTRAL_POINTS = 10  # Minimum number of points needed to calculate speed
# The number of seconds a blob is allowed to sit around without having
# any new blobs matching it.
BLOB_TRACK_TIMEOUT = 0.1  # Default 0.7
# ---- Speed Values -----------------------------------------------------------
CF_LANE1 = 2.10  # 2.10  # default 2.5869977 # Correction Factor
CF_LANE2 = 2.32  # default 2.32    3.758897
CF_LANE3 = 2.3048378  # default 2.304837879578
