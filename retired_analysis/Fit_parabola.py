from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#var_x_name, var_y_name="MOT_quad_curr",('roi_fluo_img','a')
#var_x_name, var_y_name="MOT_cooling_freq",('roi_fluo_img','a')
var_x_name, var_y_name="MOT_B_bias_x",('roi_fluo_img','a')

# The last sequence is default if the selection is empty.
# Example: list(range(3,5))+[7,11]
my_idx=[6] 

font_size = 25

df = lyse.data()
groupname= ('MOT_fluo','MOT_fluo')

x = df[var_x_name]
y1= df[groupname[0]][var_y_name[0]]
x1 = x

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

fit = np.polyfit(x1,y1,4)
y_fit= fit[0]*x1**4+fit[1]*x1**3+fit[2]*x1**2+fit[3]*x1+fit[4]

plt.figure()
fig, ax1 = plt.subplots()

from scipy.optimize import minimize
def fun(x1):
    return -(fit[0]*x1**4+fit[1]*x1**3+fit[2]*x1**2+fit[3]*x1+fit[4])
fit_max=minimize(fun, (x1[np.argmax(y1)]), bounds=((min(x1),max(x1)),))

text_res = "max@x="+str(np.round(fit_max.x,3))
print(text_res)
ax1.text(0.1, 0.1, text_res,transform=ax1.transAxes)


ax1.plot(x1, y_fit, color='blue')
fit = [np.format_float_scientific(f,precision=1,sign=False) for f in fit]
ax1.scatter(x1,y1)

ax1.set_xlabel(var_x_name)
ax1.set_ylabel(var_y_name[0])
plt.title("seq_index="+sequence_idx)

fig.tight_layout()
plt.rcParams.update({'font.size': font_size})
