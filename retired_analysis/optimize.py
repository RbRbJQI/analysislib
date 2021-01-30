from __future__ import division
from lyse import *
from pylab import *
from analysislib.common import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
def Gd(var_df, step_y):
    num_var = len(var_df.columns)-2
    # var_now = np.array(var_df.iloc[-1,0:num_var])
    g_step = 0.8
    if var_df.index[-1]%(num_var+1)>0:
        new_var = np.array(var_df.iloc[-(var_df.index[-1]%(num_var+1)),0:-2].astype(float))
        new_var[int(var_df.index[-1]%(num_var+1))-1] += g_step
        return new_var
    grad = np.zeros(num_var)
    for direction in range(num_var):
        sub = var_df.iloc[-num_var+direction,-2]-var_df.iloc[-num_var-1,-2]
        grad[direction] = np.array(sub)/g_step
    print(grad)
    
    step_x = step_y/np.linalg.norm(grad)
    print(np.linalg.norm(step_x),np.linalg.norm(grad))
    new_var = grad*step_x + np.array(var_df.iloc[-1-num_var,0:num_var].astype(float))
    print(new_var)
    return [np.around(new_vari, 4) for new_vari in new_var]
    
def generate_new_run(var_df):
    var_vals = Gd(var_df, 0.5)
    # var_vals = 1/0
    return list(var_vals)

df = data(path)
run = Run(path)
file = df['filepath']
with h5py.File(file,'r') as h5_file:
    Is_optimize = h5_file['globals']['optimize'].attrs['Is_optimize']
if Is_optimize=='True':
    with h5py.File(file,'r') as h5_file: #retrieve the calculated target
        target_path = ['MOT_abs', 'int_OD']
        int_OD = h5_file['results'][target_path[0]].attrs[target_path[1]]
        target_path = ['MOT_abs', 'roi_OD']
        roi_OD = h5_file['results'][target_path[0]].attrs[target_path[1]]
        target_path = ['MOT_abs', 'Gaussian_fit']
        x, y = h5_file['results'][target_path[0]][target_path[1]][0:2]
        wdx, wdy = h5_file['results'][target_path[0]][target_path[1]][2:4]
        height = h5_file['results'][target_path[0]][target_path[1]][4]
        x, y, wdx, wdy, height = float(x), float(y), float(wdx), float(wdy), float(height)
        x0, y0 = [274, 297]
        # target = -np.sqrt((x-x0)**2+(y-y0)**2)
        target = roi_OD
        # target = height
        print([x,y], target)
    dir = os.path.dirname(file) # retrieve the dataframe
    with open(dir+r"\\optimize.pickle", "rb") as input_file:
        var_df = pickle.load(input_file)
    var_df['target'].iloc[-1] = float(target)
    #generate a new run
    new_val = generate_new_run(var_df)
    new_val += ['TODO']
    new_val += [False]
    var_df.loc[var_df.index[-1]+1] = new_val
    pd.set_option('display.max_columns', None)
    print(var_df)
    with open(dir+r"\\optimize.pickle", "wb") as output_file:
        pickle.dump(var_df, output_file)