from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

groupname= ('MOT_fluo',)

# var_x_name, var_y_name=('MOT_quad_curr',),('roi_fluo_img',)
# var_x_name, var_y_name=('MOT_cooling_freq',),('gaussian_int',)
var_x_name, var_y_name=('molasses_cooling_freq_start',),('Gaussian_width_x',)
# var_x_name, var_y_name=('CMOT_cooling_freq_start',),('roi_fluo_img',)

# The last sequence is default if the selection is empty.
# Example: list(range(3,5))+[7,11]
my_idx=[54] 
n_order = 4 
font_size = 25
find_max =  False

df = lyse.data()


x1 = df[var_x_name[0]]
y1= df[groupname[0]][var_y_name[0]]

if my_idx==[]:
    this_idx = np.argwhere(df["sequence_index"].values==df["sequence_index"][-1]).flatten()
    my_idx = df["sequence_index"][-1]
else:
    this_idx=[]
    for iidx in my_idx:
        this_temp_idx = np.argwhere(df["sequence_index"].values==iidx).flatten()
        this_idx = np.append(this_idx, this_temp_idx)
sequence_idx=str(my_idx)

this_idx=this_idx.astype(int)
x1, y1 = x1[this_idx], y1[this_idx]
x1, y1 = np.array(x1), np.array(y1)
sort_idx = np.argsort(x1)
x1, y1 = x1[sort_idx], y1[sort_idx]

plt.figure()
fig, ax1 = plt.subplots()
# plot data
ax1.scatter(x1,y1)

def fit_func(x, *coeffs):
    y = np.polyval(coeffs, x)
    return y
 
p0 = np.ones(n_order) 
popt, pcov = curve_fit(fit_func, x1, y1, p0=p0)
xx = np.linspace(min(x1), max(x1), 5000)
yy = fit_func(xx, *popt)
ax1.plot(xx, yy)
if find_max:
    max_idx = np.argmax(yy)
else:
    max_idx = np.argmin(yy)
max_x = xx[max_idx]
print_text = "Fit to " + str(n_order) + "th poly order \nPeak @ x = " + str(np.round(max_x,3))
ax1.text(0.1, 0.1, print_text , transform=ax1.transAxes)

ax1.set_xlabel(var_x_name[0])
ax1.set_ylabel(var_y_name[0])
plt.title("seq_index="+sequence_idx)

fig.tight_layout()
plt.rcParams.update({'font.size': font_size})
