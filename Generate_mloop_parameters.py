from __future__ import division
from lyse import *
from pylab import *
import h5py
from analysislib.common import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys # to print warning messages

df = data(path)
file = df['filepath']

MHz = 1e6
us = 1e-6
ms = 1e-3

optimize_group = ['quad_trap_Mloop','transport_shim_Mloop']

'''
Don't use var to set min_v and max_v!
AFter optimization, we will run this script again. We compare var with the manual limits to see whether an variable is at the boundary.
'''


try:
    with h5py.File(file,'r') as h5_file:
        groupname = 'globals'
        dict = {}
        for optimize_groupi in optimize_group:
            for var_name in h5_file[groupname][optimize_groupi].attrs:
                var = h5_file[groupname][optimize_groupi].attrs[str(var_name)]
                var = float(eval(var))
                var = round(var, 5)

                '''
                CMOT_Mloop
                '''
                if 'CMOT_B_bias_end_x' in var_name:
                    min_v, max_v = 0.3-0.5, 0.3+0.5
                if 'CMOT_B_bias_end_y' in var_name:
                    min_v, max_v = -0.6-0.5, -0.6+0.5
                if 'CMOT_B_bias_end_z' in var_name:
                    min_v, max_v = -0.5, 0.5
                if 'CMOT_cooling_freq_end' in var_name:
                    min_v, max_v = 74.217-20/16, 74.217+20/16
                if 'CMOT_duration' in var_name:
                    min_v, max_v = 25-5, 25+6
                if 'CMOT_quad_curr_end' in var_name:
                    min_v, max_v = 19.662-5, 19.662+5
                        
                    
                '''
                molasses_Mloop
                '''
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
                
                '''
                quad_trap_Mloop
                '''
                if 'quad_trap_B_bias_end_x' in var_name:
                    min_v, max_v = -7.5-5, -7.5+5
                if 'quad_trap_B_bias_end_y' in var_name:
                    min_v, max_v = 2.5-5, 2.5+5
                if 'quad_trap_B_bias_end_z' in var_name:
                    min_v, max_v = 0.74-5, 0.74+5
                if 0:
                    if 'quad_trap_B_bias_start_x' in var_name:
                        min_v, max_v = -2.3-1, -2.3+1
                    if 'quad_trap_B_bias_start_y' in var_name:
                        min_v, max_v = 1.24-1, 1.24+1
                    if 'quad_trap_B_bias_start_z' in var_name:
                        min_v, max_v = -1, +1
                    if 'quad_trap_hold_time' in var_name:
                        min_v, max_v = 10, 40
                    if 'quad_trap_quad_curr_end' in var_name:
                        min_v, max_v = 30, 40
                    if 'quad_trap_quad_curr_start' in var_name:
                        min_v, max_v = 28-5, 28+5
                    if 'quad_trap_quad_ramp_start_delay' in var_name:
                        min_v, max_v = 10, 40
                    if 'quad_trap_ramp_duration' in var_name:
                        min_v, max_v = 10, 60                    

                '''
                transport_speed_Mloop
                '''  
                if 'move_dt_rel_1' in var_name:
                    min_v, max_v = 5.6-0.2, 5.6+0.2
                if 'move_dt_rel_2' in var_name:
                    min_v, max_v = 1.24-0.2, 1.24+0.2  
                if 'move_dt_rel_3' in var_name:
                    min_v, max_v = 4.09-0.2, 4.09+0.2    
                if 'move_dt_rel_4' in var_name:
                    min_v, max_v = 0.58-0.1, 0.58+0.1            
                if 'move_dt_rel_5' in var_name:
                    min_v, max_v = 3.22-0.2, 3.22+0.2            
                if 'move_dt_rel_6' in var_name:
                    min_v, max_v = 1.33-0.2, 1.33+0.2                   
                if 'move_v_rel_3' in var_name:
                    min_v, max_v = 0.29-0.2, 0.29+0.2           
                if 'move_v_rel_5' in var_name:
                    min_v, max_v = 0.45-0.2, 0.45+0.2   
                
                '''
                transport_coil_geometry_Mloop
                '''
                if 'INNER_TRANS_N_TURNS' in var_name:
                    min_v, max_v = 62, 62.6
                if 'MOT_N_TURNS' in var_name:
                    min_v, max_v = 59.5, 60.5  
                if 'MOT_coils_spacing_factor' in var_name:
                    min_v, max_v = 1.13-0.06, 1.13+0.06  
                if 'OUTER_TRANS_N_TURNS' in var_name:
                    min_v, max_v = 59.361997342349596-0.07, 59.361997342349596+0.07            
                if 'SCIENCE_N_TURNS' in var_name:
                    min_v, max_v = 55.9-0.5, 55.9+0.5 
                if 'inner_coils_0_spacing_factor' in var_name:
                    min_v, max_v = 0.92-0.1, 0.92+0.1  
                if 'inner_coils_1_spacing_factor' in var_name:
                    min_v, max_v = 1.05, 1.15            
                if 'inner_coils_2_spacing_factor' in var_name:
                    min_v, max_v = 1.01-0.1, 1.01+0.1           
                if 'inner_coils_3_spacing_factor' in var_name:
                    min_v, max_v = 0.99-0.05, 0.99+0.05                    
                if 'outer_coils_0_spacing_factor' in var_name:
                    min_v, max_v = 1.05-0.1, 1.05+0.1
                if 'outer_coils_1_spacing_factor' in var_name:
                    min_v, max_v = 0.94-0.1, 0.94+0.1  
                if 'outer_coils_2_spacing_factor' in var_name:
                    min_v, max_v = 1.14-0.1, 1.14+0.1   
                if 'outer_coils_3_spacing_factor' in var_name:
                    min_v, max_v = 0.94-0.1, 0.94+0.1           
                if 'outer_coils_4_spacing_factor' in var_name:
                    min_v, max_v = 00.81-0.1, 0.81+0.1
                if 'science_coils_spacing_factor' in var_name:
                    min_v, max_v = 0.98-0.1, 0.98+0.1
                
                '''
                transport_trap_characteristics_Mloop
                '''
                if 'd2beta_final_dy2_0' in var_name:
                    min_v, max_v = 1338-50, 1338+50
                if 'd2beta_final_dy2_1' in var_name:
                    min_v, max_v = 1531, 1551 
                if 'd2beta_initial_dy2_0' in var_name:
                    min_v, max_v = 995-15, 995+15    
                if 'd2beta_initial_dy2_1' in var_name:
                    min_v, max_v = 730, 770  
                if 'final_switch_y_frac' in var_name:
                    min_v, max_v = 0.57-0.05, 0.57+0.05
                if 'initial_switch_y_frac' in var_name:
                    min_v, max_v = 0.43-0.05, 0.43+0.05
                if 'move_final_current' in var_name:
                    min_v, max_v = 41, 45
                if 'move_grad_0' in var_name:
                    min_v, max_v = 1.46-0.3, 1.46+0.3  
                if 'move_grad_1' in var_name:
                    min_v, max_v = 2.06-0.3, 2.06+0.3 
                if 'move_grad_2' in var_name:
                    min_v, max_v = 3, 3.5            
                if 'move_grad_3' in var_name:
                    min_v, max_v = 1.7-0.3, 1.7+0.3            
                if 'move_grad_4' in var_name:
                    min_v, max_v = 2.0-0.3, 2.0+0.3            
                if 'move_grad_5' in var_name:
                    min_v, max_v = 1.48-0.3, 1.48+0.3
                if 'move_grad_6' in var_name:
                    min_v, max_v = 2.31-0.3, 2.31+0.3 
                if 'move_grad_7' in var_name:
                    min_v, max_v = 2.09-0.3, 2.09+0.3  
                if 'move_grad_8' in var_name:
                    min_v, max_v = 0.72-0.3, 0.72+0.3                           
                
                '''
                transport_unitconversions_Mloop
                '''
                if 'curr_ratio_ch1' in var_name:
                    min_v, max_v = 0.82, 0.92            
                if 'curr_ratio_ch2' in var_name:
                    min_v, max_v = 0.93, 0.97            
                if 'curr_ratio_ch3' in var_name:
                    min_v, max_v = 0.94, 1.00           
                if 'curr_ratio_ch4' in var_name:
                    min_v, max_v = 0.95, 1.05
                
                '''
                transport_shim_Mloop
                '''
                if 1:
                    if 'transport_MOT_B_bias_ramp_duration' in var_name:
                        min_v, max_v = 0.01, 0.5 
                    if 'transport_MOT_B_bias_x' in var_name:
                        min_v, max_v = -1, 6           
                    if 'transport_MOT_B_bias_y' in var_name:
                        min_v, max_v = -1, 6
                    if 'transport_MOT_B_bias_z' in var_name:
                        min_v, max_v = -4, 2
                else:
                    if 'transport_shim_current' in var_name:
                        min_v, max_v = -2, 2
                    if 'transport_shim_start' in var_name:
                        min_v, max_v = 0.45, 0.7
                
                try:
                    min_v
                    max_v
                except NameError:
                    print(var_name+' will NOT be optimized by Mloop!')
                else:               
                    if min_v>max_v:
                        print('\n',var_name, min_v, max_v,'\n')
                    
                    if optimize_groupi in optimize_group:
                        dict[var_name] = {"min": min_v, "max": max_v, "start": var}
                    
                    # Check whether the optimized parameters are limited by the limits
                    margin = min([abs(max_v-var),abs(var-min_v)])
                    range = max_v - min_v
                    if margin <= 0.05*range:
                        message = var_name+' at the boundary!'
                        sys.stderr.write(message+'\n')

                    # clear limits so that variables without given limits will NOT be assigned with the previous variable's limits
                    del min_v
                    del max_v
                                  
        print(str(dict).replace("'",'"'))
except Exception as e:
    print('no results', e, file)