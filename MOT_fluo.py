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
from dragable_plot import MoveGraphLine
from matplotlib.widgets import TextBox
import h5py

#      horizontal, vertical
roi_center = (269,306)
roi_radius = 145
target_center = (265,246)
Do_dynamic_ROI = 0

font_size = 10
camera_saturation = 4095
Gaussian_width_limit_y = 300
Gaussian_width_limit_x = 300

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

if Do_dynamic_ROI:    
    def get_dynamic_ROI(filepath):
        try:
            with h5py.File(filepath,'r') as h5_file:
                roi_center = h5_file['results']['dragable_plot'].attrs['ROI'][0:2]
                roi_radius = h5_file['results']['dragable_plot'].attrs['ROI'][2]
            return roi_center, roi_radius
        except:
            return None
        
df = data(path)
run = Run(path)
my_idx = df["sequence_index"]
sequence_idx=str(my_idx)
df_all = data()

if Do_dynamic_ROI:
    ROI_save_to_idx = 0
    ROI_save_to_path = df_all['filepath'].values[ROI_save_to_idx]
    ROI_par = get_dynamic_ROI(ROI_save_to_path)
    if not ROI_par==None:
        roi_center = ROI_par[0]
        roi_radius = ROI_par[1]
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
if Do_dynamic_ROI:
    roi = MoveGraphLine(ROI_save_to_path, axes[0,0], roi_center, roi_radius)
    axbox = fig.add_axes([0.2, 0.05, 0.1, 0.03])
    text_box = TextBox(axbox, 'Radius', initial=str(roi_radius))
    text_box.on_submit(roi.submit_radius)
else:
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
roi2 = patches.Circle(roi_center,roi_radius,linewidth=1, fill=None,edgecolor='r')
axes[0,1].add_patch(roi2)
axes[0,1].title.set_text("fluo")

# The axes of the Gaussian are aligned with the camera
try:
    fp = fitgaussian2d(fluo_img, roi_center)
    if np.isnan(fp[0])==False:
        axes[0,0].text(0.9, 0.1, """
        y : %.1f
        x : %.1f
        width_y : %.1f
        width_x : %.1f
        height : %.1f""" %(fp[0], fp[1], fp[2], fp[3], fp[4]),
                fontsize=font_size, horizontalalignment='right', 
                verticalalignment='bottom', color='white', transform=axes[0,0].transAxes)
        
        fitted_img = gaussian(*fp)(*np.indices(np.shape(fluo_img)))   
        # subplot 3: Gaussian fitted fluo
        Gaussian_fit_name=axes[1,0].imshow(fitted_img)
        Gaussian_fit_name.set_clim(0, np.max(orig_fluo))
        roi2 = patches.Circle(roi_center,roi_radius,linewidth=1, fill=None,edgecolor='r')
        axes[1,0].add_patch(roi2)
        axes[1,0].title.set_text("Gaussian fit")

        # subplot 4: Gaussian fit residual
        residual_name=axes[1,1].imshow(fitted_img-fluo_img)
        residual_name.set_clim(np.min(fitted_img-fluo_img), np.max(fitted_img-fluo_img))
        roi2 = patches.Circle(roi_center,roi_radius,linewidth=1, fill=None,edgecolor='r')
        axes[1,1].add_patch(roi2)
        axes[1,1].title.set_text("Gaussian fit- (fluo-bg)") 
        pos = axes[1,1].get_position()
        cbaxes = fig.add_axes([pos.x0-0.08, pos.y0-0.05, (pos.x1-pos.x0)*0.8, 0.01]) # position = [x0,y0,x1,y1]. add_axes = [x0,y0,width,height]
        fig.colorbar(residual_name, cax = cbaxes, orientation="horizontal")
        
        gaussian_int = fp[4] *2* np.pi*(fp[2]*fp[3]) 
        PSD_singleshot = gaussian_int/ (fp[2]*fp[3])**3 * df['TOF']**3
        run.save_result_array('Gaussian_fit', fp) # save Gaussian fit
        if fp[4]>0 and 0<fp[0]<fluo_img.shape[0] and 0<fp[1]<fluo_img.shape[1] and fp[2]<Gaussian_width_limit_y and fp[3]<Gaussian_width_limit_x:
            run.save_result('Gaussian_center_y',fp[0])
            run.save_result('Gaussian_center_x',fp[1])
            run.save_result('Gaussian_width_y', fp[2])
            run.save_result('Gaussian_width_x', fp[3])
            run.save_result('Gaussian_height', fp[4])
            run.save_result('gaussian_int', gaussian_int)
            run.save_result('PSD_singleshot', PSD_singleshot)
            run.save_result('Distance_to_center', pow((fp[1]-float(target_center[1]))**2+(fp[0]-float(target_center[0]))**2,1/2))
            
            # Use gaussian fit result to check whether the atoms are within roi
            if roi_center[1]+roi_radius<fp[0]+1.25*fp[2] or roi_center[1]-roi_radius>fp[0]-1.25*fp[2] or roi_center[0]+roi_radius<fp[1]+1.25*fp[3] or roi_center[0]-roi_radius>fp[1]-1.25*fp[3]:
                message = 'User Warning: Atoms are out of ROI!'
                sys.stderr.write(message+'\n')
        else:
            run.save_result('Gaussian_center_y',np.nan)
            run.save_result('Gaussian_center_x',np.nan) 
            run.save_result('Gaussian_width_y', np.inf)
            run.save_result('Gaussian_width_x', np.inf)
            run.save_result('Gaussian_height', 0)
            run.save_result('gaussian_int', 0)
            run.save_result('PSD_singleshot', 0)
            run.save_result('Distance_to_center',np.inf)

    else:
        run.save_result('Gaussian_center_y',np.nan)
        run.save_result('Gaussian_center_x',np.nan) 
        run.save_result('Gaussian_width_y', np.inf)
        run.save_result('Gaussian_width_x', np.inf)
        run.save_result('Gaussian_height', 0)
        run.save_result('gaussian_int', 0)
        run.save_result('PSD_singleshot', 0)
        run.save_result('Distance_to_center',np.inf)
        
except Exception as e:
    print('Error::::::::::::::'+str(e))

plt.suptitle("seq_index="+sequence_idx)
plt.rcParams.update({'font.size': font_size})
# color bar
cbar = fig.colorbar(orig_fluo_name, ax=axes.ravel().tolist()) # This is not compatible with tight layout

