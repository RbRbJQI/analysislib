from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import smoothfit

df = lyse.data()
groupname= ('MOT_fluo','a')

var_y_name=('gaussian_int','a')

y1= df[groupname[0]][var_y_name[0]].values

#########################################  Select your sequence indices here ############################################
my_idx=[] # The last sequence is default if the selection is empty.
if my_idx==[]:
    this_idx = np.argwhere(df["sequence_index"].values==df["sequence_index"][-1]).flatten()
    my_idx = df["sequence_index"][-1]
else:
    this_idx=[]
    for iidx in my_idx:
        this_temp_idx = np.argwhere(df["sequence_index"].values==iidx).flatten()
        this_idx = np.append(this_idx, this_temp_idx)
sequence_idx=str(my_idx)
print('last sequnce index= ',df["sequence_index"][-1])
this_idx=this_idx.astype(int)
# x1 = x1[this_idx]
y1 = y1[this_idx]
plt.figure()
fig, ax1 = plt.subplots()

x1 = np.arange(len(y1))
# u = smoothfit.fit1d(x1, y1, 0, np.max(x1), 1000, degree=1, lmbda=1e-5)
# y_fit = u(x1)

ax1.plot(x1, y1)
# ax1.plot(x1, y_fit)

std_y = np.format_float_scientific(np.std(y1),precision=2,sign=False)
avg_y = np.format_float_scientific(np.average(y1),precision=2,sign=False)

ax1.text(0.6,0.2,"std:"+str(std_y)+"\navg:"+str(avg_y)+'\nfluctuation: '+str(round(np.std(y1)/np.average(y1)*100,2) ) + '%',transform=ax1.transAxes)
plt.rcParams.update({'font.size': 26})

