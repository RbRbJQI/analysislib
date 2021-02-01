# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 15:09:03 2019

@author: Junheng Tao
"""

import numpy as np
from scipy import optimize
import h5py
import matplotlib.pyplot as plt

def gaussian(cx, cy, wx, wy, height, shift):
    return lambda x,y: height*np.exp((-((x-cx)/wx)**2-((y-cy)/wy)**2)/2)+shift


def guessparam(data,ct):
    dsum = np.nansum(data)
    x, y = np.indices(data.shape)
    center = [np.nansum(x*data)/dsum, np.nansum(y*data)/dsum]
    if min(center)<=0:
        center = ct
    width = [np.sqrt(abs(np.nansum((np.arange(data[:, int(c)].size)-c)**2*data[:, int(c)])/np.nansum(data[:, int(c)]))) for c in center]
    try:
        width = [np.sqrt(abs(np.nansum((np.arange(data[:, int(c)].size)-c)**2*data[:, int(c)])/np.nansum(data[:, int(c)]))) for c in center]
    except:
        center = ct
        width = [np.sqrt(abs(np.nansum(((np.arange(data[:, int(c)].size)-c)**2*data[:, int(c)]))/np.nansum(data[:, int(c)]))) for c in center]
    height = np.nanmax(data)
    for wi in range(2):
        if np.isnan(width[wi]) or width[wi]>len(data[:,wi]):
            width[wi] = width[abs(1-wi)]
    return center[0], center[1], width[0], width[1], height, 0

def fitgaussian2d(data, ct):
    try:
        params = np.array(guessparam(data, ct))
        print("guessfit",params)
        errorfunc = lambda p: np.ravel(gaussian(*p)(*np.indices(data.shape))-data)
        p, success = optimize.leastsq(errorfunc, params, maxfev=140)
        p[2:4] = abs(p[2:4]) #widths must be positive
        return p
    except Exception as e:
        print(e)
        return -np.ones(6)

def checkfit(data, params):
    x = int(params[0])
    y = np.indices(data[x,:].shape)
    plt.figure('fit:'+str(params))
    plt.plot(np.ravel(data[x,y]))
    plt.plot(np.ravel(gaussian(params[0],params[1],params[2],params[3],params[4],params[5])(x,y)))

def fitexpansion(data, t):
    try:
        params = [1,1]
        errorfunc = lambda p: np.ravel(expansion(*p)(t)-data)
        p, success = optimize.leastsq(errorfunc, params)
        return p
    except:
        return [-1,-1]

def fitfall(data, t):
    try:
        params = [220, -10000]
        errorfunc = lambda p: np.ravel(fall(*p)(t)-data)
        p, success = optimize.leastsq(errorfunc, params)
        return p
    except:
        return [-1,-1]
