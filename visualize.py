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
t0 = min([min(ecg_t), min(acc_t), min(hr_t)])
ecg_t = ecg_t - t0
acc_t = acc_t - t0
hr_t = hr_t - t0
t_max = max([max(ecg_t), max(acc_t), max(hr_t)])
plt.show()

min_acc=np.min(np.min(acc))
max_acc=np.max(np.max(acc))



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
# https://www.statology.org/matplotlib-two-y-axes/
plt.close('all')

# create a figure with subplots and a specified figure size with fixed dpi
fig, ax = plt.subplots(nrows=2, figsize=(19, 9.5), dpi=90)
ax[0].plot(ecg_t, ecg, color='blue', label='ECG')
ax[0].set_ylabel('electrocardiogram [micro-Volt]', color='blue')#, fontsize=14)
ax[0].set_xticklabels([]) # remove x-axis label and ticks

# create second y-axis
ax2 = ax[0].twinx()
l2 = ax2.plot(hr_t, hr[:,0], color='green', label='HR')
l2 = ax2.plot(hr_t, 60*1000/hr[:,1], color='grey', label='instant HR from RR')
ax2.set_ylabel('heart rate [bpm]', color='green')#, fontsize=14)
ax2.legend()

ax[1].plot(acc_t, acc)
ax[1].set_xlabel('time [s]')#, fontsize=14)
ax[1].set_ylabel('acceleration [micro-g]')#, fontsize=14)

# adjust the margins to save space
# add enough margin to the bottom to allow for sliders
fig.tight_layout(pad=0.0)
fig.subplots_adjust(bottom=0.125, left=0.05, right=0.96, top=0.99)

slider_color = 'White'
# Set the axis and slider position in the plot
axis_position = plt.axes([0.05, 0.05, 0.9, 0.03], facecolor = slider_color)
slider_position = Slider(axis_position, 'time', 0.0, t_max)

axis_t_range = plt.axes([0.05, 0.02, 0.45, 0.03], facecolor = slider_color)
slider_t_range = Slider(axis_t_range, 'time-range', 1, 0.5*t_max)

#axis_zoom = plt.axis([0.72, 0.05, 0.25, 0.03], facecolor = slider_color)
#slider_scale_y = Slider(axis_zoom, 'scale y', 1, 4)

# update() function to change the graph when the slider is changed
def update(val):
    global ax
    pos = slider_position.val
    t_range = slider_t_range.val    
    scale_y = 1
    #scale_y = slider_scale_y.val
    t1 = pos - t_range
    t2 = pos + t_range
    #if t1<0: t1=0
    ax[0].axis([t1, t2, min(ecg)/scale_y, max(ecg)/scale_y])
    ax[1].axis([t1, t2, min_acc, max_acc])
    Plot.canvas.draw_idle()

# update function called using on_changed() function
slider_position.on_changed(update)
slider_t_range.on_changed(update)
#slider_scale_y.on_changed(update)

# Display the plot
plt.show()