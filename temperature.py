from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gaussian2d import *

cross_section0 = 1.3e-9*1e-4
kB = 1.38e-23
mRb = 1.443e-25
h = 6.63e-34

threshold = 0.0017
df = lyse.data()
# groupname='MOT_abs'
groupname='Science_abs'
# groupname='MOT_fluo'
var_x_name, var_y_name="t_of_f",'Gaussian_width_y'
x0 = df[var_x_name]
y0=df[groupname][var_y_name]
mag_r = 1/0.4#1/0.226#df['']
print(mag_r)


ind = 0
while ind<len(x0)-1:
    x, y = [], []
    start_ind = ind
    while True:
        if not np.isnan(y0[ind]):
            x.append(x0[ind])
            y.append(y0[ind])
        if ind>=len(x0)-1: break
        elif x0[ind]>x0[ind+1]: break
        ind+=1
    # print(x,y)
    # print()
    if ind>=len(x0)-1 and x0[ind]<threshold:   
        run = lyse.Run(df['filepath'][ind])
        run.save_result('PSD', np.nan)
        run.save_result('temperature', np.nan)
        break
    ind += 1
    if ind<len(x0):
        continue
    print(x,y)
    x, y = np.array(x)*1e3, np.array(y)*5.3*1e-3*mag_r
    try:
        fp_fall = np.polyfit(x**2, y**2, 1)
        plt.figure('temp')

        v = sqrt(fp_fall[0])
        width0 = sqrt(fp_fall[1])
        plt.plot(x, np.sqrt(fp_fall[0]*x**2+fp_fall[1]), label="v="+str(v) )
        # plt.legend()

        T = mRb*v**2/kB
        plt.title('T='+str(round(T*1e6,2))+'uK')

        x_unit='(ms)'
        y_unit='(mm)'
        plt.scatter(x,y)
        plt.xlabel(var_x_name+x_unit)
        plt.ylabel(var_y_name+y_unit)
        run = lyse.Run(df['filepath'][ind-1])
        run.save_result('temperature', round(T*1e6,2))
        
        # print(width0)
        n0 = df[groupname]['Gaussian_height'][start_ind]/(width0*1e-3)/cross_section0*sqrt(pi) #*?sqrt(2*pi)?
        # print(n0*1e-9)
        thermal_lambda = h/sqrt(2*3.14*mRb*kB*T)
        PSD = n0*thermal_lambda**3
        print(PSD)
        run.save_result('PSD', PSD)
        if np.isnan(PSD): run.save_result('PSD', -1)
    except:
        run = lyse.Run(df['filepath'][ind-1])
        run.save_result('PSD', -1)
        run.save_result('temperature', 9999)
    