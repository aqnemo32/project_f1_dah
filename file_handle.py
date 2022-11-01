#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 14:17:35 2022

@author: s1973088
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.optimize import curve_fit

def gauss(x, a, sig, mu):
    return a*np.exp(-np.square(x-mu)/(2*np.square(sig)))

def decay(x, a, b):
    return a*np.exp(x*b)

def main():
    # a = datetime.datetime.now()
    # import data
    # xmass = np.loadtxt(sys.argv[1])
    f = open("ups-15-small.bin","r")
    datalist = np.fromfile(f,dtype=np.float32)
    # number of events
    nevent = int(len(datalist)/6)
    xdata = np.split(datalist,nevent)
    
    # print(xdata[0])
    # make list of invariant mass of events
    xmass = np.zeros(nevent)
    mom_tran_pair =  np.zeros(nevent)
    rap = np.zeros(nevent)
    mom_pair = np.zeros(nevent)
    mom_tran_1 = np.zeros(nevent)
    mom_tran_2 = np.zeros(nevent)
    for i in range(0,nevent):
        xmass[i]=xdata[i][0]
        mom_tran_pair[i] = xdata[i][1]
        rap[i] = xdata[i][2]
        mom_pair[i] = xdata[i][3]
        mom_tran_1[i] = xdata[i][4]
        mom_tran_2[i] = xdata[i][5]
        
    
    f.close() 
    Min = np.min(xmass)
    Max = np.max(xmass)

    # b = datetime.datetime.now() - a
    # print(b)
    count , bins, patches = plt.hist(xmass, color = 'k', bins = 600, histtype= 'bar', range =(Min, Max), density=True )

    
    #histogram of the peaks from raw data
    bins_1 = []
    counts_1 = []
    bins_back = []
    counts_back= []
    bins_2 = []
    counts_2 = []
    bins_3 = []
    counts_3 = []

    
    for i,j in zip(bins, count):
        if i > 9.25 and i <9.7:
            bins_1.append(i)
            counts_1.append(j)
        elif i < 9.2 or i > 10.55:
            bins_back.append(i)
            counts_back.append(j)
        elif i < 9.8 and i > 9.7:
            bins_back.append(i)
            counts_back.append(j)
        elif i > 9.85 and i <10.15:
            bins_2.append(i)
            counts_2.append(j)
        elif i > 10.25 and i <10.45:
            bins_3.append(i)
            counts_3.append(j)
    
    print(f'{len(bins_1)}\n{len(counts_1)}')
        
    param_back, cov_back = curve_fit(decay, bins_back, counts_back)

    # back_sub = decay(np.array(bins_back), param_back[0], param_back[1])
    # plt.scatter(bins_back, back_sub, color = 'r')
    # plt.plot(bins, decay(np.array(bins), param_back[0], param_back[1]), color = 'b')
    # plt.show()
    # plt.clf()
    
    counts_clean = np.array(count) - decay(np.array(bins[1:]), param_back[0], param_back[1])
    
    counts_1_clean = np.array(counts_1) - decay(np.array(bins_1), param_back[0], param_back[1])
    counts_2_clean = np.array(counts_2) - decay(np.array(bins_2), param_back[0], param_back[1])
    counts_3_clean = np.array(counts_3) - decay(np.array(bins_3), param_back[0], param_back[1])
    
    
    param_1, cov_1 = curve_fit(gauss, bins_1, counts_1_clean, p0 = [15000, 0.3,9.5])
    param_2, cov_2 = curve_fit(gauss, bins_2, counts_2_clean, p0 = [5000, 0.3,10.1])
    param_3, cov_3 = curve_fit(gauss, bins_3, counts_3_clean, p0 = [2500, 0.3,10.35])
    
    count_1_fit = gauss(bins_1, param_1[0], param_1[1], param_1[2]) + decay(
        np.array(bins_1), param_back[0], param_back[1])
    count_2_fit = gauss(bins_2, param_2[0], param_2[1], param_2[2]) + decay(
        np.array(bins_2), param_back[0], param_back[1])
    count_3_fit = gauss(bins_3, param_3[0], param_3[1], param_3[2]) + decay(
        np.array(bins_3), param_back[0], param_back[1])
    
    
    
    # plt.plot(bins[1:], count)
    plt.plot(bins_1, count_1_fit)
    plt.plot(bins_2, count_2_fit)
    plt.plot(bins_3, count_3_fit)
    plt.show()
    plt.clf()
    
main()























