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

from functions import gauss, decay, double_gauss

def main():
    xmass = np.load('xmass.npy')
    
    Min = np.min(xmass)
    Max = np.max(xmass)

    # b = datetime.datetime.now() - a
    # print(b)
    count , bins, patches = plt.hist(xmass, color = 'k', bins = 600, histtype= 'bar', range =(Min, Max), density=True )


    #histogram of the peaks from raw data
    bins_1 = []
    count_1 = []
    bins_back = []
    count_back= []
    bins_2 = []
    count_2 = []
    bins_3 = []
    count_3 = []

    # setting up the peak and background parts of the histogram
    for i,j in zip(bins, count):
        # why does changing the limits of what can be qualified as the first peak, change the what gets appended to tails
        if i > 9.05 and i <9.7:
            bins_1.append(i)
            count_1.append(j)
        elif i < 9.2 or i > 10.55:
            bins_back.append(i)
            count_back.append(j)
        elif i < 9.8 and i > 9.7:
            bins_back.append(i)
            count_back.append(j)
        elif i > 9.85 and i <10.15:
            bins_2.append(i)
            count_2.append(j)
        elif i > 10.25 and i <10.45:
            bins_3.append(i)
            count_3.append(j)
    
    # print(f'{len(bins_1)}\n{len(count_1)}')
    # fitting the exponential decay of the background count
        
    # param_back, cov_back = curve_fit(decay, bins_back, count_back)

    # back_sub = decay(np.array(bins_back), param_back[0], param_back[1])
    # plt.scatter(bins_back, back_sub, color = 'r')
    # plt.plot(bins, decay(np.array(bins), param_back[0], param_back[1]), color = 'b')
    # plt.show()
    # plt.clf()
    
    # count_clean = np.array(count) - decay(np.array(bins[1:]), param_back[0], param_back[1])
    
    # count_1_clean = np.array(count_1) - decay(np.array(bins_1), param_back[0], param_back[1])
    # count_2_clean = np.array(count_2) - decay(np.array(bins_2), param_back[0], param_back[1])
    # count_3_clean = np.array(count_3) - decay(np.array(bins_3), param_back[0], param_back[1])
    
    param_1, cov_1 = curve_fit(gauss, bins_1, count_1, p0 = [10, 0.3,9.5])
    print()
    # tail = double_gauss(bins_1, 10, 0.2, 9.45, 2, 0.4, 9.45, param_1[0], param_1[1])
    # print(tail)
    tail = []
    count_tail = []
    center = []
    count_center = []
    for i,j in zip(bins_1, count_1):
        if i < param_1[2]-2*param_1[1] or i > param_1[2]+2*param_1[1]:
            tail.append(i)
            count_tail.append(j)
        elif i > param_1[2]-2*param_1[1] and i < param_1[2]+2*param_1[1]:
            center.append(i)
            count_center.append(j)
    print(center)
    param_1_d, cov_1_d = curve_fit(
        lambda x, a_1, mu_1, sig_1, a_2, mu_2, sig_2: 
        double_gauss(x, a_1, mu_1, sig_1, a_2, mu_2, sig_2, param_1[0], param_1[1]),
        bins_1, count_1,
        p0 = [10, 0.2, 9.45, 2, 0.4, 9.45], maxfev = 4000)
        
    
    print(param_1, param_1_d)
    # param_2, cov_2 = curve_fit(gauss, bins_2, count_2_clean, p0 = [5000, 0.3,10.1])
    # param_3, cov_3 = curve_fit(gauss, bins_3, count_3_clean, p0 = [2500, 0.3,10.35])
    
    count_1_fit = gauss(bins_1, param_1[0], param_1[1], param_1[2]) 
    count_1_d_fit = double_gauss(bins_1, param_1_d[0], param_1_d[1], param_1_d[2],
                    param_1_d[3], param_1_d[4], param_1_d[5], param_1[0], param_1[1]) 
    # count_2_fit = gauss(bins_2, param_2[0], param_2[1], param_2[2]) + decay(
    #     np.array(bins_2), param_back[0], param_back[1])
    # count_3_fit = gauss(bins_3, param_3[0], param_3[1], param_3[2]) + decay(
    #     np.array(bins_3), param_back[0], param_back[1])
    
    
    
    # plt.plot(bins[1:], count)
    plt.plot(bins_1, count_1_fit, '--', lw=2)
    plt.plot(bins_1, count_1_d_fit,'r', lw=1)
    # plt.plot(bins_2, count_2_fit)
    # plt.plot(bins_3, count_3_fit)
    plt.xlabel('Bin Count')
    plt.ylabel('Mass (units)')
    plt.show()
    plt.clf()
    
    plt.plot(tail,count_tail, label = 'tail')
    plt.plot(center, count_center, 'k', label = 'center')
    plt.legend()
    plt.show()
    plt.clf
    
    #Residual
    
    res_1 = count_1_fit - count_1
    res_1_d = count_1_d_fit - count_1
    res_1_d_sq = np.square(res_1_d)
    res_1_sq = np.square(res_1)
    # res_2 = count_2_fit - count_2
    # res_3 = count_3_fit - count_3
    
    r_sq_1 = 1 - (np.sum((count_1- count_1_fit)**2)/(np.sum((count_1-np.mean(count_1))**2)))
    r_sq_1_d = 1 - (np.sum((count_1- count_1_d_fit)**2)/(np.sum((count_1-np.mean(count_1))**2)))
    
    # print(f'single = {r_sq_1}\ndouble = {r_sq_1_d}\n{r_sq_1_d - r_sq_1}')
    # beta = 2
    # m = 5
    # crystal_1 = crystalball.pdf(bins_1, beta, m)
    # plt.plot(bins_1,crystal_1)
    # plt.show()
    # plt.clf()
    
    
    # plt.scatter(bins_1,res_1, marker = 'x', lw = 0.8, color = 'k')
    # plt.title('Residual plot for peak 1')
    # plt.xlabel('Mass')
    # plt.ylabel('Residual')
    # plt.show()
    # plt.clf()
    # plt.scatter(bins_1,res_1_sq, marker = 'o', lw = 1, color = 'k', label = 'gauss')
    # plt.scatter(bins_1,res_1_d_sq, marker = 'x', lw = 1, color = 'r', label = 'double gauss')
    # plt.title('Residual squared plot for peak 1')
    # plt.xlabel('Mass')
    # plt.ylabel('Residual')
    # plt.legend()
    # plt.show()
    # plt.clf()

a = datetime.datetime.now()    
main()
b = datetime.datetime.now() - a
print(b)
S


