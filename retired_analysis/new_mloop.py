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
# print(file)
optimize_group = ['subdoppler', 'cooling','quad_trap_opt']
# optimize_group = ['(C)MOT']
# optimize_group = ['quad_trap']
# optimize_group=['transport']
try:
    with h5py.File(file,'r') as h5_file:
        groupname = 'globals'
        dict = {}
        ms = 0.001
        res = 71.8e6
        MHz = 1e6
        for var_name in h5_file[groupname]['transport'].attrs:
            var = h5_file[groupname]['transport'].attrs[str(var_name)]
            var = float(eval(var))
            var = round(var, 5)
            min_v, max_v = 0.5*var, 2*var
            if 'curr_r0' in var_name:
                min_v, max_v = 0.82, 0.92            
            if 'curr_r1' in var_name:
                min_v, max_v = 0.9, 0.96            
            if 'curr_r2' in var_name:
                min_v, max_v = 0.96, 1.02           
            if 'curr_r3' in var_name:
                min_v, max_v = 0.95, 1.1
            if 'BIAS_N_TURNS1' in var_name:
                min_v, max_v = 57, 59  
            if 'BIAS_N_TURNS2' in var_name:
                min_v, max_v = 57.5, 58.75    
            if 'B_bias_tran_x' in var_name:
                min_v, max_v = -1.2, 0            
            if 'B_bias_tran_y' in var_name:
                min_v, max_v = -0.75, 0.25            
            if 'B_bias_tran_z' in var_name:
                min_v, max_v = 0.25, 1            
            if 'INNER_TRANS_N_TURNS' in var_name:
                min_v, max_v = 61.5, 62.5
            if 'MOT_N_TURNS' in var_name:
                min_v, max_v = 59, 60  
            if 'MOT_coils_spacing_factor' in var_name:
                min_v, max_v = 1.1, 1.25   
            if 'OUTER_TRANS_N_TURNS' in var_name:
                min_v, max_v = 58, 59.5            
            if 'SCIENCE_N_TURNS' in var_name:
                min_v, max_v = 55, 56            
            if 'bias_ratio_yx' in var_name:
                min_v, max_v = 1.2, 1.45            
            if 'd2beta_final_dy2_0' in var_name:
                min_v, max_v = 1200, 1420
            if 'd2beta_final_dy2_1' in var_name:
                min_v, max_v = 1550, 1570 
            if 'd2beta_initial_dy2_0' in var_name:
                min_v, max_v = 1000, 1050    
            if 'd2beta_initial_dy2_1' in var_name:
                min_v, max_v = 720, 770            
            if 'dbeta_beginning_dy_0' in var_name:
                min_v, max_v = 0, 0.025            
            if 'dur_tran_bias' in var_name:
                min_v, max_v = 50, 70            
            if 'final_switch_y_frac' in var_name:
                min_v, max_v = 0.55, 0.75
            if 'initial_switch_y_frac' in var_name:
                min_v, max_v = 0.3, 0.6  
            if 'inner_coils_0_spacing_factor' in var_name:
                min_v, max_v = 0.85, 1.05  
            if 'inner_coils_1_spacing_factor' in var_name:
                min_v, max_v = 0.95, 1.15            
            if 'inner_coils_2_spacing_factor' in var_name:
                min_v, max_v = 0.85, 1.0           
            if 'inner_coils_3_spacing_factor' in var_name:
                min_v, max_v = 0.8, 0.95           
            if 'move_dt_rel_1' in var_name:
                min_v, max_v = 5, 7
            if 'move_dt_rel_2' in var_name:
                min_v, max_v = 1.0, 2.2  
            if 'move_dt_rel_3' in var_name:
                min_v, max_v = 3.7, 4.4    
            if 'move_dt_rel_4' in var_name:
                min_v, max_v = 0.5, 0.7            
            if 'move_dt_rel_5' in var_name:
                min_v, max_v = 2.9, 3.6            
            if 'move_dt_rel_6' in var_name:
                min_v, max_v = 1.1, 1.6            
            if 'move_final_current' in var_name:
                min_v, max_v = 39, 44
            if 'move_grad_0' in var_name:
                min_v, max_v = 0.7, 1.5  
            if 'move_grad_1' in var_name:
                min_v, max_v = 1.2, 2.2 
            if 'move_grad_2' in var_name:
                min_v, max_v = 1.2, 3.5            
            if 'move_grad_3' in var_name:
                min_v, max_v = 1.2, 2.5            
            if 'move_grad_4' in var_name:
                min_v, max_v = 1.2, 2.5            
            if 'move_grad_5' in var_name:
                min_v, max_v = 0.5, 1.7
            if 'move_grad_6' in var_name:
                min_v, max_v = 1.2, 3 
            if 'move_grad_7' in var_name:
                min_v, max_v = 1.2, 2.2  
            if 'move_grad_8' in var_name:
                min_v, max_v = 0.6, 1.5          
            if 'move_v_rel_3' in var_name:
                min_v, max_v = 0.2, 0.9           
            if 'move_v_rel_5' in var_name:
                min_v, max_v = 0.2, 0.6            
            if 'outer_coils_0_spacing_factor' in var_name:
                min_v, max_v = 1.0, 1.2
            if 'outer_coils_1_spacing_factor' in var_name:
                min_v, max_v = 0.8, 1.0  
            if 'outer_coils_2_spacing_factor' in var_name:
                min_v, max_v = 1.1, 1.35   
            if 'outer_coils_3_spacing_factor' in var_name:
                min_v, max_v = 0.85, 1.05           
            if 'outer_coils_4_spacing_factor' in var_name:
                min_v, max_v = 0.75, 0.95
            if 'science_coils_spacing_factor' in var_name:
                min_v, max_v = 0.95, 1.15
            if 'dur_transport' in var_name:
                min_v, max_v = 1.2, 2
       
            if min_v>max_v:
                print('\n',var_name, min_v, max_v,'\n')
            var = max(min_v, min(max_v, var))
            if 'transport' in optimize_group:
                dict[var_name] = {"min": min_v, "max": max_v, "start": var}
        
        for optimize_groupi in optimize_group:
            for var_name in h5_file[groupname][optimize_groupi].attrs:
                var = h5_file[groupname][optimize_groupi].attrs[str(var_name)]
                var = float(eval(var))
                var = round(var, 5)
                min_v, max_v = 0.5*var, 2*var
                # if 'int' in var_name:
                    # min_v, max_v = 0, 2*var
                if 'quad' in var_name:
                    min_v, max_v = -0.22, -0.145                       
                if 'quad_trap' in var_name:
                    min_v, max_v = -1.2, -0.95            
                if 'B_bias_com_x' in var_name:
                    min_v, max_v = -1, 1  
                if 'B_bias_com_y' in var_name:
                    min_v, max_v = -1.5, 0.5            
                if 'B_bias_com_z' in var_name:
                    min_v, max_v = -1, 1.5            
                # if 'B_bias_mol_x' in var_name:
                    # min_v, max_v = -0.5, 0   
                # if 'B_bias_mol_y' in var_name:
                    # min_v, max_v = -0.25, 0.3            
                # if 'B_bias_mol_z' in var_name:
                    # min_v, max_v = -0.1, 0.1            
                if 'B_bias_mot_x' in var_name:
                    min_v, max_v = -1, 1.5  
                if 'B_bias_mot_y' in var_name:
                    min_v, max_v = -1.5, 1            
                if 'B_bias_mot_z' in var_name:
                    min_v, max_v = -1, 1.5                  
                # if 'B_bias_mov_x' in var_name:
                    # min_v, max_v = -0.7, -0.0            
                # if 'B_bias_mov_y' in var_name:
                    # min_v, max_v = -0.7, 0            
                # if 'B_bias_mov_z' in var_name:
                    # min_v, max_v = -1.5, -0.7            
                if 'B_bias_optpump_x' in var_name:
                    min_v, max_v = -0.25, 0.25            
                if 'B_bias_optpump_y' in var_name:
                    min_v, max_v = -0.3, 0.2            
                if 'B_bias_optpump_z' in var_name:
                    min_v, max_v = 0, 0.80            
                if 'B_bias_quad_x' in var_name:
                    min_v, max_v = -1, 1.5            
                if 'B_bias_quad_y' in var_name:
                    min_v, max_v = -1.5, 1              
                if 'B_bias_quad_z' in var_name:
                    min_v, max_v = -1, 1.5      
                if 'B_bias_magtrap_x' in var_name:
                    min_v, max_v = -1, 1.5            
                if 'B_bias_magtrap_y' in var_name:
                    min_v, max_v = -1.5, 1              
                if 'B_bias_magtrap_z' in var_name:
                    min_v, max_v = -1, 1.5                   
                if 'CMOT_dur' in var_name:
                    min_v, max_v = 0.01, 0.03            
                if 'OptPumpint' in var_name:
                    min_v, max_v = 0.2, 1.25         
                if 'bias_dur' in var_name:
                    min_v, max_v = 0.5, 1.5            
                if 'cent' in var_name:
                    min_v, max_v = 7.325*1e7, 7.340*1e7            
                if 'com_cool_int' in var_name:
                    min_v, max_v = 0.9,1.2           
                if 'com_rep_int' in var_name:
                    min_v, max_v = -0.07, 0.6            
                if 'compress_freq_start' in var_name:
                    min_v, max_v = 0, 3               
                if 'compress_freq_end' in var_name:
                    min_v, max_v = 0, 3         
                if 'compressed_MOT_quad' in var_name:
                    min_v, max_v = -0.6, -0.2          
                if 'dur_OptPumping' in var_name:
                    min_v, max_v = 0.5, 2            
                if 'dur_mol' in var_name:
                    min_v, max_v = 0.009, 0.023                    
                if 'mol_cool_int' in var_name:
                    min_v, max_v = 0.82, 1.2            
                if 'mol_rep_int_end' in var_name:
                    min_v, max_v = -0.07, 0.6            
                if 'mol_rep_int_start' in var_name:
                    min_v, max_v = -0.07, 0.6             
                if 'molasses_freq' in var_name:
                    min_v, max_v = 7.31*1e7, 8.0*1e7            
                if 'mot_cool_int' in var_name:
                    min_v, max_v = 0.8, 1.2            
                if 'mot_rep_int' in var_name:
                    min_v, max_v = 0.5, 0.7            
                if 'opt_f' in var_name:
                    min_v, max_v = -0.5, 2
                if 'opt_rep_int' in var_name:
                    min_v, max_v = -0.07, 0.6 
                if 'quad_bias_delay' in var_name:
                    min_v, max_v = 1e-5, 0.005 
                if 'curr_r0' in var_name:
                    min_v, max_v = 0.82, 0.92            
                if 'curr_r1' in var_name:
                    min_v, max_v = 0.9, 0.96            
                if 'curr_r2' in var_name:
                    min_v, max_v = 0.96, 1.02           
                if 'curr_r3' in var_name:
                    min_v, max_v = 0.95, 1.1
                if 'BIAS_N_TURNS1' in var_name:
                    min_v, max_v = 57, 59  
                if 'BIAS_N_TURNS2' in var_name:
                    min_v, max_v = 57.5, 58.75    
                if 'B_bias_tran_x' in var_name:
                    min_v, max_v = -1.2, 0            
                if 'B_bias_tran_y' in var_name:
                    min_v, max_v = -0.75, 0.25            
                if 'B_bias_tran_z' in var_name:
                    min_v, max_v = 0.25, 1            
                if 'INNER_TRANS_N_TURNS' in var_name:
                    min_v, max_v = 61.5, 62.5
                if 'MOT_N_TURNS' in var_name:
                    min_v, max_v = 59, 60  
                if 'MOT_coils_spacing_factor' in var_name:
                    min_v, max_v = 1.1, 1.25   
                if 'OUTER_TRANS_N_TURNS' in var_name:
                    min_v, max_v = 58, 59.5            
                if 'SCIENCE_N_TURNS' in var_name:
                    min_v, max_v = 55, 56            
                if 'bias_ratio_yx' in var_name:
                    min_v, max_v = 1.2, 1.45            
                if 'd2beta_final_dy2_0' in var_name:
                    min_v, max_v = 1200, 1420
                if 'd2beta_final_dy2_1' in var_name:
                    min_v, max_v = 1550, 1570 
                if 'd2beta_initial_dy2_0' in var_name:
                    min_v, max_v = 1000, 1050    
                if 'd2beta_initial_dy2_1' in var_name:
                    min_v, max_v = 720, 770            
                if 'dbeta_beginning_dy_0' in var_name:
                    min_v, max_v = 0, 0.025            
                if 'dur_tran_bias' in var_name:
                    min_v, max_v = 50, 70            
                if 'final_switch_y_frac' in var_name:
                    min_v, max_v = 0.55, 0.75
                if 'initial_switch_y_frac' in var_name:
                    min_v, max_v = 0.3, 0.6  
                if 'inner_coils_0_spacing_factor' in var_name:
                    min_v, max_v = 0.85, 1.05  
                if 'inner_coils_1_spacing_factor' in var_name:
                    min_v, max_v = 0.95, 1.15            
                if 'inner_coils_2_spacing_factor' in var_name:
                    min_v, max_v = 0.85, 1.0           
                if 'inner_coils_3_spacing_factor' in var_name:
                    min_v, max_v = 0.8, 0.95           
                if 'move_dt_rel_1' in var_name:
                    min_v, max_v = 5, 7
                if 'move_dt_rel_2' in var_name:
                    min_v, max_v = 1.0, 2.2  
                if 'move_dt_rel_3' in var_name:
                    min_v, max_v = 3.7, 4.4    
                if 'move_dt_rel_4' in var_name:
                    min_v, max_v = 0.5, 0.7            
                if 'move_dt_rel_5' in var_name:
                    min_v, max_v = 2.9, 3.6            
                if 'move_dt_rel_6' in var_name:
                    min_v, max_v = 1.1, 1.6            
                if 'move_final_current' in var_name:
                    min_v, max_v = 39, 44
                if 'move_grad_0' in var_name:
                    min_v, max_v = 0.7, 1.5  
                if 'move_grad_1' in var_name:
                    min_v, max_v = 1.2, 2.2 
                if 'move_grad_2' in var_name:
                    min_v, max_v = 1.2, 3.5            
                if 'move_grad_3' in var_name:
                    min_v, max_v = 1.2, 2.5            
                if 'move_grad_4' in var_name:
                    min_v, max_v = 1.2, 2.5            
                if 'move_grad_5' in var_name:
                    min_v, max_v = 0.5, 1.7
                if 'move_grad_6' in var_name:
                    min_v, max_v = 1.2, 3 
                if 'move_grad_7' in var_name:
                    min_v, max_v = 1.2, 2.2  
                if 'move_grad_8' in var_name:
                    min_v, max_v = 0.6, 1.5          
                if 'move_v_rel_3' in var_name:
                    min_v, max_v = 0.2, 0.9           
                if 'move_v_rel_5' in var_name:
                    min_v, max_v = 0.2, 0.6            
                if 'outer_coils_0_spacing_factor' in var_name:
                    min_v, max_v = 1.0, 1.2
                if 'outer_coils_1_spacing_factor' in var_name:
                    min_v, max_v = 0.8, 1.0  
                if 'outer_coils_2_spacing_factor' in var_name:
                    min_v, max_v = 1.1, 1.35   
                if 'outer_coils_3_spacing_factor' in var_name:
                    min_v, max_v = 0.85, 1.05           
                if 'outer_coils_4_spacing_factor' in var_name:
                    min_v, max_v = 0.75, 0.95
                if 'science_coils_spacing_factor' in var_name:
                    min_v, max_v = 0.95, 1.15
                if 'dur_transport' in var_name:
                    min_v, max_v = 1.2, 2
                    
                
                if min_v>max_v:
                    print('\n',var_name, min_v, max_v,'\n')
                var = max(min_v, min(max_v, var))
                if optimize_groupi in optimize_group:
                    dict[var_name] = {"min": min_v, "max": max_v, "start": var}

        print(str(dict).replace("'",'"'))
except Exception as e:
    print('no results', e, file)