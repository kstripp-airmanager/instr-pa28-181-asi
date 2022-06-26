#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge
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

# Colors
FACE_COLOR = '#131512'
TICK_COLOR = '#FFFFFF'
WHITE_ARC_COLOR = '#FFFFFF'
GREEN_ARC_COLOR = '#008000'
YELLOW_ARC_COLOR = '#F9C806'
REDLINE_COLOR = '#FF0000'

# Speed Range
V_min = 35
V_max = 170

# Tick geometry
MAJ_TICK_WIDTH = 6
MAJ_TICK_HEIGHT = 60
TAS_TICK_HEIGHT = 23

MIN_TICK_WIDTH = 3
MIN_TICK_HEIGHT = 30

# V-speeds
V_s0 = 49   # Stall, landing config.  Bottom of white arc
V_s = 55    # Stall, clean config.  Bottom of green arc
V_fe = 102  # Max flap extension speed.  Top of white arc
V_no  = 125 # Masimum structural speed.  Green / yellow transition
V_ne = 154  # Never exceed speed.  Red line / top of yello arc

V_ARC_WIDTH = 9

# Known speed angles
# These are the best estimates from skewed photos
# Note: Angles are measured clockwise from vertical
speeds = [0, 40, 70, 105, 140, 170]
angles = [0, 30, 90, 180, 270, 330]

#################################################
# Fit function

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

#################################################
# Generate the gauge face

# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/figure_size_units.html
px = 1/plt.rcParams['figure.dpi']
fix, ax = plt.subplots(figsize=(560*px, 560*px))

# Create overall geometry
x = (FACE_DIAM/2-1) * np.sin(2*np.pi* np.array([0, 90, 180, 270])/360)
y = (FACE_DIAM/2-1) * np.cos(2*np.pi* np.array([0, 90, 180, 270])/360)
ax.plot(x, y, '.', color=FACE_COLOR)
ax.axis("Off")
plt.gca().set_aspect('equal')

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

plt.savefig("guage_face.png", transparent=True)
#plt.show()
