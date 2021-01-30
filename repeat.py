from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

groupname= ('MOT_abs',)
var_y_name=('Gaussian_height',)
# The last sequence is default if the selection is empty.
# Example: list(range(3,5))+[7,11]
my_idx=[15] 
font_size = 25

df = lyse.data()
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
plt.figure()
fig, ax = plt.subplots()

x = np.arange(len(y))
ax.plot(x, y)

std_y = np.nanstd(y)
mean_y = np.nanmean(y)

ax.text(0.1,0.2,"""std: %.2f 
mean: %.2f
std/mean: %.3f """ %(std_y, mean_y, std_y/mean_y),transform=ax.transAxes)
ax.set_ylabel(var_y_name[0])
ax.set_xlabel('Experiment #')
plt.title("seq_index="+sequence_idx)
plt.rcParams.update({'font.size': font_size})
plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)

