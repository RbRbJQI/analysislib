from __future__ import division
from lyse import *
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = data(path)
file = df['filepath']

MHz = 1e6
us = 1e-6
ms = 1e-3

optimize_group = ['molasses_Mloop']

try:
    with h5py.File(file[0],'r') as h5_file:
        groupname = 'globals'
        dict = {}
        for optimize_groupi in optimize_group:
            for var_name in h5_file[groupname][optimize_groupi].attrs:
                var = h5_file[groupname][optimize_groupi].attrs[str(var_name)]
                var = float(eval(var))
                var = round(var, 5)
                if 'B_zero_x' in var_name:
                    min_v, max_v = -0.5, 0.5
                if 'B_zero_y' in var_name:
                    min_v, max_v = -0.5, 0.5
                if 'B_zero_z' in var_name:
                    min_v, max_v = -0.5, 0.5
                if 'molasses_cooling_freq_start' in var_name:   
                    min_v, max_v = 73.751-3, 73.751+3
                if 'molasses_cooling_freq_end' in var_name:
                    min_v, max_v = 76.45-3, 76.45+3
                if 'molasses_cooling_int' in var_name:
                    min_v, max_v = 0, 1.2
                if 'molasses_repump_int_start' in var_name:
                    min_v, max_v = 0, 0.6
                if 'molasses_repump_int_end' in var_name:
                    min_v, max_v = 0, 0.6   
                if 'molasses_duration' in var_name:
                    min_v, max_v = 3, 15  
                                              
                if min_v>max_v:
                    print('\n',var_name, min_v, max_v,'\n')
                var = max(min_v, min(max_v, var))
                if optimize_groupi in optimize_group:
                    dict[var_name] = {"min": min_v, "max": max_v, "start": var}

        print(str(dict).replace("'",'"'))
except Exception as e:
    print('no results', e, file)