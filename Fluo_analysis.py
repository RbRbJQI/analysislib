from __future__ import division
from lyse import *
from pylab import *
from analysislib.common import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = data(path)
run = Run(path)
t, MOT_fluorecence = run.get_trace('curr1')
plt.figure('curr')
plt.ylabel('curr')
plt.xlabel('ms')
r = 10/0.24
plt.plot((t)*1e3, r*MOT_fluorecence)
