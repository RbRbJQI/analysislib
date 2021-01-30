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

optimize_group = ['transport_shim_Mloop']

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
                if 'quad_trap_B_bias_start_x' in var_name:
                    min_v, max_v = -2.3-1, -2.3+1
                if 'quad_trap_B_bias_start_y' in var_name:
                    min_v, max_v = 1.24-1, 1.24+1
                if 'quad_trap_B_bias_start_z' in var_name:
                    min_v, max_v = -1, +1
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
                    min_v, max_v = 1.34-0.2, 1.34+0.2  
                if 'move_dt_rel_3' in var_name:
                    min_v, max_v = 3.99-0.2, 3.99+0.2    
                if 'move_dt_rel_4' in var_name:
                    min_v, max_v = 0.54-0.1, 0.54+0.1            
                if 'move_dt_rel_5' in var_name:
                    min_v, max_v = 3.02-0.2, 3.02+0.2            
                if 'move_dt_rel_6' in var_name:
                    min_v, max_v = 1.20-0.2, 1.20+0.2                   
                if 'move_v_rel_3' in var_name:
                    min_v, max_v = 0.41-0.2, 0.41+0.2           
                if 'move_v_rel_5' in var_name:
                    min_v, max_v = 0.38-0.2, 0.38+0.2   
                
                '''
                transport_coil_geometry_Mloop
                '''
                if 'INNER_TRANS_N_TURNS' in var_name:
                    min_v, max_v = 61.5, 62.5
                if 'MOT_N_TURNS' in var_name:
                    min_v, max_v = 59, 60  
                if 'MOT_coils_spacing_factor' in var_name:
                    min_v, max_v = 1.1664588498686552-0.06, 1.1664588498686552+0.06  
                if 'OUTER_TRANS_N_TURNS' in var_name:
                    min_v, max_v = 59.361997342349596-0.07, 59.361997342349596+0.07            
                if 'SCIENCE_N_TURNS' in var_name:
                    min_v, max_v = 55.49031733203944-0.5, 55.49031733203944+0.5 
                if 'inner_coils_0_spacing_factor' in var_name:
                    min_v, max_v = 1.0166875334333076-0.1, 1.0166875334333076+0.1  
                if 'inner_coils_1_spacing_factor' in var_name:
                    min_v, max_v = 0.9, 1.1            
                if 'inner_coils_2_spacing_factor' in var_name:
                    min_v, max_v = 0.9582473284775698-0.1, 0.9582473284775698+0.1           
                if 'inner_coils_3_spacing_factor' in var_name:
                    min_v, max_v = 0.9390285477731173-0.05, 0.9390285477731173+0.05                    
                if 'outer_coils_0_spacing_factor' in var_name:
                    min_v, max_v = 1.0134866135121907-0.1, 1.0134866135121907+0.1
                if 'outer_coils_1_spacing_factor' in var_name:
                    min_v, max_v = 0.9045343385932298-0.1, 0.9045343385932298+0.1  
                if 'outer_coils_2_spacing_factor' in var_name:
                    min_v, max_v = 1.1-0.1, 1.2   
                if 'outer_coils_3_spacing_factor' in var_name:
                    min_v, max_v = 0.8736665639691724-0.1, 0.8736665639691724+0.1           
                if 'outer_coils_4_spacing_factor' in var_name:
                    min_v, max_v = 0.9110499203999851-0.1, 0.9110499203999851+0.1
                if 'science_coils_spacing_factor' in var_name:
                    min_v, max_v = 1.0293735229611503-0.1, 1.0293735229611503+0.1
                
                '''
                transport_shim_Mloop
                '''
                if 'transport_shim0_curr' in var_name:
                    min_v, max_v = -2.5, 1           
                if 'transport_shim0_end' in var_name:
                    min_v, max_v = 0.56, 1
                if 'transport_shim0_start' in var_name:
                    min_v, max_v = 0.38, 0.55
                
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