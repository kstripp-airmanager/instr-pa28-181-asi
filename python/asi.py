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
TAS_MAX_IAS = 120 # knots, max IAS covered by TAS window

# Colors
FACE_COLOR = '#131512'
TICK_COLOR = '#FFFFFF'

# Speed Range
V_min = 35
V_max = 170

# Tick geometry
MAJ_TICK_WIDTH = 6
MAJ_TICK_HEIGHT = 60

MIN_TICK_WIDTH = 3
MIN_TICK_HEIGHT = 30


# Known speed angles
# These are the best estimates from skewed photos
speeds = [0, 40, 70, 105, 140, 170]
angles = [0, 30, 90, 180, 270, 330]

#################################################
# Fit function

ref_speeds = np.array(speeds)
ref_angles = np.array(angles)

vfit = np.poly1d(np.polyfit(speeds, angles, 3))
v_angle = lambda v: vfit(v) + 90

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

fix, ax = plt.subplots()

# Create overall geometry
x = (FACE_DIAM/2-1) * np.sin(2*np.pi* np.array([0, 90, 180, 270])/360)
y = (FACE_DIAM/2-1) * np.cos(2*np.pi* np.array([0, 90, 180, 270])/360)
ax.plot(x, y, '.', color=FACE_COLOR)
ax.axis("Off")
plt.gca().set_aspect('equal')


# Draw ticks
for idx, angle in enumerate(angles):
    theta = 2*np.pi * angle/360
    x = (FACE_WIDTH/2) * np.cos(theta)
    y = (FACE_WIDTH/2) * np.sin(theta)

    width = MAJ_TICK_WIDTH/2 if idx % 2 == 1 else MIN_TICK_WIDTH/2
    height = MAJ_TICK_HEIGHT if idx % 2 == 1 else MIN_TICK_HEIGHT

    ax.add_patch(Rectangle((x,y),  1 * width, -1 * height, angle-90, color=TICK_COLOR))
    ax.add_patch(Rectangle((x,y), -1 * width, -1 * height, angle-90, color=TICK_COLOR))
plt.savefig("guage_face.png", transparent=True)
#plt.show()
