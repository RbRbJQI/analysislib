from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

groupname= ('MOT_fluo',)

var_x_name, var_y_name=("MOT_load_time",),('roi_fluo_img',)
# var_x_name, var_y_name=('quad_trap_hold_time',),('roi_fluo_img',)

# The last sequence is default if the selection is empty.
# Example: list(range(3,5))+[7,11]
my_idx=[64] 
fix_long_time_value=0 # choose 1 if the exponential decays to 0

font_size = 15

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


from scipy.optimize import curve_fit
def expfunc(x, a,b,c):
    return a*np.exp(-x/b) + c
def print_expfunc(x, a,b,c):
    return 'y='+str(a)+ '*exp(-'+str(x)+'/' + str(b)+ ')+'+str(c)
def fake_expfunc(x, a,b,c):
    return a*np.exp(-x/b) / ( 1+c*a*b*(1-np.exp(-x/b)) )

from uncertainties import ufloat
if fix_long_time_value:
    c_fixed=0
    fit, cov = curve_fit(lambda x, a, b: expfunc(x, a, b, c_fixed), x1, y1, [100e6, 10e3])
    sigma_ab = np.sqrt(np.diagonal(cov))
    fit=np.append(fit,[c_fixed])
    a = ufloat(fit[0], sigma_ab[0])
    b = ufloat(fit[1], sigma_ab[1])
else:
    fit, cov = curve_fit(expfunc, x1, y1, [-80e6, 5, 1e7])
    sigma_ab = np.sqrt(np.diagonal(cov))
    a = ufloat(fit[2], sigma_ab[2])
    b = ufloat(fit[1], sigma_ab[1])
    
plt.figure()
fig, ax1 = plt.subplots()


# print fit confidence interval
text_res = "Best fit parameters:\n" r"$N_0$" "= {}\n" r"$\tau$" "= {}".format(a, b)
ax1.text(0.5, 0.5, text_res,transform=ax1.transAxes)


ax1.plot(x1, expfunc(x1, *fit), color='blue')
fit = [np.format_float_scientific(f,precision=1,sign=False) for f in fit]
ax1.scatter(x1,y1, label=print_expfunc('t', *fit), color='blue')


ax1.set_xlabel(var_x_name[0])
ax1.set_ylabel(var_y_name[0])
ax1.legend(loc='lower right')
plt.title("seq_index="+sequence_idx)
fig.tight_layout()
plt.rcParams.update({'font.size': font_size})