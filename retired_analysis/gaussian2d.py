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
    # return lambda x,y: height*np.exp(-np.sqrt((x-cx)**2/wx**2+(y-cy)**2/wy**2))+shift
    
# class Mask(object):
    # def __init__(self, ct, rad):
        # self.ct = ct
        # self.rad = rad
    # def ifin(self, a,b,c,d,e,f):
        # return lambda x,y:(x-self.ct[0])**2 + (y-self.ct[1])**2 < self.rad**2
        
# def showmask(data,mask):
    # data1 = np.copy(data)
    # for x in range(len(data)):
        # for y in range(len(data[0])):
            # data1[x,y] = data[x,y]*(np.abs((x-mask.ct[0])**2 + (y-mask.ct[1])**2 - mask.rad**2)>9) + 100*(np.abs((x-mask.ct[0])**2 + (y-mask.ct[1])**2 - mask.rad**2)<9)
    # return data1

def guessparam(data,ct):
    dsum = data.sum()
    x, y = np.indices(data.shape)
    center = [(x*data).sum()/dsum, (y*data).sum()/dsum]
    if min(center)<=0:
        center = ct
    width = [np.sqrt(abs((np.arange(data[:, int(c)].size)-c)**2*data[:, int(c)]).sum()/data[:, int(c)].sum()) for c in center]
    try:
        width = [np.sqrt(abs(((np.arange(data[:, int(c)].size)-c)**2*data[:, int(c)]).sum()/data[:, int(c)].sum())) for c in center]
    except:
        center = ct
        width = [np.sqrt(abs(((np.arange(data[:, int(c)].size)-c)**2*data[:, int(c)]).sum()/data[:, int(c)].sum())) for c in center]
    height = data.max()
    for wi in range(2):
        if np.isnan(width[wi]):
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
