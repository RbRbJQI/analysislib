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
import copy

font_size = 10
XZ_center = (285,158)
XY_center = (265,307)
science_center = (234,290)

camera_saturation = 4095
OD_clim = [] # Use the fitted peak OD as default when left empty

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
    return np.array(atom), np.array(probe)  
    
df = data(path)
run = Run(path)
my_idx = df["sequence_index"]
sequence_idx=str(my_idx)
orientation = df['probe_direction']
atom, probe = get_images(orientation)

# camera saturation warning
if np.max(probe) >= camera_saturation or np.max(atom) >= camera_saturation:
    message = 'User Warning: Camera saturated!'
    sys.stderr.write(message+'\n')

mask_bad = np.zeros(probe.shape)
OD = np.zeros(probe.shape)
mask_bad[probe<=0] = np.nan # Set OD = Nan, wherever no probe light detected in the probe shot
mask_bad[atom<=0] = np.nan # Set OD = Nan, wherever no probe light detected in the atom shot
OD[mask_bad==0] = -np.log(np.divide(atom[mask_bad==0], probe[mask_bad==0]))
OD[mask_bad!=0] = np.nan
suptitle_text = 'Number of pixels with no detected light = '+str(np.sum(np.isnan(OD)))
print(suptitle_text)

plt.figure('abs_img')
fig, axes = plt.subplots(2,3)

probe_name = axes[0,0].imshow(probe)
probe_name.set_clim(0, np.max(probe))
axes[0,0].title.set_text('Probe-bg')

atom_name = axes[0,1].imshow(atom)
atom_name.set_clim(0, np.max(probe))
axes[0,1].title.set_text('Atom-bg')

# Show red when OD = nan
cmap = copy.copy(matplotlib.cm.get_cmap("viridis"))
cmap.set_bad(color = 'red')
OD_name = axes[1,0].imshow(OD, cmap=cmap)

axes[1,0].title.set_text('OD')

try:
    OD_nan_ignore = np.nan_to_num(OD)
    fp = fitgaussian2d(OD_nan_ignore, eval(orientation+'_center'))
    if np.isnan(fp[0])==False:       
        axes[0,2].text(0, 1, """
        y : %.1f
        x : %.1f
        width_y : %.1f
        width_x : %.1f
        height : %.1f""" %(fp[0], fp[1], fp[2], fp[3], fp[4]),
                fontsize=font_size, horizontalalignment='left',
                verticalalignment='top', transform=axes[0,2].transAxes)

        fitted_img = gaussian(*fp)(*np.indices(np.shape(OD)))   
        # subplot: Gaussian fitted OD
        Gaussian_fit_name=axes[1,1].imshow(fitted_img)
        axes[1,1].title.set_text("Gaussian fitted OD")
        
        # subplot: 1D cut of OD
        axes[0,2].plot(OD[round(fp[0]),range(OD.shape[1])])
        axes[0,2].plot(gaussian(fp[0],fp[1],fp[2],fp[3],fp[4],fp[5])(fp[0],range(OD.shape[1])))
        axes[0,2].set_xlabel('x')
        axes[0,2].set_ylabel('OD(x,'+str(round(fp[0]))+')')
        pos = axes[0,2].get_position()
        axes[0,2].set_position([pos.x0+0.07, pos.y0+0.05, pos.x1-pos.x0, pos.y1-pos.y0])
        
        axes[1,2].plot(OD[range(OD.shape[0]),round(fp[1])])
        axes[1,2].plot(gaussian(fp[0],fp[1],fp[2],fp[3],fp[4],fp[5])(range(OD.shape[0]),fp[1]))
        axes[1,2].set_xlabel('y')
        axes[1,2].set_ylabel('OD('+str(round(fp[1]))+',y)')
        pos = axes[1,2].get_position()
        axes[1,2].set_position([pos.x0+0.07, pos.y0, pos.x1-pos.x0, pos.y1-pos.y0])
        
        if OD_clim==[]:
            OD_clim = [0-0.1,gaussian(fp[0],fp[1],fp[2],fp[3],fp[4],fp[5])(fp[0],fp[1])+0.3]
        
        gaussian_int = fp[4] *2* np.pi*(fp[2]*fp[3])       
        run.save_result_array('Gaussian_fit', fp) # save Gaussian fit
        if fp[4]>0 and 0<fp[0]<probe.shape[0] and 0<fp[1]<probe.shape[1]:
            run.save_result('Gaussian_center_y',fp[0])
            run.save_result('Gaussian_center_x',fp[1])
            run.save_result('Gaussian_width_y', fp[2])
            run.save_result('Gaussian_width_x', fp[3])
            run.save_result('Gaussian_height', fp[4])
            run.save_result('gaussian_int', gaussian_int)
        else:
            run.save_result('Gaussian_center_y',np.nan)
            run.save_result('Gaussian_center_x',np.nan) 
            run.save_result('Gaussian_width_y', np.inf)
            run.save_result('Gaussian_width_x', np.inf)
            run.save_result('Gaussian_height', 0)
            run.save_result('gaussian_int', 0)

    else:
        run.save_result('Gaussian_center_y',np.nan)
        run.save_result('Gaussian_center_x',np.nan) 
        run.save_result('Gaussian_width_y', np.inf)
        run.save_result('Gaussian_width_x', np.inf)
        run.save_result('Gaussian_height', 0)
        run.save_result('gaussian_int', 0)


except Exception as e:
    print('Error::::::::::::::'+str(e))

if OD_clim==[]:
    OD_clim = [0-0.1,3+0.1]

OD_name.set_clim(OD_clim)
Gaussian_fit_name.set_clim(OD_clim)
axes[0,2].set_ylim(OD_clim)
axes[1,2].set_ylim(OD_clim)
    
# colorbar
cbaxes = fig.add_axes([0.01, 0.55, 0.01, 0.4]) # position = [x0,y0,x1,y1]. add_axes = [x0,y0,width,height]
fig.colorbar(probe_name, cax = cbaxes)

cbaxes = fig.add_axes([0.01, 0.05, 0.01, 0.4]) # position = [x0,y0,x1,y1]. add_axes = [x0,y0,width,height]
fig.colorbar(OD_name, cax = cbaxes)

plt.suptitle(suptitle_text+"\nseq_index="+sequence_idx)
plt.rcParams.update({'font.size': font_size})
