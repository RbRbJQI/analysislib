from __future__ import division
from lyse import *
from pylab import *
from analysislib.common import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = data(path)
run = Run(path)


t, MOT_fluorecence = run.get_trace('curr0')
max_fluo = max(MOT_fluorecence)
t_start = 2292
min_fluo = min(MOT_fluorecence[t_start:])
MOT_fluorecence[t_start:] -= min_fluo*np.ones(len(MOT_fluorecence[t_start:]))
print(MOT_fluorecence[t_start])

plt.plot(MOT_fluorecence[t_start:], label='curr0')
plt.title('slope= '+str((MOT_fluorecence[-1]-MOT_fluorecence[t_start])) )
