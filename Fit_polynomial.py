from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# groupname= ('MOT_fluo',)
groupname= ('MOT_abs',)

# var_x_name, var_y_name=('MOT_quad_curr',),('roi_fluo_img',)
# var_x_name, var_y_name=('MOT_cooling_freq',),('gaussian_int',)
# var_x_name, var_y_name=('molasses_duration','molasses_duration'),('Gaussian_width_x','Gaussian_width_y')
# var_x_name, var_y_name=('quad_trap_B_bias_end_z','quad_trap_B_bias_end_z'),('PSD_singleshot','Distance_to_center')
var_x_name, var_y_name=('probe_science_repump_freq',),('gaussian_int',)

# The last sequence is default if the selection is empty.
# Example: list(range(3,5))+[7,11]
my_idx=[48] 
n_order = 4 
font_size = 20
find_max = [True] # Match the size of this list with len(var_y_name)

df = lyse.data()
x,y = [], []
for ii in range(len(var_y_name)):
    x.append(df[var_x_name[ii]].values)
    y.append(df[groupname[0]][var_y_name[ii]].values)

if my_idx==[]:
    this_idx = np.argwhere(df["sequence_index"].values==df["sequence_index"][-1]).flatten()
    my_idx = df["sequence_index"][-1]
else:
    this_idx=[]
    for iidx in my_idx:
        this_temp_idx = np.argwhere(df["sequence_index"].values==iidx).flatten()
        this_idx = np.append(this_idx, this_temp_idx)
sequence_idx=str(my_idx)
x, y = np.array(x), np.array(y)
this_idx=this_idx.astype(int)
x, y = x[:, this_idx], y[:, this_idx]

for ii in range(len(var_y_name)):
    sort_idx = np.argsort(x[ii])
    x[ii], y[ii] = x[ii,sort_idx], y[ii,sort_idx]

fig, axes = plt.subplots(1,len(var_y_name),figsize=(6*len(var_y_name),4)) # I cannot change the size of the figure window. It seems to be fixed by lyse.
if len(var_y_name)==1:  axes = [axes]

# plot data 
for ii in range(len(var_y_name)):
    axes[ii].scatter(x[ii],y[ii])

def fit_func(x, *coeffs):
    y = np.polyval(coeffs, x)
    return y

for ii in range(len(var_y_name)): 
    p0 = np.ones(n_order) 
    popt, pcov = curve_fit(fit_func, x[ii], y[ii], p0=p0)
    xx = np.linspace(min(x[ii]), max(x[ii]), 5000)
    yy = fit_func(xx, *popt)

    axes[ii].plot(xx, yy)
    if find_max[ii]:
        max_idx = np.argmax(yy)
    else:
        max_idx = np.argmin(yy)
    max_x = xx[max_idx]
    print_text = "Fit to " + str(n_order) + "th poly order \nPeak @ x = " + str(np.round(max_x,3))
    axes[ii].text(0.1, 0.1, print_text , transform=axes[ii].transAxes)

    axes[ii].set_xlabel(var_x_name[ii])
    axes[ii].set_ylabel(var_y_name[ii])

plt.suptitle("seq_index="+sequence_idx)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
fig.tight_layout()
plt.rcParams.update({'font.size': font_size})

