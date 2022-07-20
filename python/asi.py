#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge
from matplotlib.text import Text
from matplotlib import rcParams
import numpy as np
import prettytable

from config import *

#################################################
# Fit functions

ref_speeds = np.array(speeds)
ref_angles = np.array(angles)

vfit = np.poly1d(np.polyfit(speeds, angles, 3))
v_angle = lambda v: -1 * vfit(v) + 90

speed_ticks = np.arange(V_min, V_max+5, 5)
angles = v_angle(speed_ticks)

# Display the fit function
pt = prettytable.PrettyTable()

pt.field_names = ["Airspeed", "Fit Angle"]

for speed in range(40, 180, 10):
    pt.add_row([speed, int(90 - v_angle(speed))])

print(pt)

# Plot the fit function
plt.plot(ref_speeds, ref_angles, label="reference")
plt.plot(speed_ticks, 90 - angles, label="fit")
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
