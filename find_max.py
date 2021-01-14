from __future__ import division
import lyse
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = lyse.data()
sci_abs, file_name = [], []
maxv, maxf = 0, ''
minv, minf = 9999, ''
# group, targ = 'MOT_abs', 'roi_OD'
# group, targ = 'temperature', 'PSD'
group, targ = 'MOT_fluo', 'roi_fluo_img'

for index, row in df.iterrows():
    file = row['filepath'].values[0]
    try:
        with h5py.File(file,'r') as h5_file:
            for groupname in h5_file['results']:
                if groupname==group:
                    # sci_abs.append(float(h5_file['results'][groupname].attrs['roi_OD']))
                    # file_name.append(file)
                    if maxv<float(h5_file['results'][groupname].attrs[targ]):
                        maxv = float(h5_file['results'][groupname].attrs[targ])
                        maxf = file
                    if minv>float(h5_file['results'][groupname].attrs[targ]):
                        minv = float(h5_file['results'][groupname].attrs[targ])
                        minf = file
    except Exception as e:
        # print('no results', e, file)
        continue

# file = file_name[sci_abs.index(max(sci_abs))+2]
# print(file)
# print(sci_abs.index(max(sci_abs))+2, max(sci_abs))
print(maxf, maxv)
print(minf, minv)