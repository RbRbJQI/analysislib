from __future__ import division
from lyse import *
from pylab import *
from analysislib.common import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from gaussian2d import *

def get_images():
    atom = run.get_image(orientation='science', label = 'science_img', image='atom')
    probe = run.get_image(orientation='science', label = 'science_img', image='probe')
    try:
        bg = run.get_image(orientation='science', label = 'science_img', image='bg')
        atom = atom.astype(float)
        probe = probe.astype(float)
        bg = bg.astype(float)
        atom = np.copy(atom - bg)
        probe = np.copy(probe - bg)
    except Exception as e:
        print('no bg \n', e)
    fluo = []
    try:
        fluo = run.get_image(orientation='YZ', label = 'MOT_fluo_img', image='fluo_img')
    except:
        print('no fluo')
    return np.array(atom), np.array(probe), np.array(fluo)
def avg_image(a):
    #bgr = np.mean(a[-100:-1,-100:-1])
    bgr = 50
    # for i in range(np.shape(a)[0]):
        # for j in range(np.shape(a)[1]):
            # if a[i][j]<=0:
                # try:
                    # a_neigh = np.array([a[i+1][j], a[i-1][j], a[i][j+1], a[i][j-1], a[i-1][j-1], a[i+1][j-1]])
                    # a_neigh = a_neigh[a_neigh>0]
                    # a[i][j] = np.copy( np.mean(a_neigh) )
                # except:
                    # a[i][j] = bgr
    a[where(a<bgr)] = bgr
    
    return a
def show_img(name, a, l_scale = 0, h_scale=4095):
    # plt.figure(name)
    plt.imshow(a)
    
    if type(h_scale)==int:
        if type(l_scale)==int:
            plt.clim(l_scale,h_scale)
        else:
            plt.clim(0,h_scale)
    else:
        if type(l_scale)==int:
            plt.clim(l_scale,h_scale)#np.max(a))
    plt.colorbar()
    
df = data()
run = Run(path)
atom, probe, fluo = get_images()
atom, probe = [avg_image(img) for img in [atom, probe]]

OD = -np.log(np.divide(atom, probe))
int_OD = np.mean(OD[150:380,200:400])
# plt.figure('sda')
# plt.imshow(OD[150:380,200:400])
# plt.clim(0,1)
run.save_result('int_OD', int_OD)
# plt.figure('MOT_fluo')
# plt.imshow(fluo)
plt.figure('science')
plt.subplot(311)
show_img('probe', probe)
plt.subplot(312)
show_img('atom', atom)
plt.subplot(313)
show_img('OD', OD, h_scale=0.5)
try:
    # if int_OD>0.02:
    fp = fitgaussian2d(OD, [234,290])
    plt.contour(gaussian(fp[0],fp[1],fp[2],fp[3],fp[4],fp[5])(*np.indices(np.shape(OD))), levels=[0.1,0.5])
    print('fit: ',fp)
    if 0<fp[0]<OD.shape[0] and 0<fp[1]<OD.shape[1]:
        checkfit(OD, fp)
        run.save_result_array('Gaussian_fit', fp)
        fp = [int(f) for f in fp]
        crop = 50#int(fp[3]/2)
        pcrop = 10
        roi_OD = np.sum(OD[(fp[0]-crop):(fp[0]+crop), (fp[1]-crop):(fp[1]+crop)])
        peak_OD = np.mean(OD[(fp[0]-pcrop):(fp[0]+pcrop), (fp[1]-pcrop):(fp[1]+pcrop)])
        run.save_result('roi_OD', roi_OD)
        run.save_result('Gaussian_width_x', fp[2])
        run.save_result('Gaussian_width_y', fp[3])
        # run.save_result('peak_OD', peak_OD)
        run.save_result('center_x', fp[0])
        run.save_result('center_y', fp[1])
        print(roi_OD)
        plt.text(0.95, 0.05, """
        x : %.1f
        y : %.1f
        width_x : %.1f
        width_y : %.1f""" %(fp[0], fp[1], fp[2], fp[3]),
                fontsize=8, horizontalalignment='right',
                verticalalignment='bottom')#, transform=ax.transAxes)
    else:
        roi_OD, peak_OD=0,0
except Exception as e:
    print('Error::::::::::::::'+e)
# print(df['MOT_abs','Gaussian_fit'])
#plt.savefig('C:/Users/RbRb/Desktop/'+str(time.time())+'.png')