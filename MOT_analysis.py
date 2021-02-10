from __future__ import division
from lyse import *
from pylab import *
from analysislib.common import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = data(path)
run = Run(path)
# t0=0.228
t, MOT_fluorecence = run.get_trace('fluo')
plt.ylabel('current/A')
plt.xlabel('ms')
r = 10/0.24
plt.plot((t)*1e3, MOT_fluorecence*1e2,label='fluo')


t, MOT_fluorecence = run.get_trace('curr0')
plt.plot((t)*1e3, MOT_fluorecence*r, label='curr0')
final_current=np.mean(MOT_fluorecence[(len(t)//2):])*r
run.save_result('final_current', final_current)

t, MOT_fluorecence = run.get_trace('curr1')
plt.plot((t)*1e3, MOT_fluorecence*r, label='curr1')

t, MOT_fluorecence = run.get_trace('curr2')
plt.plot((t)*1e3, MOT_fluorecence*r, label='curr2')

t, MOT_fluorecence = run.get_trace('curr3')
plt.plot((t)*1e3, MOT_fluorecence*r*39.5/40, label='curr3')


rb = 17/69
t, MOT_fluorecence = run.get_trace('biasx')
plt.plot((t)*1e3, MOT_fluorecence*r*rb, label='biasx')

t, MOT_fluorecence = run.get_trace('biasy')
plt.plot((t)*1e3, MOT_fluorecence*r*rb, label='biasy')
plt.legend()

t, MOT_fluorecence = run.get_trace('Repump_monitor')
plt.plot((t)*1e3, MOT_fluorecence*500, label='Repump_monitor')
plt.legend()
t_roi_start, t_roi_end = int(np.round(0.6/(t[1]-t[0]))), int(np.round(1.8/(t[1]-t[0])))
Repump_avg = np.average(MOT_fluorecence[t_roi_start:t_roi_end])*500
run.save_result('MOT_repump_fluo', Repump_avg)
 

t, MOT_fluorecence = run.get_trace('Cooling_monitor')
plt.plot((t)*1e3, MOT_fluorecence*50, label='Cooling_monitor')
plt.legend()

# t, MOT_fluorecence = run.get_trace('B_sensor')
# plt.plot((t)*1e3, MOT_fluorecence*10, label='B_sensor')
# plt.legend()
