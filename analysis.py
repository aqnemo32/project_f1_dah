#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 22:47:32 2022

@author: achilequarante
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime

from functions import *

def main():
    xmass = np.load('ups_anal/xmass.npy')

    
    Min = np.min(xmass)
    Max = np.max(xmass)
    _, n_bins = np.modf((Max-Min)/freedman(xmass))
    
    count , bins_w, patches = plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'bar', range =(Min, Max), density=True )
    bins = bins_w[1:] - (bins_w[1] - bins_w[0])/2

    #histogram of the peaks from raw data
    bins_1 = bins[(bins > 9.2) & (bins < 9.7)]
    count_1 = count[(bins > 9.2) & (bins < 9.7)]
    bins_back = np.concatenate((bins[(bins < 9.2) | (bins > 10.55)], bins[(bins > 9.7) & (bins < 9.8)]))
    count_back= np.concatenate((count[(bins < 9.2) | (bins > 10.55)], count[(bins > 9.7) & (bins < 9.8)]))
    bins_2 = bins[(bins > 9.85) & (bins < 10.15)]
    count_2 = count[(bins > 9.85) & (bins < 10.15)]
    bins_3 = bins[(bins > 10.25) & (bins < 10.45)]
    count_3 = count[(bins > 10.25) & (bins < 10.45)]
# hello there
    # setting up the peak and background parts of the histogram

    
    print(f'{len(bins_1)}\n{len(count_1)}')
    # fitting the exponential decay of the background count
        
    param_back, cov_back = curve_fit(decay, bins_back, count_back)

    # back_sub = decay(np.array(bins_back), param_back[0], param_back[1])
    # plt.scatter(bins_back, back_sub, color = 'r')
    # plt.plot(bins, decay(np.array(bins), param_back[0], param_back[1]), color = 'b')
    # plt.show()
    # plt.clf()
    
    count_clean = count - decay(bins, param_back[0], param_back[1])
    
    count_1_clean = count_1 - decay(bins_1, param_back[0], param_back[1])
    count_2_clean = count_2 - decay(bins_2, param_back[0], param_back[1])
    count_3_clean = count_3 - decay(bins_3, param_back[0], param_back[1])
    
    
    param_1, cov_1 = curve_fit(gauss, bins_1, count_1_clean, p0 = [10, 9.45, 0.03])
    param_2, cov_2 = curve_fit(gauss, bins_2, count_2_clean, p0 = [10, 10.0, 0.03])
    param_3, cov_3 = curve_fit(gauss, bins_3, count_3_clean, p0 = [10, 10.27, 0.03])
    
    
    print(f"A, mu, sig =  {param_1}")

    
    count_1_fit = gauss(bins_1, param_1[0], param_1[1], param_1[2]) + decay(
        bins_1, param_back[0], param_back[1])

    count_2_fit = gauss(bins_2, param_2[0], param_2[1], param_2[2]) + decay(
        bins_2, param_back[0], param_back[1])
    
    count_3_fit = gauss(bins_3, param_3[0], param_3[1], param_3[2]) + decay(
        bins_3, param_back[0], param_back[1])
    
    
    
    
    
    # plt.plot(bins[1:], count)
    plt.plot(bins_1, count_1_fit, '--', lw = 2, color = 'r')
    plt.plot(bins_2, count_2_fit, '--', lw = 2, color = 'b')
    plt.plot(bins_3, count_3_fit, '--', lw = 2, color = 'g')
    # plt.plot(bins_2, count_2_fit)
    # plt.plot(bins_3, count_3_fit)
    plt.xlabel('Bin Count')
    plt.ylabel('Mass (units)')
    plt.show()
    plt.clf()
    
    #Residual
    
    res_1 = count_1_fit - count_1
    res_1_sq = np.square(res_1)
    # res_2 = count_2_fit - count_2
    # res_3 = count_3_fit - count_3
    
    r_sq_1 = 1 - (np.sum((count_1- count_1_fit)**2)/(np.sum((count_1-np.mean(count_1))**2)))
    print(f"R^2 = {r_sq_1}")
    
    
    #CRYSTAL BALL FUNC
    
    # beta = 2
    # m = 5
    # crys_param, cryst_cov = curve_fit(crystalball, bins_back, count_back)
    # print(crys_param)
    # plt.plot(bins_1,crystal_1)
    # plt.show()
    # plt.clf()
    ###
    
    # plt.scatter(bins_1,res_1, marker = 'x', lw = 0.8, color = 'k')
    # plt.title('Residual plot for peak 1')
    # plt.xlabel('Mass')
    # plt.ylabel('Residual')
    # plt.show()
    # plt.clf()
    plt.scatter(bins_1,res_1_sq, marker = 'o', lw = 1, color = 'k', label = 'gauss')
    plt.title('Residual squared plot for peak 1')
    plt.xlabel('Mass')
    plt.ylabel('Residual')
    plt.legend()
    plt.show()
    plt.clf()

a = datetime.datetime.now()    
main()
b = datetime.datetime.now() - a
print(b)


