from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = lyse.data()
# groupname=('temperature', 'MOT_fluo')
# groupname= ('MOT_fluo','MOT_fluo')
groupname=('MOT_abs',)
# var_x_name, var_y_name="t_of_f",'Gaussian_center_y'
var_x_name, var_y_name="hold_time_com",('roi_fluo_img','a')
# var_x_name, var_y_name="repump_freq",('roi_fluo_img','roi_MOT_fluo_img')
# var_x_name, var_y_name="dur_probe_coils",('roi_OD','a')
# var_x_name, var_y_name="load_time",('roi_fluo_img','final_current')
# var_x_name, var_y_name="t_of_f",'roi_OD'
# var_x_name, var_y_name="hold_time_com",'Gaussian_height'
# var_x_name, var_y_name="hold_time_com",('temperature', 'Gaussian_width_x')
# var_x_name, var_y_name="quad_trap",'temperature'
x = df[var_x_name]
y1= df[groupname[0]][var_y_name[0]]
# y3= df[groupname[0]]['roi_MOT_fluo_img']#[0:10]
x1 = x
# y2= df[groupname[1]][var_y_name[1]]


# print(x)

# x, y1, y2 = np.array(x), np.array(y1), np.array(y2)
# ind_nan = np.argwhere(np.isnan(y1))
# x1, y1, y2 = np.delete(x, ind_nan), np.delete(y1, ind_nan), y2#np.delete(y2, ind_nan) 
x1, y1 = np.array(x1), np.array(y1)
# y2,y3 = np.array(y2), np.array(y3)
# x1, y1 = x1[np.argsort(x1)], y1[[np.argsort(x1)]]
# print(x1, y1)
# fit = np.polyfit(x, y, 2)
from scipy.optimize import curve_fit
def expfunc(x, a,b,c):
    return a*np.exp(-x/b) + 1*c
def print_expfunc(x, a,b,c):
    return 'y='+str(a)+ '*exp(-'+str(x)+'/' + str(b)+ ')+'+str(c)
def fake_expfunc(x, a,b,c):
    return a*np.exp(-x/b) / ( 1+c*a*b*(1-np.exp(-x/b)) )
# print(y1,y2,y3)
fit, cov = curve_fit(expfunc, x1, y1, [1e8, 1e2, 0e7])#[-2.8e8,1.5,2.8e8])
plt.figure()
fig, ax1 = plt.subplots()
x_unit='()'
y_unit= ('()', '(A)')
x1=np.arange(len(y1))
# ax1.plot(x1, expfunc(x1, *fit), color='blue')
fit = [np.format_float_scientific(f,precision=3,sign=False) for f in fit]
# ax1.scatter(x1,y1, label=var_y_name[0]+' : '+ print_expfunc('t', *fit), color='blue')
ax1.scatter(x1,y1, color='blue')
# ax1.scatter(x1,y1, label=var_y_name[0], color='blue')
# ax1.scatter(x1,y3, label='MOT_fluo', color='green')
lplot = ax1.set_xlabel(var_x_name+x_unit)
# ax1.set_ylabel(var_y_name[0]+y_unit[0])
ax1.set_ylabel('roi_fluo'+y_unit[0])
try: 
    # x2= x[17:]+
    # y2 = df[groupname[0]][var_y_name[0]][17:]
    x2, y2 = np.array(x2), np.array(y2)
    x2, y2 = x2[np.argsort(x2)], y2[[np.argsort(x2)]]
    fit2, cov2 = curve_fit(expfunc, x2, y2, [3e7, 1e3, 0])#[-2.8e8,1.5,2.8e8])
    ax1.plot(x2, expfunc(x2, *fit2), color='red')
    fit2 = [np.format_float_scientific(f,precision=3,sign=False) for f in fit2]
    ax1.scatter(x2,y2, label=var_y_name[0]+': '+ print_expfunc('t', *fit2), color='red')
    # ax1.scatter(x2,y2, label=var_y_name[0]+' UV at quad trap: '+ print_expfunc('t', *fit2), color='red')
except: 
    pass
# ax1.legend(loc='best')
plt.title(var_x_name+" measurement")#'y='+str(fit[0])+ '*exp(-t/' + str(fit[1])+ ')+'+str(fit[2]))

# ax2 = ax1.twinx()
# # rplot = ax2.scatter(x2,y2,label=var_y_name[0]+'UV', color='red')
# rplot = ax2.scatter(x1,y2,label='MOT', color='red')
# ax2.plot(x1,y2, color='red')
# ax2.set_ylabel(var_y_name[1]+y_unit[1])
# ax2.legend(loc='lower left')
# fig.tight_layout()

# plt.title('x0='+str(-fit[1]/2/fit[0]))
# pixel_size=5.3e-6

# plt.title('M='+str(2*fit[0]*pixel_size/9.8))
# plt.plot(x,fit[0]*x**2+fit[1]*x+fit[2])