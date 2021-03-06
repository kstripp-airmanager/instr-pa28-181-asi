# Reference files
# Note: Angles are measured clockwise from vertical
IAS_REF = "ias_reference.csv"
TAS_REF = "tas_reference.csv"
ALT_REF = "alt_reference.csv"

# Instrument ID
instrument_id = "af0fcd2a-a0ae-454f-a97f-aa228736acaf"

# Geometry
GAUGE_WIDTH = 512 # px, total gauge image size used for Air Manager
BEZEL_WIDTH = 480 # px
FACE_DIAM = 465   # px, outer diameter of the face image
FACE_WIDTH = 380  # px
WINDOW_OUTER = 200 # px, outer radius of windows
TEMP_WINDOW_INNER = 155 # px, inner radius of temperature window
TAS_WINDOW_INNER = 158 # px, inner radius of TAS window

TEMP_WINDOW_ANGLE = 36 # degrees, symmetric around vertical
TAS_MIN_IAS = 84 # knots, min IAS covered by TAS window
TAS_MAX_IAS = 125 # knots, max IAS covered by TAS window

V_LABEL_INSET = 25 # px, inset distance inside tick marks

# Colors
FACE_COLOR = '#131512'
TICK_COLOR = '#FFFFFF'
WHITE_ARC_COLOR = '#FFFFFF'
GREEN_ARC_COLOR = '#008000'
YELLOW_ARC_COLOR = '#F9C806'
REDLINE_COLOR = '#FF0000'
LABEL_COLOR = '#FFFFFF'
MODEL_TEXT_COLOR = '#00859F'

CARD_COLOR = '#E6E6E6'
CARD_MARK_COLOR = '#050505'

# Tick geometry
MAJ_TICK_WIDTH = 6
MAJ_TICK_HEIGHT = 60
TAS_TICK_HEIGHT = 23 # IAS tick near TAS window

MIN_TICK_WIDTH = 3
MIN_TICK_HEIGHT = 30

TEMP_TICK_HEIGHT = 15
TEMP_TICK_WIDTH = 3

ALT_MAJ_HEIGHT = 50
ALT_MAJ_WIDTH = 1
ALT_MIN_HEIGHT = 10
ALT_MIN_WIDTH = 0.5
ALT_LABEL_OFFSET = 20

TAS_MAJ_HEIGHT = 10 # TAS ticks on card
TAS_MAJ_WIDTH = 1
TAS_MIN_HEIGHT = 10
TAS_MIN_WIDTH = 0.5
TAS_LABEL_OFFSET = 25

# Speed Range
V_min = 35
V_max = 170

# V-speeds
V_s0 = 49   # Stall, landing config.  Bottom of white arc
V_s = 55    # Stall, clean config.  Bottom of green arc
V_fe = 102  # Max flap extension speed.  Top of white arc
V_no = 125  # Masimum structural speed.  Green / yellow transition
V_ne = 154  # Never exceed speed.  Red line / top of yello arc

V_ARC_WIDTH = 9

# Speed Labels
v_labels = [40, 60, 80, 100, 120, 140, 160]
v_font_large = 20 # pt
v_font_small = 14 # pt

# Temperature scale
temp_min = -30
temp_max = 30
temp_step = 10
temp_angle_min = -15
temp_angle_max = 15
temp_label_step = 30 # label every 30 degrees

t_font_size = 12
t_label_inset = 15

# Altitude card scale
alt_min = -2000
alt_max = 18000
alt_step = 500
alt_font = 8

# True Airspeed card scale
tas_min = 70
tas_max = 150
tas_step = 5
tas_font = 13

# Other labels
labels = [
    {
        'text': "AIRSPEED",
        'fontsize' : 14,
        'color' : LABEL_COLOR,
        'r': 58, # placement radius
        't': 0,  # palcement angle
    },{
        'text': "TEMP\n\u00B0C",
        'fontsize' : 11,
        'color' : LABEL_COLOR,
        'r': 95,
        't': 0,
    },{
        'text': "28-181",
        'fontsize' : 10,
        'color' : MODEL_TEXT_COLOR,
        'r': 38,
        't': 0,
    },{
        'text': "KNOTS",
        'fontsize' : 11,
        'color' : LABEL_COLOR,
        'r': 50,
        't': 180,
    },{
        'text': "T\nA\nS",
        'fontsize' : 11,
        'color' : LABEL_COLOR,
        'r': TAS_WINDOW_INNER-20,
        't': 120,
        'kwargs': {"rotation":58, "linespacing":0.9},
    },{
        'text': "P\nALT",
        'fontsize' : 11,
        'color' : LABEL_COLOR,
        'r': TEMP_WINDOW_INNER,
        't': -28,
        'kwargs': {"rotation":25},
    }
]
