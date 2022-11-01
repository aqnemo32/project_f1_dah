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
    return a*np.exp(np.square(x-mu)/(2*np.square(sig)))

def decay(x, a, b):
    return a*np.exp(x*b)

def main():
    # a = datetime.datetime.now()
    # import data
    # xmass = np.loadtxt(sys.argv[1])
    f = open("ups-15.bin","r")
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
    count , bins, patches = plt.hist(xmass, color = 'k', bins = 600, histtype= 'bar', range =(Min, Max) )

    
    #histogram of the peaks from raw data
    bins_1 = []
    counts_1 = []
    bins_back = []
    counts_back= []
    # bins_2 = []
    # counts_2 = []
    # bins_3 = []
    # counts_3 = []

    
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
        
        # elif binedge1[i] > 9.85 and binedge1[i]<10.15:
        #     bins_2.append(binedge1[i])
        #     counts_2.append(count[i])      
        # elif binedge1[i] > 10.25 and binedge1[i]<10.45:
        #     bins_3.append(binedge1[i])
        #     counts_3.append(count[i])
        
    param_back, cov_back = curve_fit(decay, bins_back, counts_back)

    back_sub = decay(np.array(bins_back), param_back[0], param_back[1])
    plt.scatter(bins_back, back_sub, color = 'r')
    plt.plot(bins, decay(np.array(bins), param_back[0], param_back[1]), color = 'b')
    plt.show()
    plt.clf()
    counts_clean = np.array(count) - decay(np.array(bins[1:]), param_back[0], param_back[1])
    plt.plot(bins[1:], counts_clean)
    plt.show()
    plt.clf()
main()