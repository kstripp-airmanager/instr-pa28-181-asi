#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge
from matplotlib.text import Text
from matplotlib import rcParams
import numpy as np
import prettytable

from config import *

#####################################################################
def compute_ias_fit(display=False):

    ias_ref = np.loadtxt(IAS_REF, delimiter=',', skiprows=1)

    vfit = np.poly1d(np.polyfit(ias_ref[:,0], ias_ref[:,1], 3))
    v_angle = lambda v: -1 * vfit(v) + 90

    speed_ticks = np.arange(V_min, V_max+5, 5)
    angles = v_angle(speed_ticks)

    # Display the fit function
    if display:
        pt = prettytable.PrettyTable()

        pt.field_names = ["Airspeed", "Fit Angle"]

        for speed in range(40, 180, 10):
            pt.add_row([speed, int(90 - v_angle(speed))])

        print(pt)

    # Plot the fit function
    plt.figure()
    plt.plot(ias_ref[:,0], ias_ref[:,1], label="reference")
    plt.plot(speed_ticks, 90 - angles, label="fit")
    plt.legend()
    plt.title("Airspeed polyfit")
    plt.xlabel("Speed")
    plt.ylabel("Indicator angle (\u00B0)")
    plt.savefig("ias_fit.png")

    plt.figure()
    plt.plot(ias_ref[1:,0], np.diff(ias_ref[:,1]), label="reference")
    plt.plot(speed_ticks[1:], np.diff(90 - angles), label="fit")
    plt.legend()
    plt.title("Airspeed fit derivative")
    plt.xlabel("Speed Step")
    plt.ylabel("Relative angle (\u00B0)")
    plt.savefig("ias_fit_diff.png")


    return v_angle

#####################################################################
def compute_tas_fit(display=False):
    """ Compute fit function for true airspeed angles"""

    tas_ref = np.loadtxt(TAS_REF, delimiter=',', skiprows=1)
    
    # Pressure altitude tick fit
    vfit = np.poly1d(np.polyfit(tas_ref[:,0], tas_ref[:,1], 1))
    tas_angle = lambda v: -1 * vfit(v) + 90

    # Display the fit function
    if display:
        pt = prettytable.PrettyTable()

        pt.field_names = ["True Airspeed", "Fit Angle"]

        for tas in range(70, 160, 10):
            pt.add_row([tas, int(90 - tas_angle(tas))])

        print(pt)

    return tas_angle

#####################################################################
def compute_alt_fit(display=False):
    """ Compute fit function for pressure altitude angles"""

    alt_ref = np.loadtxt(ALT_REF, delimiter=',', skiprows=1)
    
    # Pressure altitude tick fit
    vfit = np.poly1d(np.polyfit(alt_ref[:,0], alt_ref[:,1], 1))
    alt_angle = lambda v: -1 * vfit(v) + 90

    # Display the fit function
    if display:
        pt = prettytable.PrettyTable()

        pt.field_names = ["Altitude", "Fit Angle"]

        for alt in range(-2000, 12000, 1000):
            pt.add_row([alt, int(90 - alt_angle(alt))])

        print(pt)

    return alt_angle

#####################################################################
def compute_temp_fit():

    # Temperature tick fit
    return lambda t: temp_angle_max/temp_max * t

#####################################################################
def draw_face():

    v_angle = compute_ias_fit()
    temp_angle = compute_temp_fit()
    
    speed_ticks = np.arange(V_min, V_max+5, 5)
    angles = v_angle(speed_ticks)

    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/figure_size_units.html
    px = 1/plt.rcParams['figure.dpi']
    fix, ax = plt.subplots(figsize=(GAUGE_WIDTH*px, GAUGE_WIDTH*px))

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

    plt.savefig(f"../{instrument_id}/resources/gauge_face.png", transparent=True)
    #plt.show()

#####################################################################
def draw_card():
    
    alt_angle = compute_alt_fit(display=True)
    alt_ticks = np.arange(alt_min, alt_max+alt_step, alt_step)
    alt_angles = alt_angle(alt_ticks)
    
    tas_angle = compute_tas_fit(display=True)
    tas_ticks = np.arange(tas_min, tas_max+tas_step, tas_step)
    tas_angles = tas_angle(tas_ticks)

    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/figure_size_units.html
    px = 1/plt.rcParams['figure.dpi']
    fix, ax = plt.subplots(figsize=(GAUGE_WIDTH*px, GAUGE_WIDTH*px))

    # Set up general figure properties
    x = (WINDOW_OUTER-1) * np.sin(2*np.pi* np.array([0, 90, 180, 270])/360)
    y = (WINDOW_OUTER-1) * np.cos(2*np.pi* np.array([0, 90, 180, 270])/360)
    ax.plot(x, y, '.', color=CARD_COLOR)
    ax.axis("Off")
    plt.gca().set_aspect('equal')

    rcParams['font.family'] = 'Alte DIN 1451 Mittelschrift'

    # The DIN 1451 font is close, but the I glyph matches the 1 glyph seen on the actual gauge
    typeset = lambda s: str(s).replace("1", "I")

    # Draw card background
    radius = WINDOW_OUTER
    ax.add_patch(Circle((0,0), radius=radius, color=CARD_COLOR))
    
    # Draw altitude ticks
    for idx, angle in enumerate(alt_angles):
        theta = 2*np.pi * angle/360

        # Tick width based on major or minor
        width = ALT_MAJ_WIDTH/2 if alt_ticks[idx] % 1000 == 0 else ALT_MIN_WIDTH/2
        height = ALT_MAJ_HEIGHT if alt_ticks[idx] % 1000 == 0 else ALT_MIN_HEIGHT

        # Height and location varies around TAS window
        x = (TEMP_WINDOW_INNER) * np.cos(theta)
        y = (TEMP_WINDOW_INNER) * np.sin(theta)

        ax.add_patch(Rectangle((x,y),  0.5 * width, height, angle-90, color=CARD_MARK_COLOR))
        ax.add_patch(Rectangle((x,y), -0.5 * width, height, angle-90, color=CARD_MARK_COLOR))
        
        if alt_ticks[idx] % 2000 == 0:
            x = (TEMP_WINDOW_INNER+ ALT_LABEL_OFFSET) * np.cos(theta)
            y = (TEMP_WINDOW_INNER+ ALT_LABEL_OFFSET) * np.sin(theta)
            label = int(alt_ticks[idx]/1000)
            plt.text(x,y, typeset(label), color=CARD_MARK_COLOR,
                     rotation = angle-90,
                     backgroundcolor = CARD_COLOR,
                     ha='center', va='center', size=alt_font)

    # Draw TAS ticks
    for idx, angle in enumerate(tas_angles):
        theta = 2*np.pi * angle/360

        # Tick width based on major or minor
        width = TAS_MAJ_WIDTH/2 if alt_ticks[idx] % 1000 == 0 else TAS_MIN_WIDTH/2
        height = TAS_MAJ_HEIGHT if alt_ticks[idx] % 1000 == 0 else TAS_MIN_HEIGHT

        # Height and location varies around TAS window
        x = (TAS_WINDOW_INNER) * np.cos(theta)
        y = (TAS_WINDOW_INNER) * np.sin(theta)
        ax.add_patch(Rectangle((x,y),  0.5 * width, height, angle-90, color=CARD_MARK_COLOR))
        ax.add_patch(Rectangle((x,y), -0.5 * width, height, angle-90, color=CARD_MARK_COLOR))

        if tas_ticks[idx] % 10 == 0:
            x = (TAS_WINDOW_INNER+ TAS_LABEL_OFFSET) * np.cos(theta)
            y = (TAS_WINDOW_INNER+ TAS_LABEL_OFFSET) * np.sin(theta)
            label = int(tas_ticks[idx])
            plt.text(x,y, typeset(label), color=CARD_MARK_COLOR,
                     rotation = angle+90,
                     backgroundcolor = CARD_COLOR,
                     ha='center', va='center', size=tas_font)

    plt.savefig(f"../{instrument_id}/resources/gauge_card.png", transparent=True)

#####################################################################
if __name__ == "__main__":
    draw_face()
    draw_card()
