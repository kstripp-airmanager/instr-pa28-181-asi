#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
# Speed Range
V_min = 35
V_max = 170

# Known speed angles
# These are the best estimates from skewed photos
speeds = [0, 40, 70, 105, 140, 170]
angles = [0, 30, 90, 180, 270, 330]

#################################################
# Fit function

ref_speeds = np.array(speeds)
ref_angles = np.array(angles)

vfit = np.poly1d(np.polyfit(speeds, angles, 3))
v_angle = lambda v: vfit(v)

speed_ticks = np.arange(V_min, V_max+5, 5)
angles = v_angle(speed_ticks) + 90

# Plot the fit function
plt.plot(ref_speeds, ref_angles, label="reference")
plt.plot(speed_ticks, angles - 90, label="fit")
plt.legend()
plt.title("Airspeed polyfit")
plt.xlabel("Speed")
plt.ylabel("Indicator angle (\u00B0)")

plt.savefig("fit_function.png")

plt.show()
