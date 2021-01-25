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
import sys # to print warning messages

#      horizontal, vertical
roi_center = (320,310)
roi_radius = 200
font_size = 10
camera_saturation = 4095

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
    

df = data(path)
run = Run(path)
fluo_img, orig_fluo = get_images()

# camera saturation warning
if np.max(orig_fluo) >= camera_saturation:
    message = 'User Warning: Camera saturated!'
    sys.stderr.write(message+'\n')

# Create the figure
plt.figure('fluo_img')
fig, axes = plt.subplots(2,2)

# subplot 1: fluo - bg
fluo_img_name=axes[0,0].imshow(fluo_img)
fluo_img_name.set_clim(0, np.max(orig_fluo))
roi = patches.Circle(roi_center,roi_radius,linewidth=1, fill=None,edgecolor='r')
axes[0,0].add_patch(roi)
axes[0,0].title.set_text("fluo - bg")

# save integrated fluorescence signal within roi
cy, cx = roi_center[0], roi_center[1] # cy,cx in the sense of column and row, while roi_center in the sense of left/right and up/down. 
r = roi_radius
y, x = np.arange(0,fluo_img.shape[0]), np.arange(0,fluo_img.shape[1])
mask = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < r**2
roi_fluo_img = np.sum(fluo_img[mask])
run.save_result('roi_fluo_img', roi_fluo_img)

# subplot 2: fluo
orig_fluo_name=axes[0,1].imshow(orig_fluo)
orig_fluo_name.set_clim(0, np.max(orig_fluo))
roi = patches.Circle(roi_center,roi_radius,linewidth=1, fill=None,edgecolor='r')
axes[0,1].add_patch(roi)
axes[0,1].title.set_text("fluo")

# The axes of the Gaussian are aligned with the camera
try:
    fp = fitgaussian2d(fluo_img, roi_center)
    if np.isnan(fp[0])==False:
        plt.text(2, 1, """
        y : %.1f
        x : %.1f
        width_y : %.1f
        width_x : %.1f
        height : %.1f""" %(fp[0], fp[1], fp[2], fp[3], fp[4]),
                fontsize=font_size, horizontalalignment='center',
                verticalalignment='top', transform=axes[1,0].transAxes)
        
        fitted_img = gaussian(*fp)(*np.indices(np.shape(fluo_img)))   
        # subplot 3: Gaussian fitted fluo
        Gaussian_fit_name=axes[1,0].imshow(fitted_img)
        Gaussian_fit_name.set_clim(0, np.max(orig_fluo))
        roi = patches.Circle(roi_center,roi_radius,linewidth=1, fill=None,edgecolor='r')
        axes[1,0].add_patch(roi)
        axes[1,0].title.set_text("Gaussian fit")

        # subplot 4: Gaussian fit residual
        residual_name=axes[1,1].imshow(fitted_img-fluo_img)
        residual_name.set_clim(np.min(fitted_img-fluo_img), np.max(fitted_img-fluo_img))
        roi = patches.Circle(roi_center,roi_radius,linewidth=1, fill=None,edgecolor='r')
        axes[1,1].add_patch(roi)
        axes[1,1].title.set_text("Gaussian fit- (fluo-bg)") 
        pos = get(gca(), 'position')
        cbaxes = fig.add_axes([pos.x0-0.1, pos.y0-0.05, (pos.x1-pos.x0)*0.8, 0.01]) # position = [x0,y0,x1,y1]. add_axes = [x0,y0,width,height]
        fig.colorbar(residual_name, cax = cbaxes, orientation="horizontal")
        
        gaussian_int = fp[4] *2* np.pi*(fp[2]*fp[3])         
        run.save_result_array('Gaussian_fit', fp) # save Gaussian fit
        if fp[4]>0 and 0<fp[0]<fluo_img.shape[0] and 0<fp[1]<fluo_img.shape[1]:
            run.save_result('Gaussian_center_y',fp[0])
            run.save_result('Gaussian_center_x',fp[1])
            run.save_result('Gaussian_width_y', fp[2])
            run.save_result('Gaussian_width_x', fp[3])
            run.save_result('Gaussian_height', fp[4])
            run.save_result('gaussian_int', gaussian_int)
            
            # Use gaussian fit result to check whether the atoms are within roi
            if roi_center[1]+roi_radius<fp[0]+1.25*fp[2] or roi_center[1]-roi_radius>fp[0]-1.25*fp[2] or roi_center[0]+roi_radius<fp[1]+1.25*fp[3] or roi_center[0]-roi_radius>fp[1]-1.25*fp[3]:
                message = 'User Warning: Atoms are out of ROI!'
                sys.stderr.write(message+'\n')
        else:
            run.save_result('Gaussian_center_y',np.nan)
            run.save_result('Gaussian_center_x',np.nan) 
            run.save_result('Gaussian_width_y', np.nan)
            run.save_result('Gaussian_width_x', np.nan)
            run.save_result('Gaussian_height', np.nan)
            run.save_result('gaussian_int', np.nan)

    else:
        run.save_result('gaussian_int', np.nan)
        run.save_result('Gaussian_height', np.nan)
except Exception as e:
    print('Error::::::::::::::'+str(e))
 
plt.rcParams.update({'font.size': font_size})
# color bar
cbar = fig.colorbar(orig_fluo_name, ax=axes.ravel().tolist()) # This is not compatible with tight layout
cbar.ax.tick_params(labelsize=font_size)
