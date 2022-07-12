#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge
from matplotlib.text import Text
from matplotlib import rcParams
import numpy as np

# Geometry
BEZEL_WIDTH = 480 # px
FACE_DIAM = 470   # px, outer diameter of the face image
FACE_WIDTH = 396  # px
WINDOW_OUTER = 205 # px, outer radius of windows
TEMP_WINDOW_INNER = 170 # px, inner radius of temperature window
TAS_WINDOW_INNER = 162 # px, inner radius of TAS window

TEMP_WINDOW_ANGLE = 40 # degrees, symmetric around vertical
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

# Speed Range
V_min = 35
V_max = 170

# Tick geometry
MAJ_TICK_WIDTH = 6
MAJ_TICK_HEIGHT = 60
TAS_TICK_HEIGHT = 23

MIN_TICK_WIDTH = 3
MIN_TICK_HEIGHT = 30

TEMP_TICK_HEIGHT = 15
TEMP_TICK_WIDTH = 3

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

# Known speed angles
# These are the best estimates from skewed photos
# Note: Angles are measured clockwise from vertical
speeds = [0, 40, 70, 105, 140, 170]
angles = [0, 30, 90, 180, 270, 325]

# Temperature scale
temp_min = -30
temp_max = 30
temp_step = 10
temp_angle_min = -17
temp_angle_max = 17
temp_label_step = 30 # label every 30 degrees

t_font_size = 12
t_label_inset = 15

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
        't': 122,
        'kwargs': {"rotation":58, "linespacing":0.9},
    },{
        'text': "P\nALT",
        'fontsize' : 11,
        'color' : LABEL_COLOR,
        'r': TEMP_WINDOW_INNER,
        't': -27,
        'kwargs': {"rotation":25},
    }
]
#################################################
# Fit functions

ref_speeds = np.array(speeds)
ref_angles = np.array(angles)

vfit = np.poly1d(np.polyfit(speeds, angles, 3))
v_angle = lambda v: -1 * vfit(v) + 90

speed_ticks = np.arange(V_min, V_max+5, 5)
angles = v_angle(speed_ticks)

# Plot the fit function
plt.plot(ref_speeds, ref_angles, label="reference")
plt.plot(speed_ticks, angles - 90, label="fit")
plt.legend()
plt.title("Airspeed polyfit")
plt.xlabel("Speed")
plt.ylabel("Indicator angle (\u00B0)")

plt.savefig("fit_function.png")

# Temperature tick fit
temp_angle = lambda t: temp_angle_max/temp_max * t

#################################################
# Generate the gauge face

# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/figure_size_units.html
px = 1/plt.rcParams['figure.dpi']
fix, ax = plt.subplots(figsize=(560*px, 560*px))

# Set up general figure properties
x = (FACE_DIAM/2-1) * np.sin(2*np.pi* np.array([0, 90, 180, 270])/360)
y = (FACE_DIAM/2-1) * np.cos(2*np.pi* np.array([0, 90, 180, 270])/360)
ax.plot(x, y, '.', color=FACE_COLOR)
ax.axis("Off")
plt.gca().set_aspect('equal')

rcParams['font.family'] = 'Alte DIN 1451 Mittelschrift'

# The DIN 1451 font is close, but the I glyph matches the 1 glyph seen on the actual gauge
typeset = lambda s: str(s).replace("1", "I")

# Draw face border
radius = np.mean([FACE_DIAM/2, WINDOW_OUTER])
width = FACE_DIAM/2 - WINDOW_OUTER
ax.add_patch(Circle((0,0), radius=radius, color=FACE_COLOR,
                   linewidth=width, fill=False))

# Fill in face around windows
theta1 = v_angle(TAS_MIN_IAS)
theta2 = -1 * TEMP_WINDOW_ANGLE/2 + 90
ax.add_patch(Wedge((0,0), FACE_DIAM/2, theta1, theta2, color=FACE_COLOR))

theta1 = 1 * TEMP_WINDOW_ANGLE/2 + 90
theta2 = v_angle(TAS_MAX_IAS)
ax.add_patch(Wedge((0,0), FACE_DIAM/2, theta1, theta2, color=FACE_COLOR))

theta1 = -1 * TEMP_WINDOW_ANGLE/2 + 90
theta2 = 1 * TEMP_WINDOW_ANGLE/2 + 90
ax.add_patch(Wedge((0,0),TEMP_WINDOW_INNER, theta1, theta2, color=FACE_COLOR))

theta1 = v_angle(TAS_MAX_IAS)
theta2 = v_angle(TAS_MIN_IAS)
ax.add_patch(Wedge((0,0),TAS_WINDOW_INNER, theta1, theta2, color=FACE_COLOR))

# Draw speed range arcs
theta1 = v_angle(TAS_MIN_IAS)
theta2 = v_angle(V_s0)
ax.add_patch(Wedge((0,0),(FACE_WIDTH/2-V_ARC_WIDTH), theta1, theta2, width=V_ARC_WIDTH, color=WHITE_ARC_COLOR))

theta1 = v_angle(V_fe)
theta2 = v_angle(TAS_MIN_IAS)
ax.add_patch(Wedge((0,0),TAS_WINDOW_INNER-V_ARC_WIDTH, theta1, theta2, width=V_ARC_WIDTH, color=WHITE_ARC_COLOR))

theta1 = v_angle(TAS_MIN_IAS)
theta2 = v_angle(V_s)
ax.add_patch(Wedge((0,0),(FACE_WIDTH/2), theta1, theta2, width=V_ARC_WIDTH, color=GREEN_ARC_COLOR))

theta1 = v_angle(V_no)
theta2 = v_angle(TAS_MIN_IAS)
ax.add_patch(Wedge((0,0),TAS_WINDOW_INNER, theta1, theta2, width=V_ARC_WIDTH, color=GREEN_ARC_COLOR))

theta1 = v_angle(V_ne)
theta2 = v_angle(V_no)
ax.add_patch(Wedge((0,0),(FACE_WIDTH/2), theta1, theta2, width=V_ARC_WIDTH, color=YELLOW_ARC_COLOR))

# Redline speed
angle = v_angle(V_ne)
theta = 2*np.pi * angle/360
x = (FACE_WIDTH/2) * np.cos(theta)
y = (FACE_WIDTH/2) * np.sin(theta)
width = MIN_TICK_WIDTH/2
height = np.mean([MIN_TICK_HEIGHT, MAJ_TICK_HEIGHT])
ax.add_patch(Rectangle((x,y),  1 * width, -1 * height, angle-90, color=REDLINE_COLOR))
ax.add_patch(Rectangle((x,y), -1 * width, -1 * height, angle-90, color=REDLINE_COLOR))

# Draw ticks
for idx, angle in enumerate(angles):
    theta = 2*np.pi * angle/360

    # Widths are the same for all ticks
    width = MAJ_TICK_WIDTH/2 if idx % 2 == 1 else MIN_TICK_WIDTH/2

    # Height and location varies around TAS window
    x = (FACE_WIDTH/2) * np.cos(theta)
    y = (FACE_WIDTH/2) * np.sin(theta)
    if angle > v_angle(TAS_MIN_IAS):
        height = MAJ_TICK_HEIGHT if idx % 2 == 1 else MIN_TICK_HEIGHT
    elif angle >= v_angle(TAS_MAX_IAS):
        x = (TAS_WINDOW_INNER) * np.cos(theta)
        y = (TAS_WINDOW_INNER) * np.sin(theta)
        height = TAS_TICK_HEIGHT
    else:
        height = MAJ_TICK_HEIGHT if idx % 2 == 1 else MIN_TICK_HEIGHT

    ax.add_patch(Rectangle((x,y),  1 * width, -1 * height, angle-90, color=TICK_COLOR))
    ax.add_patch(Rectangle((x,y), -1 * width, -1 * height, angle-90, color=TICK_COLOR))

# Add speed labels
for idx, speed in enumerate(v_labels):
    angle = v_angle(speed)
    theta = 2*np.pi * angle/360

    # Height and location varies around TAS window
    if angle > v_angle(TAS_MIN_IAS):
        fontsize = v_font_large
        radius = FACE_WIDTH/2 - MAJ_TICK_HEIGHT - V_LABEL_INSET
    elif angle >= v_angle(TAS_MAX_IAS):
        fontsize = v_font_small
        radius = TAS_WINDOW_INNER - TAS_TICK_HEIGHT - V_LABEL_INSET
    else:
        fontsize = v_font_large
        radius = FACE_WIDTH/2 - MAJ_TICK_HEIGHT - V_LABEL_INSET

    x = (radius) * np.cos(theta)
    y = (radius) * np.sin(theta)

    # The DIN 1451 font is close, but the I glyph matches the 1 glyph seen on the actual gauge
    plt.text(x,y, typeset(speed), color=TICK_COLOR, ha='center', va='center', size=fontsize)

# Draw Temperature ticks
for temperature in np.arange(temp_min, (temp_max + temp_step), temp_step):

    angle = temp_angle(temperature) + 90
    theta = 2*np.pi * angle/360

    width = TEMP_TICK_WIDTH/2
    height = TEMP_TICK_HEIGHT

    x = TEMP_WINDOW_INNER * np.cos(theta)
    y = TEMP_WINDOW_INNER * np.sin(theta)

    ax.add_patch(Rectangle((x,y),  1 * width, -1 * height, angle-90, color=TICK_COLOR))
    ax.add_patch(Rectangle((x,y), -1 * width, -1 * height, angle-90, color=TICK_COLOR))

    if temperature % temp_label_step == 0:
        
        radius = TEMP_WINDOW_INNER - TEMP_TICK_HEIGHT - t_label_inset
        fontsize = t_font_size
        x = (radius) * np.cos(theta)
        y = (radius) * np.sin(theta)

        # explicit sign, but not on 0: https://stackoverflow.com/a/2763589
        label = '{0:{1}}'.format(temperature, '+' if temperature else '')
        plt.text(x,y, typeset(label), color=TICK_COLOR, ha='center', va='center', size=fontsize)

# Draw other labels
for label in labels:
    
    theta = 2*np.pi * label['t']/360
    x = (label['r']) * np.sin(theta)
    y = (label['r']) * np.cos(theta)
    kwargs = label['kwargs'] if 'kwargs' in label.keys() else {}

    plt.text(x,y, typeset(label['text']), color=label['color'],
             ha='center', va='center',
             size=label['fontsize'], **kwargs)

plt.savefig("guage_face.png", transparent=True)
#plt.show()
