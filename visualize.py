#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 10:19:00 2026

@author: labadmin
"""

# https://www.geeksforgeeks.org/python/python-scroll-through-plots/

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pyxdf

fname = "sample_recording/sub-P001_ses-S001_task-Default_run-001_polarh10.xdf"
fname = 'sample_recording/sub-P001_ses-S001_task-Default_run-001_ecg.xdf'

data, header = pyxdf.load_xdf(fname)

for stream in data:

    if stream['info']['type'][0] =='HR':
        hr = stream["time_series"]
        hr_t = stream["time_stamps"]

    if stream['info']['type'][0] =='ECG':
        ecg = stream["time_series"]
        ecg_t = stream["time_stamps"]

    if stream['info']['type'][0] =='ACC':
        acc = stream["time_series"]
        acc_t = stream["time_stamps"]
        
    '''
    if isinstance(y, list):
        # list of strings, draw one vertical line for each marker
        for timestamp, marker in zip(stream["time_stamps"], y):
            plt.axvline(x=timestamp)
            print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
    elif isinstance(y, np.ndarray):
        # numeric data, draw as lines
        plt.plot(stream["time_stamps"], y)
    else:
        raise RuntimeError("Unknown stream format")
    '''

ecg_t = ecg_t - ecg_t[0]

plt.show()



# Setting Plot and Axis variables as subplots()
# function returns tuple(fig, ax)
Plot, Axis = plt.subplots()

# Adjust the bottom size according to the
# requirement of the user
plt.subplots_adjust(bottom=0.25)

# Set the x and y axis to some dummy data
#t = np.arange(0.0, 100.0, 0.1)
#s = np.sin(2*np.pi*t)

# plot the x and y using plot function
l = plt.plot(ecg_t, ecg)

# Choose the Slider color
slider_color = 'White'

# Set the axis and slider position in the plot
axis_position = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor = slider_color)
slider_position = Slider(axis_position, 'time', 0.1, 90.0)

axis_zoom = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor = slider_color)
slider_zoom = Slider(axis_zoom, 'zoom', 100, 1500)

# update() function to change the graph when the
# slider is in use
def update(val):
    pos = slider_position.val
    zoom = slider_zoom.val
    Axis.axis([pos, pos+10, -zoom, zoom])
    Plot.canvas.draw_idle()

# update function called using on_changed() function
slider_position.on_changed(update)
slider_zoom.on_changed(update)

# Display the plot
plt.show()