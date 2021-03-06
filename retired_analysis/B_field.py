from __future__ import division
from lyse import *
from pylab import *
from analysislib.common import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = data(path)
run = Run(path)

from scipy.interpolate import interp1d

from labscriptlib.RbRb.transport import (
    Transport,
    piecewise_minjerk_and_coast,
    make_coils,
    lru_cache,
    linear,
    solve_two_coil,
    
)
from labscriptlib.RbRb.transport.currents import two_coil_zero_beta
from matplotlib import rc
rc('text', usetex=False)

BIAS_N_TURNS1 = df['BIAS_N_TURNS1']
BIAS_N_TURNS2 = df['BIAS_N_TURNS2']
INNER_TRANS_N_TURNS = df['INNER_TRANS_N_TURNS']
MOT_N_TURNS = df['MOT_N_TURNS']
MOT_coils_spacing_factor = df['MOT_coils_spacing_factor']
OUTER_TRANS_N_TURNS = df['OUTER_TRANS_N_TURNS']
SCIENCE_N_TURNS = df['SCIENCE_N_TURNS']
bias_ratio_yx = df['bias_ratio_yx']
d2beta_final_dy2_0 = df['d2beta_final_dy2_0']
d2beta_final_dy2_1 = df['d2beta_final_dy2_1']
d2beta_initial_dy2_0 = df['d2beta_initial_dy2_0']
d2beta_initial_dy2_1 = df['d2beta_initial_dy2_1']
dbeta_beginning_dy_0 = df['dbeta_beginning_dy_0']
final_switch_y_frac = df['final_switch_y_frac']
initial_switch_y_frac = df['initial_switch_y_frac']
inner_coils_0_spacing_factor = df['inner_coils_0_spacing_factor']
inner_coils_1_spacing_factor = df['inner_coils_1_spacing_factor']
inner_coils_2_spacing_factor = df['inner_coils_2_spacing_factor']
inner_coils_3_spacing_factor = df['inner_coils_3_spacing_factor']
move_dt_rel_1 = df['move_dt_rel_1']
move_dt_rel_2 = df['move_dt_rel_2']
move_dt_rel_3 = df['move_dt_rel_3']
move_dt_rel_4 = df['move_dt_rel_4']
move_dt_rel_5 = df['move_dt_rel_5']
move_dt_rel_6 = df['move_dt_rel_6']
move_final_current = df['move_final_current']
move_grad_0 = df['move_grad_0']
move_grad_1 = df['move_grad_1']
move_grad_2 = df['move_grad_2']
move_grad_3 = df['move_grad_3']
move_grad_4 = df['move_grad_4']
move_grad_5 = df['move_grad_5']
move_grad_6 = df['move_grad_6']
move_grad_7 = df['move_grad_7']
move_grad_8 = df['move_grad_8']
move_v_rel_3 = df['move_v_rel_3']
move_v_rel_5 = df['move_v_rel_5']
outer_coils_0_spacing_factor = df['outer_coils_0_spacing_factor']
outer_coils_1_spacing_factor = df['outer_coils_1_spacing_factor']
outer_coils_2_spacing_factor = df['outer_coils_2_spacing_factor']
outer_coils_3_spacing_factor = df['outer_coils_3_spacing_factor']
outer_coils_4_spacing_factor = df['outer_coils_4_spacing_factor']
science_coils_spacing_factor = df['science_coils_spacing_factor']
transport_time = df['dur_transport']
inner_coils_spacing_factors=(inner_coils_0_spacing_factor, inner_coils_1_spacing_factor, inner_coils_2_spacing_factor, inner_coils_3_spacing_factor)
outer_coils_spacing_factors=(outer_coils_0_spacing_factor , outer_coils_1_spacing_factor, outer_coils_2_spacing_factor, outer_coils_3_spacing_factor, outer_coils_4_spacing_factor)


# t0=0.228
t, MOT_fluorecence = run.get_trace('fluo')
plt.figure('curr_real')
# # plt.subplot(121)
plt.ylabel('current/A')
plt.xlabel('ms')
r = 10/0.24
plt.plot((t)*1e3, MOT_fluorecence*1e2,label='fluo')


t1, MOT_fluorecence = run.get_trace('curr1')
curr1 = MOT_fluorecence*r
plt.plot((t1)*1e3, MOT_fluorecence*r, label='curr1')

t2, MOT_fluorecence = run.get_trace('curr2')
curr2 = MOT_fluorecence*r
plt.plot((t2)*1e3, MOT_fluorecence*r, label='curr2')

t3, MOT_fluorecence = run.get_trace('curr3')
curr3 = MOT_fluorecence*r
plt.plot((t3)*1e3, MOT_fluorecence*r, label='curr3')

t0, MOT_fluorecence = run.get_trace('curr0')
curr0 = MOT_fluorecence*r
plt.plot((t0)*1e3, MOT_fluorecence*r, label='curr0')

rb = 17/69
t_biasx, MOT_fluorecence = run.get_trace('biasx')
biasx = MOT_fluorecence*r*rb
plt.plot((t_biasx)*1e3, MOT_fluorecence*r*rb, label='biasx')

t_biasy, MOT_fluorecence = run.get_trace('biasy')
biasy = MOT_fluorecence*r*rb
plt.plot((t_biasy)*1e3, MOT_fluorecence*r*rb, label='biasy')
plt.legend()

coils = make_coils(
    BIAS_N_TURNS1=BIAS_N_TURNS1,
    BIAS_N_TURNS2=BIAS_N_TURNS2,
    MOT_N_TURNS=MOT_N_TURNS,
    SCIENCE_N_TURNS=SCIENCE_N_TURNS,
    INNER_TRANS_N_TURNS=INNER_TRANS_N_TURNS,
    OUTER_TRANS_N_TURNS=OUTER_TRANS_N_TURNS,
    MOT_coils_spacing_factor=MOT_coils_spacing_factor,
    science_coils_spacing_factor=science_coils_spacing_factor,
    inner_coils_spacing_factors=inner_coils_spacing_factors,
    outer_coils_spacing_factors=outer_coils_spacing_factors,
)
transport_trajectory = piecewise_minjerk_and_coast(
    0,
    transport_time,
    0,
    coils['science'].y,# - move_y_final_offset,
    1.0,  # Relative duration of initial accelerating segment, 1 by definition
    (move_dt_rel_1, 1.0),  # vrel in first coasting segment, 1 by definition
    move_dt_rel_2,
    (move_dt_rel_3, move_v_rel_3),
    move_dt_rel_4,
    (move_dt_rel_5, move_v_rel_5),
    move_dt_rel_6
)
move_grad_final = coils['science'].dB(coils['science'].r0, move_final_current, 'z')[2]

transport_gradient_ramp = interp1d(
    np.linspace(0, transport_time, 10),
    [
        move_grad_0,#=0.44,
        move_grad_1,#=1.61,
        move_grad_2,#=1.89,
        move_grad_3,#=1.99,
        move_grad_4,#=2.06,
        move_grad_5,#=1.92,
        move_grad_6,#=1.61,
        move_grad_7,#=1.26,
        move_grad_8,#=1.01,
        move_grad_final,
    ],
    'cubic',
    fill_value='extrapolate',
)
transport = Transport(
    coils=coils,
    y_of_t=transport_trajectory,
    t_final=transport_time,
    dBz_dz_of_t=transport_gradient_ramp,
    initial_switch_y_frac=initial_switch_y_frac,
    d2beta_initial_dy2_0=d2beta_initial_dy2_0,
    d2beta_initial_dy2_1=d2beta_initial_dy2_1,
    final_switch_y_frac=final_switch_y_frac,
    d2beta_final_dy2_1=d2beta_final_dy2_1,
    d2beta_final_dy2_0=d2beta_final_dy2_0,
    dbeta_beginning_dy_0 = dbeta_beginning_dy_0
)


ys = transport.y_of_t
t_start = 1.659
switch = transport.t_switchover 
switch.insert(0, 0)
switch = np.array(switch)+ t_start

def Curr_t(t, Curr, t_array):
    ind = np.argwhere(t_array>t+t_start)[0]-1
    # print (ind) 
    return Curr[ind]
    
def Channel_n(n):
    if n==0:
        return biasx, t_biasx
    if n in [1,5,9]:
        return curr0, t0
    if n in [2,6]:
        return curr1, t1
    if n in [3,7,10]:
        return curr2, t2
    if n in [4,8,11]:
        return np.array(curr3), t3

def B3coil(t_y, n1, n2, n3):
    coil1, coil2, coil3=coils[n1], coils[n2], coils[n3]
    y=ys(t_y)
    print('transport distance:',y)
    I_1,t_1=Channel_n(n1)
    I_2,t_2=Channel_n(n2)
    I_3,t_3=Channel_n(n3)
    I1, I2, I3 = Curr_t(t_y, I_1, t_1), Curr_t(t_y, I_2, t_2), Curr_t(t_y, I_3, t_3)
    # print ('I1',I1,'I2',I2,'I3',I3)
    B1=coil1.B( (0,y,0), I1  )
    # print ('B1',B1)
    B2=coil2.B( (0,y,0), I2 )
    B3=coil3.B( (0,y,0), I3 )
    B_tot = B1+B2+B3
    _, _, dB1z_dz = coil1.dB((0, y, 0), I=I1, s='z')
    _, _, dB2z_dz = coil2.dB((0, y, 0), I=I2, s='z')
    _, _, dB3z_dz = coil3.dB((0, y, 0), I=I3, s='z')
    _, dB1y_dy, _ = coil1.dB((0, y, 0), I=I1, s='y')
    _, dB2y_dy, _ = coil2.dB((0, y, 0), I=I2, s='y')
    _, dB3y_dy, _ = coil3.dB((0, y, 0), I=I3, s='y')
    dBdz=dB1z_dz+dB2z_dz+dB3z_dz
    dBdy=dB1y_dy+dB2y_dy+dB3y_dy
    beta = - dBdz/dBdy
    return B_tot, beta
    

t_t, Bx_t, By_t, Bz_t, beta_t=[],[],[],[],[]
    
for n in range(len(switch)-1):
    for t_iter in np.linspace(switch[n],switch[n+1],5):
        print('transport time:',t_iter-t_start)
        B_t, beta=B3coil(t_iter-t_start, n, n+1, n+2)
        t_t.append(t_iter)
        Bx_t.append(B_t[0][0])
        By_t.append(B_t[1][0])
        Bz_t.append(B_t[2][0])
        beta_t.append(beta)
        
plt.figure('beta_t')
plt.plot(t_t,beta_t,label='beta')
plt.figure('Bxyz_t')
# Bx_t = np.flatten(Bx_t)
# print(Bx_t, 'this is it')
plt.plot(t_t,Bx_t,label='Bx')           
plt.plot(t_t,By_t,label='By')           
plt.plot(t_t,Bz_t,label='Bz')           
plt.legend()


#theory curve
curr = transport.currents_at_time(0.6)
tt = np.linspace(0,transport_time,200)
fig, ax = plt.subplots()
figure('theorycurr')
cc = transport.currents_at_time(tt)
for ncoil in range(len(curr)):
    ax.plot(tt, cc[ncoil], label=str(ncoil))
    ax.legend(ncol=2)
figure('beta')
plot(ys(tt), transport.beta_ramp(tt))
figure('beta_real')
plot(tt, transport.real_beta)
figure('dbdz')
plot(tt, transport.dBz_dz_of_t(tt),label='dbdz')
plot(tt,transport.dBz_dz_of_t(tt)/transport.real_beta,label='dbdx')
plt.legend()
plt.title('dbdx_min='+str(np.min(transport.dBz_dz_of_t(tt)/transport.real_beta)))
