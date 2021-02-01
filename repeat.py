from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['timezone'] = 'US/Eastern'

groupname= ('MOT_abs',)
var_y_name=('Gaussian_height',)

# groupname= ('MOT_fluo',)
# var_y_name=('roi_fluo_img',)

# The last sequence is default if the selection is empty.
# Example: list(range(3,5))+[7,11]
my_idx=[575] 
font_size = 25
Do_scientific_notation = False

df = lyse.data()
index_name = 'run time'
index = df[index_name].values
y= df[groupname[0]][var_y_name[0]].values

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
y = y[this_idx]
index = index[this_idx]
plt.figure()
fig, ax = plt.subplots()

# bottom x axis
ax.plot(index, y)
xlim([index[0],index[-1]])
ax.set_ylabel(var_y_name[0])
ax.set_xlabel('Experiment #')
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
datefmt = mpl.dates.DateFormatter('%H:%M')
plt.gca().fmt_xdata = datefmt
plt.gca().xaxis.set_major_formatter(datefmt)
plt.xticks(rotation=45)

# Print texts
std_y = np.nanstd(y)
mean_y = np.nanmean(y)

if Do_scientific_notation:
    ax.text(0.1,0.2,
    """
    std: %.2e 
    mean: %.2e
    std/mean: %.3e """ %(std_y, mean_y, std_y/mean_y),transform=ax.transAxes)

else:
    ax.text(0.1,0.2,
    """
    std: %.2f 
    mean: %.2f
    std/mean: %.3f """ %(std_y, mean_y, std_y/mean_y),transform=ax.transAxes)


# top x axis: Experiment run number
ax2 = ax.twiny()  # instantiate a second axes that shares the same y-axis
color = 'tab:blue'
ax2.set_xlabel('Experiment #', color=color)  
x = np.arange(len(y))
xlim([x[0],x[-1]])
ax2.tick_params(axis='x', labelcolor=color)

plt.title("seq_index="+sequence_idx)
plt.rcParams.update({'font.size': font_size})
plt.subplots_adjust(left=0.2, right=0.9, top=0.7, bottom=0.2)

