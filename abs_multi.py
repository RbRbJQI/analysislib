from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gaussian2d import *


df = lyse.data()
ct = []
wd = []
int_OD = []
t = []
mag_fluo = []
hold_time = []
sci_abs = []
fluo_OD = []
if_fit = True
for index, row in df.iterrows():
    file = row['filepath'].values[0]
    try:
        with h5py.File(file,'r') as h5_file:
            # t = df['t_of_f']
            # hold_time = df['hold_time']
            for groupname in h5_file['results']:
                resultsgroup = h5_file['results'][groupname]
                if groupname=='MOT_abs':
                    fluo_OD.append(h5_file['results'][groupname].attrs['fluo'])
                    if if_fit:
                        fp = h5_file['results'][groupname]['Gaussian_fit']
                        wd.append(fp[3])
                        ct.append([fp[0], fp[1]])
                        t.append(h5_file['globals'].attrs['t_of_f'])
                    # int_OD.append(h5_file['results'][groupname].attrs['int_OD'])
                # if groupname=='Science_abs':
                    # sci_abs.append(h5_file['results'][groupname].attrs['roi_OD'])
                    # fp = h5_file['results'][groupname]['Gaussian_fit']
                    # wd.append(fp[3])
                    # ct.append([fp[0], fp[1]])
    except Exception as e:
        wd.append(0)
        print('no results', e, file)
        continue
if if_fit:
    t, wd = np.array(t), np.array(wd)
    t = t*1e3
    # fp_exp = fitexpansion(wd**2, t)
    fp_exp = np.polyfit(t**2, wd**2, 1)
    # title = ' sig_0='+str(round(fp_exp[0]))+' v='+str(round(fp_exp[1]))
    title = ' sig_0='+str(round(sqrt(abs(fp_exp[1]))))+' v='+str((sqrt(fp_exp[0])))
    plt.figure('Gaussian width: '+title)
    plt.scatter(t, wd)
    # plt.plot(t, sqrt(expansion(fp_exp[0],fp_exp[1])(t)))
    plt.plot(t, sqrt(fp_exp[0]*t**2+fp_exp[1]))
    
    ct = np.array(ct)
    y = ct[:,0]*5.3*1e-3
    fp_fall = np.polyfit(t, y, 2)
    plt.figure('falling'+str(fp_fall))
    plt.scatter(t, y)
    plt.plot(t, fp_fall[0]*t**2+fp_fall[1]*t+fp_fall[2])
    plt.title('g='+str(round(fp_fall[0]*2e3,3))+'m/s^2')
    plt.xlabel('t_of_f(ms)')
    plt.ylabel('y(mm)')


# int_OD = np.array(int_OD)
# wd = np.array(wd)
# idx=np.argwhere((int_OD>0.25))#&(wd<58.5))
# print(idx, int_OD[idx])
# print(wd[idx])
# plt.figure('integrated OD')
# plt.plot(int_OD)
# plt.figure('OD/width y')
# # plt.plot(int_OD/wd)
# plt.figure('width y')
# plt.plot(wd)

# hold_time, fluo_OD, sci_abs = np.array(hold_time), np.array(fluo_OD), np.array(sci_abs)
# ef = np.polyfit(np.array(hold_time), np.log(np.array(sci_abs)/np.array(fluo_OD)), 1)
# efit = np.exp(ef[0]*hold_time+ef[1])
# plt.figure('lifetime:    '+str(-1/ef[0]))
# plt.plot(hold_time, efit)
# plt.scatter(hold_time, np.array(sci_abs)/np.array(fluo_OD))