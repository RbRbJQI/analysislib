from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gaussian2d import *

pipe_D= (138*2)*5.3e-3
mag_r = 9.525/pipe_D
# mag_r = 1/0.226
print(mag_r)

length = 20
len_data_group=5
num_group=round(length/len_data_group)

df = lyse.data()
groupname='MOT_fluo'
var_name='hold_time_start'
var_x_name, var_y_name, var_y2_name="t_of_f",'Gaussian_width_x', 'roi_fluo_img'
x0 = df[var_x_name]
y0=df[groupname][var_y_name]
y2=df[groupname][var_y2_name]


x=df[var_name]
x=np.array(x[-length:])

x0=np.array(x0[-length:])
y0=np.array(y0[-length:])
y2=np.array(y2[-length:])

# print(x)
dataset=np.column_stack((x,x0,y0,y2))
print(dataset)
dataset=dataset[np.argsort(dataset[:,0])]
print(dataset)
# print(dataset)

x_list=dataset[0:-1:len_data_group,0]
T_list=[]
ROI_list=[]
plt.figure(1)
for num in range(num_group):
    xx, yy, y2y2 = np.array(dataset[num*len_data_group:(num+1)*len_data_group,1])*1e3, np.array(dataset[num*len_data_group:(num+1)*len_data_group,2])*5.3*1e-3*mag_r, np.array(dataset[num*len_data_group:(num+1)*len_data_group,3])
    idx = np.isfinite(xx) & np.isfinite(yy)
    print(idx)
    print(xx)
    print(yy)
    ROI_mean=np.mean(y2y2[idx])
    ROI_max=np.max(y2y2[idx])
    # ROI_list.append(ROI_mean)
    ROI_list.append(ROI_max)
    fp_fall = np.polyfit(xx[idx]**2, yy[idx]**2, 1)
    # plt.figure(num)
    xy=np.column_stack((xx,yy))
    xy=xy[np.argsort(xy[:,0])]
    v = sqrt(fp_fall[0])
    plt.plot(xy[:,0], np.sqrt(fp_fall[0]*xy[:,0]**2+fp_fall[1]), label="v="+str(v) )
    plt.legend()

    kB = 1.38e-23
    mRb = 1.443e-25
    T = mRb*v**2/kB
    plt.title('T='+str(round(T*1e6,2))+'uK')

    x_unit='()'
    y_unit='(mm)'
    plt.scatter(xx,yy)
    plt.xlabel(var_x_name+x_unit)
    plt.ylabel(var_y_name+y_unit)
    T_list.append(T)
    # run = lyse.Run(df['filepath'][ind-1])
    # run.save_result('temperature', round(T*1e6,2))
plt.show()
x_unit='(ms)'
y_unit='(uK)'
y2_unit='()'

plt.figure(var_name+'~'+'T')
fig, ax1 = plt.subplots()
lplot = ax1.set_xlabel(var_name+x_unit)
ax1.set_ylabel('T'+y_unit)
x, y = np.array(x_list), np.array(T_list)*1e6
ax1.scatter(x, y, label='temperature', color='blue')  
ax1.legend(loc='center left')


ax2 = ax1.twinx()
rplot = ax2.scatter(x_list,ROI_list,label='Count', color='red')
ax2.set_ylabel('count'+y2_unit[1])
ax2.legend(loc='center right')
fig.tight_layout()