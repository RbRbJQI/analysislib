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

def probe_mask( point, center, radius ):
    x0,y0=center[0],center[1]
    x,y=point[0],point[1]
    if(np.sqrt((x-x0)**2+(y-y0)**2)>radius):
        return 0
    else:
        return 1

def get_images():
    fluo = run.get_image(orientation='XZ', label = 'fluo_img', image='fluo_img')
    orig_fluo = np.copy(fluo)
    try:
        bg = run.get_image(orientation='XZ', label = 'fluo_img', image='bg')
        fluo = fluo.astype(float)
        bg = bg.astype(float)
        fluo = np.copy(fluo - bg)
    except Exception as e:
        print('no bg \n', e)
    return np.array(fluo), np.array(orig_fluo)
    
def get_MOT_images():
    fluo_MOT = run.get_image(orientation='YZ', label = 'MOT_fluo_img', image='fluo_img')
    try:
        bg = run.get_image(orientation='YZ', label = 'fluo_img', image='bg')
        fluo_MOT = fluo_MOT.astype(float)
        bg = bg.astype(float)
        fluo_MOT = np.copy(fluo_MOT - bg)
    except Exception as e:
        print('no MOT fluo or no bg \n', e)
    return np.array(fluo_MOT)
   
def show_img(name, a, l_scale = 0, h_scale=4096):
    # plt.figure(name)
    plt.imshow(a) # IBS: use the "extent" kwarg to set the scale in real units rather than pixels.
    
    plt.clim(l_scale,h_scale)
    plt.colorbar()
    
print(path)
df = data(path)
run = Run(path)
fluo_img, orig_fluo = get_images()
# MOT_fluo_img = get_MOT_images()



plt.figure('fluo_img')

fig, (ax1, ax2)=plt.subplots(1,2)
# plt.subplot(122)
orig_fluo_name=ax2.imshow(orig_fluo)
orig_fluo_name.set_clim(0, np.max(orig_fluo))
plt.colorbar(orig_fluo_name,ax=ax2)
# plt.colorbar()
roi_start=(100,80)#(100,120)
w,h=330,330


# plt.subplot(121)
# Create a Rectangle patch
rect = patches.Rectangle(roi_start,w,h,linewidth=3,edgecolor='r',facecolor='none')
circle = patches.Circle((289.3,296.5),138, fill=None, edgecolor='r')
# Add the patch to the Axes
ax1.add_patch(rect)
fluo_img_name=ax1.imshow(fluo_img)
fluo_img_name.set_clim(0, np.max(orig_fluo))
ax2.add_patch(circle)

plt.colorbar(fluo_img_name,ax=ax1)
# show_img('fluo_img', fluo_img, h_scale=500)
roi_fluo_img = np.sum(fluo_img[roi_start[0]:roi_start[0]+w,roi_start[1]:roi_start[1]+h])
run.save_result('roi_fluo_img', roi_fluo_img)

# plt.subplot(122)
# show_img('MOT_fluo_img', MOT_fluo_img, h_scale=np.max(MOT_fluo_img))
# roi_fluo_img = np.sum(MOT_fluo_img)
# run.save_result('roi_MOT_fluo_img', roi_fluo_img)

try:
    fp = fitgaussian2d(fluo_img, [283,243])
    if np.isnan(fp[0])==False:
        ax1.contour(gaussian(fp[0],fp[1],fp[2],fp[3],fp[4],fp[5])(*np.indices(np.shape(fluo_img))), levels=[10,50])
        plt.text(222.95, 300.15, """
        x : %.1f
        y : %.1f
        width_x : %.1f
        width_y : %.1f
        height : %.1f""" %(fp[0], fp[1], fp[2], fp[3], fp[4]),
                fontsize=8, horizontalalignment='center',
                verticalalignment='bottom')
        gaussian_int = fp[4] *2* 3.14159*(fp[2]*fp[3])#+fp[5]*w*h
        if abs(fp[0]-246)>120: gaussian_int=0
        run.save_result('gaussian_int', gaussian_int)
        plt.figure('xxx')
        checkfit(fluo_img, fp)
        # plt.text(222.95, 300.15, """
        # x : %.1f
        # y : %.1f
        # width_x : %.1f
        # width_y : %.1f""" %(fp[0], fp[1], fp[2], fp[3]),
                # fontsize=8, horizontalalignment='center',
                # verticalalignment='bottom')
        # plt.contour(gaussian(fp[0],fp[1],fp[2],fp[3],fp[4],fp[5])(*np.indices(np.shape(fluo_img))))
        print('fit: ',fp)
        run.save_result_array('Gaussian_fit', fp)
        fp[0:4] = [int(f) for f in fp[0:4]]
        plt.text(222.95, 300.15, """
        x : %.1f
        y : %.1f
        width_x : %.1f
        width_y : %.1f
        height : %.1f""" %(fp[0], fp[1], fp[2], fp[3], fp[4]),
                fontsize=8, horizontalalignment='center',
                verticalalignment='bottom')
        fitted_img = gaussian(*fp)(*np.indices(np.shape(fluo_img)))
        # plt.figure('residue_fluo_img')
        # plt.subplot(122)
        # plt.imshow(fluo_img-fitted_img)
        # plt.colorbar()
        
        # checkfit(fluo_img, fp)
        
        x0, y0 = [217, 272]
        # fp[0:2] = x0, y0
        crop = int(fp[3])
        # roi_fluo_img = np.mean(fluo_img[int(fp[0]-crop):int(fp[0]+crop), int(fp[1]-crop):int(fp[1]+crop)])
        # roi_fluo_img = np.sum(fluo_img)
        # run.save_result('roi_fluo_img', roi_fluo_img)
       
        
        if fp[4]>0 and -0.1<fp[0]<481 and -0.1<fp[1]<601:
            run.save_result('Gaussian_width_x', fp[2])
            run.save_result('Gaussian_width_y', fp[3])
            run.save_result('Gaussian_height', fp[4])
            run.save_result('Gaussian_center_y',fp[0])
            run.save_result('Gaussian_center_x',fp[1])
            
        else:
            run.save_result('Gaussian_width_x', np.nan)
            run.save_result('Gaussian_width_y', np.nan)
            run.save_result('Gaussian_height', np.nan)
            run.save_result('Gaussian_center_y',np.nan)
            run.save_result('Gaussian_center_x',fp[1])
        print('roi_fluo_img=',roi_fluo_img)
        print('Gaussian_height=',fp[4])
    else:
        run.save_result('roi_fluo_img', 0)
        run.save_result('Gaussian_height', 0)
except Exception as e:
    print('Error::::::::::::::'+str(e))