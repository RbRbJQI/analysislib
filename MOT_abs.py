from __future__ import division
from lyse import *
from pylab import *
from analysislib.common import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from gaussian2d import *
import matplotlib.patches as patches

for j in ['A','B','C']:
	for i in range(1,5):
		for k in ['+','-']:print(str(i)+j+k)

def get_images(orientation):
    atom = run.get_image(orientation=orientation, label = 'abs_img', image='atom')
    probe = run.get_image(orientation=orientation, label = 'abs_img', image='probe')
    try:
        bg = run.get_image(orientation=orientation, label = 'abs_img', image='bg')
        atom = atom.astype(float)
        probe = probe.astype(float)
        bg = bg.astype(float)
        atom = np.copy(atom - bg)
        probe = np.copy(probe - bg)
    except Exception as e:
        print('no bg \n', e)
    fluo = []
    try:
        fluo = run.get_image(orientation='xz', label = 'MOT_fluo_img', image='fluo_img')
    except:
        print('no fluo')
    return np.array(atom), np.array(probe), np.array(fluo)
def avg_image(a):
    #bgr = np.mean(a[-100:-1,-100:-1])
    bgr = 20
    # for i in range(np.shape(a)[0]):
        # for j in range(np.shape(a)[1]):
            # if a[i][j]<=0:
                # try:
                    # a_neigh = np.array([a[i+1][j], a[i-1][j], a[i][j+1], a[i][j-1], a[i-1][j-1], a[i+1][j-1]])
                    # a_neigh = a_neigh[a_neigh>0]
                    # a[i][j] = np.copy( np.mean(a_neigh) )
                # except:
                    # a[i][j] = bgr
    a[where(a<=bgr)] = bgr
    
    return a
def show_img(name, a, l_scale = 0, h_scale=4096):
    # plt.figure(name)
    plt.imshow(a) # IBS: use the "extent" kwarg to set the scale in real units rather than pixels.
    
    # if type(h_scale)==int:
        # if type(l_scale)==int:
            # plt.clim(l_scale,h_scale)
        # else:
            # plt.clim(0,h_scale)
    # else:
        # if type(l_scale)==int:
            # plt.clim(l_scale,np.max(a))
    plt.clim(l_scale,h_scale)
    plt.colorbar()
    
df = data(path)
run = Run(path)
atom, probe, fluo = get_images(df['probe_direction'].upper())
atom, probe = [avg_image(img) for img in [atom, probe]]

OD = -np.log(np.divide(atom, probe))

if df['probe_direction']=='xy': 
    ct = [265,307]
else:
    ct=[285,158]
import cv2
mask = np.zeros(OD.shape, dtype=np.uint8)
mask = cv2.circle(mask, tuple(ct), 150, 1, -1)
# OD = np.multiply(OD, mask)

int_OD = np.mean(OD)
fluo_OD = np.mean(fluo)
if not np.isnan(fluo_OD):
    run.save_result('fluo', fluo_OD)
    plt.figure('fluo_img')
    plt.imshow(fluo)

print('int_OD: ',int_OD)
run.save_result('int_OD', int_OD)
plt.figure('img')
fig, (ax1, ax2, ax3)=plt.subplots(3,1)
# plt.subplot(311)
probe_name = ax1.imshow(probe)
plt.colorbar(probe_name, ax=ax1)
# show_img('probe', probe)
# plt.subplot(312)
# show_img('atom', atom)
atom_name = ax2.imshow(atom)
plt.colorbar(atom_name, ax=ax2)
# plt.subplot(313)
OD_name = ax3.imshow(OD)
# show_img('OD', OD, h_scale=0.5)
OD_name.set_clim(0, 1)
plt.colorbar(OD_name,ax=ax3)
circle = patches.Circle((289.3,296.5),138, fill=None, edgecolor='r')
ax3.add_patch(circle)
# plt.title('probe_t='+str(round(df['t_tran_probe'],2))+'s')
try:
    # if int_OD>0.007:
    fp = fitgaussian2d(OD, ct)
    if np.isnan(fp[0])==False:
        # plt.contour(gaussian(fp[0],fp[1],fp[2],fp[3],fp[4],fp[5])(*np.indices(np.shape(OD))), levels=[0.1,0.5])
        plt.figure('sda')
        plt.imshow(OD)
        # plt.clim(0,2)
        # plt.contour(gaussian(fp[0],fp[1],fp[2],fp[3],fp[4],fp[5])(*np.indices(np.shape(OD))))
        print('fit: ',fp)
        checkfit(OD, fp)
        run.save_result_array('Gaussian_fit', fp)
        fp[0:4] = [int(f) for f in fp[0:4]]

        plt.text(0.95, 0.05, """
        x : %.1f
        y : %.1f
        width_x : %.1f
        width_y : %.1f""" %(fp[0], fp[1], fp[2], fp[3]),
                fontsize=8, horizontalalignment='right',
                verticalalignment='bottom')#, transform=ax.transAxes)
        x0, y0 = [158, 272]
        # fp[0:2] = x0, y0
        crop = 175#int(fp[3]/2)
        roi_OD = np.sum(OD[int(fp[0]-crop):int(fp[0]+crop), int(fp[1]-crop):int(fp[1]+crop)])
        gaussian_int = fp[4] *2* 3.14159*(fp[2]*fp[3])#+fp[5]*w*h
        # run.save_result('roi_OD', roi_OD)
        run.save_result('roi_OD', gaussian_int)
       
        
        if fp[4]>0:
            run.save_result('Gaussian_width_x', fp[2])
            run.save_result('Gaussian_height', fp[4])
            
        else:
            run.save_result('Gaussian_width_x', np.nan)
            run.save_result('Gaussian_height', np.nan)
        print('roi_OD=',roi_OD)
        print('Gaussian_height=',fp[4])
        # print('life: ',roi_OD/fluo_OD)
        # run.save_result('optimized_OD',np.sqrt(fluo_OD)*roi_OD)
    else:
        run.save_result('roi_OD', 0)
        run.save_result('Gaussian_height', 0)
        # run.save_result('optimized_OD',np.sqrt(fluo_OD)*roi_OD)     
# else:
    # run.save_result('roi_OD', np.nan)
    # run.save_result('Gaussian_height', np.nan)
    # run.save_result('Gaussian_width_x', np.nan)
    # run.save_result('optimized_OD',np.sqrt(fluo_OD)*roi_OD)

except Exception as e:
    print('Error::::::::::::::'+str(e))