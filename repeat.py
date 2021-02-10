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

groupname= ('MOT_abs','MOT_analysis',)
var_y_name=('Gaussian_height','MOT_repump_fluo',)

# groupname= ('MOT_abs',)
# var_y_name=('Gaussian_height',)

# groupname= ('MOT_fluo',)
# var_y_name=('roi_fluo_img',)

# The last sequence is default if the selection is empty.
# Example: list(range(3,5))+[7,11]
my_idx=[1] 
font_size = 17
Do_scientific_notation = False

df = lyse.data()
index_name = 'run time'
index = df[index_name].values

y = []
for ii in range(len(var_y_name)):
    y.append(df[groupname[ii]][var_y_name[ii]].values)

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
y = np.array(y)
y = y[:, this_idx]

index = index[this_idx]
plt.figure()

fig, ax = plt.subplots(1,len(var_y_name),figsize=(6*len(var_y_name),4)) # I cannot change the size of the figure window. It seems to be fixed by lyse.
if len(var_y_name)==1:  ax = [ax]

for ii in range(len(var_y_name)): 
    # bottom x axis
    ax[ii].plot(index, y[ii])
    xlim([index[0],index[-1]])
    ax[ii].set_ylabel(var_y_name[ii])
    ax[ii].xaxis.set_major_locator(plt.MaxNLocator(5))
    datefmt = mpl.dates.DateFormatter('%H:%M')
    ax[ii].fmt_xdata = datefmt
    ax[ii].xaxis.set_major_formatter(datefmt)
    plt.setp(ax[ii].xaxis.get_majorticklabels(),rotation=45)

    # Print texts
    std_y = np.nanstd(y[ii])
    mean_y = np.nanmean(y[ii])

    if Do_scientific_notation:
        ax[ii].text(0.1,0.2,
        """
        std: %.2e 
        mean: %.2e
        std/mean: %.3e """ %(std_y, mean_y, std_y/mean_y),transform=ax[ii].transAxes)

    else:
        ax[ii].text(0.1,0.2,
        """
        std: %.2f 
        mean: %.2f
        std/mean: %.3f """ %(std_y, mean_y, std_y/mean_y),transform=ax[ii].transAxes)

    
for ii in range(len(var_y_name)):    
    exec('ax'+str(ii+1)+ '= ax[ii].twiny()')  # instantiate a second axes that shares the same y-axis
    color = 'tab:blue'
    exec("ax"+str(ii+1)+".set_xlabel('Experiment #', color=color)") 
    x = np.arange(len(y[ii]))
    exec("ax"+str(ii+1)+".tick_params(axis='x', labelcolor=color)")
    exec("ax"+str(ii+1)+".set_xlim([x[0],x[-1]])")

    
plt.suptitle("seq_index="+sequence_idx)
plt.rcParams.update({'font.size': font_size})
plt.subplots_adjust(left=0.15, right=0.9, top=0.7, bottom=0.2)

