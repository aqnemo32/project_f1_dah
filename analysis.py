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
    xmass_raw = np.load('ups_anal/xmass.npy')
    tran_1_ups = np.load('ups_anal/mom_tran_1.npy')
    tran_2_ups = np.load('ups_anal/mom_tran_2.npy')


    
    # R is the absolute value of the difference in transverse momentum divided by the sum in transverse momentum (from 0 to 1)

    R = np.absolute(tran_2_ups - tran_1_ups)/(tran_2_ups + tran_1_ups)
    # Using R we clean the data in such a way that the purity of the peaks in the histogram is increased
    xmass = xmass_raw[R<0.42]

    Min = np.min(xmass)
    Max = np.max(xmass)
    _, n_bins = np.modf((Max-Min)/freedman(xmass_raw))
    
    count , bins_w, patches = plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'step', range =(Min, Max), density=False )
    bins = bins_w[1:] - (bins_w[1] - bins_w[0])/2

    #histogram of the peaks from raw data

    bins_1 = bins[(bins > 9.1) & (bins < 9.7)]
    count_1 = count[(bins > 9.1) & (bins < 9.7)]

    bins_2 = bins[(bins > 9.85) & (bins < 10.175)]
    count_2 = count[(bins > 9.85) & (bins < 10.175)]

    bins_3 = bins[(bins >= 10.175) & (bins < 10.55)]
    count_3 = count[(bins >= 10.175) & (bins < 10.55)]

    bins_back = np.concatenate((bins[(bins <= 9.1) | (bins >= 10.55)], bins[(bins >= 9.7) & (bins <= 9.85)]))
    count_back= np.concatenate((count[(bins <= 9.1) | (bins >= 10.55)], count[(bins >= 9.7) & (bins <= 9.85)]))

    # setting up the peak and background parts of the histogram

    # fitting the exponential decay of the background count
        
    param_back, cov_back = curve_fit(decay, bins_back, count_back)
    print(param_back)
    back_prime = decay(bins_back, param_back[0], param_back[1])
    background = decay(bins, param_back[0], param_back[1])

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
    param_3, cov_3 = curve_fit(gauss, bins_3, count_3_clean, p0 = [10, 10.27, 0.02])
    

    
    count_1_fit = gauss(bins_1, param_1[0], param_1[1], param_1[2]) + decay(
        bins_1, param_back[0], param_back[1])
    
    mu_1 = param_1[1]
    sig_1 = param_1[2]

    count_2_fit = gauss(bins_2, param_2[0], param_2[1], param_2[2]) + decay(
        bins_2, param_back[0], param_back[1])

    mu_2 = param_2[1]
    sig_2 = param_2[2]
    
    count_3_fit = gauss(bins_3, param_3[0], param_3[1], param_3[2]) + decay(
        bins_3, param_back[0], param_back[1])

    mu_3 = param_3[1]
    sig_3 = param_3[2]

    peaks = gauss(bins, param_1[0], param_1[1], param_1[2]) + gauss(bins, param_2[0], param_2[1], param_2[2]) + gauss(bins, param_3[0], param_3[1], param_3[2])

    count_gauss = peaks + background
    
    

    plt.plot (bins, count_gauss, '--', lw = 2, color = 'r')
    plt.ylabel('Bin Count')
    plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
    plt.show()
    plt.clf()
    
    #Residual
    
    res_gauss = count_gauss - count
    sum_res_sq_gauss = np.sum(np.square(res_gauss))
    # res_2 = count_2_fit - count_2
    # res_3 = count_3_fit - count_3
    
    # DOUBLE GAUSSIAN
    # peak 1
    tail_1st_1, count_tail_1st_1, center_1, count_center_1, tail_2nd_1, count_tail_2nd_1 = peak_split(bins_1, count_1_clean, mu_1, sig_1)
    
    

    tail_1 = np.concatenate((tail_1st_1, tail_2nd_1))
    count_tail_1 = np.concatenate((count_tail_1st_1, count_tail_2nd_1))



    param_tail_1, cov_t = curve_fit(gauss, tail_1, count_tail_1, p0 = [5000, 9.45, 0.04], maxfev = 1600)
    param_center_1, cov_c = curve_fit(gauss, center_1, count_center_1, p0= [10000, 9.45, 0.01])
    
    
    tail_fit_1 = gauss(tail_1, param_tail_1[0], param_tail_1[1], param_tail_1[2])
    center_fit_1 = gauss(center_1, param_center_1[0], param_center_1[1], param_center_1[2])

    double_gauss_fit_1 = np.concatenate((tail_fit_1[tail_1 < mu_1], center_fit_1, tail_fit_1[tail_1 > mu_1])) + decay(bins_1, param_back[0], param_back[1])


    # peak 2
    tail_1st_2, count_tail_1st_2, center_2, count_center_2, tail_2nd_2, count_tail_2nd_2 = peak_split(bins_2, count_2_clean, mu_2, sig_2)

    tail_2 = np.concatenate((tail_1st_2, tail_2nd_2))
    count_tail_2 = np.concatenate((count_tail_1st_2, count_tail_2nd_2))
    
    param_tail_2, cov_t = curve_fit(gauss, tail_2, count_tail_2, p0 = [1000, 10.0, 0.04], maxfev = 1600)
    param_center_2, cov_c = curve_fit(gauss, center_2, count_center_2, p0= [2000, 10.0, 0.01])
    
    
    tail_fit_2 = gauss(tail_2, param_tail_2[0], param_tail_2[1], param_tail_2[2])
    center_fit_2 = gauss(center_2, param_center_2[0], param_center_2[1], param_center_2[2])

    double_gauss_fit_2 = np.concatenate((tail_fit_2[tail_2 < mu_2], center_fit_2, tail_fit_2[tail_2 > mu_2])) + decay(bins_2, param_back[0], param_back[1])

    # peak 3
    print(sig_3)
    tail_1st_3, count_tail_1st_3, center_3, count_center_3, tail_2nd_3, count_tail_2nd_3 = peak_split(bins_3, count_3_clean, mu_3, np.absolute(sig_3))



    tail_3= np.concatenate((tail_1st_3, tail_2nd_3))
    count_tail_3 = np.concatenate((count_tail_1st_3, count_tail_2nd_3))
    
    param_tail_3, cov_t = curve_fit(gauss, tail_3, count_tail_3, p0 = [500, mu_3, 0.04], maxfev = 1600)
    param_center_3, cov_c = curve_fit(gauss, center_3, count_center_3, p0= [1000, mu_3, 0.01])
    
    
    tail_fit_3 = gauss(tail_3, param_tail_3[0], param_tail_3[1], param_tail_3[2])
    center_fit_3 = gauss(center_3, param_center_3[0], param_center_3[1], param_center_3[2])

    double_gauss_fit_3 = np.concatenate((tail_fit_3[tail_3 < mu_3], center_fit_3, tail_fit_3[tail_3 > mu_3])) + decay(bins_3, param_back[0], param_back[1])

    count_double_gauss = np.concatenate((back_prime[bins_back <= bins_1[0]],
     double_gauss_fit_1,
     back_prime[(bins_back >= bins_1[-1]) & (bins_back <= bins_2[0])],
     double_gauss_fit_2,
     back_prime[(bins_back >= bins_2[-1]) & (bins_back <= bins_3[0])],
     double_gauss_fit_3,
     back_prime[bins_back >= bins_3[-1]]))

    plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'step', range =(Min, Max), density=False )
    plt.plot(bins, count_double_gauss)
    plt.show()
    plt.clf()
    
    #CRYSTAL BALL FUNC

    # fitting the peaks to crystall ball functions using scipy.curve_fit
    param_crys_1, cryst_cov_1 = curve_fit(crystalball, 
        bins_1, count_1_clean, p0 = [1.88, 0.9, 9.456127695, 0.043517612], maxfev = 8000)

    crystal_1 = crystalball(bins, param_crys_1[0], param_crys_1[1], param_crys_1[2], param_crys_1[3])

    param_crys_2, cryst_cov_2 = curve_fit(crystalball, 
        bins_2, count_2_clean, p0 = [1.5, 0.9, 10.0, 0.043517612], maxfev = 8000)
    
    crystal_2 = crystalball(bins, param_crys_2[0], param_crys_2[1], param_crys_2[2], param_crys_2[3])

    param_crys_3, cryst_cov_3 = curve_fit(crystalball, 
        bins_3, count_3_clean, p0 = [1.5, 0.8, 10.35, 0.043517612], maxfev = 8000)

    crystal_3 = crystalball(bins, param_crys_3[0], param_crys_3[1], param_crys_3[2], param_crys_3[3])


    peaks_cb = crystal_1 + crystal_2 + crystal_3
    count_cb = peaks_cb + background

    plt.plot(bins,count_cb)
    plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'step', range =(Min, Max), density=False )
    plt.xlabel('Mass')
    plt.ylabel('Count')
    plt.title('Crystall Ball Fit')
    plt.show()
    plt.clf()
    
    res_crystal = count_cb - count
    sum_res_sq_crystal = np.sum(np.square(res_crystal))
    # plt.scatter(bins_1,res_1, marker = 'x', lw = 0.8, color = 'k')
    # plt.title('Residual plot for peak 1')
    # plt.xlabel('Mass')
    # plt.ylabel('Residual')
    # plt.show()
    # plt.clf()
    plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'step', range =(Min, Max), density=False )
    back_sub = decay(np.array(bins_back), param_back[0], param_back[1])
    plt.scatter(bins_back, back_sub, color = 'r')
    plt.plot(bins, decay(np.array(bins), param_back[0], param_back[1]), color = 'b')
    plt.show()
    plt.clf()
    print(f"{sum_res_sq_gauss/sum_res_sq_crystal = }")

    chi_sq_gauss = chi_sq(count_gauss, count)
    chi_sq_d_gauss = chi_sq(count_double_gauss, count)
    chi_sq_cb = chi_sq(count_cb, count)

    print(f"{chi_sq_gauss = :.5}\n{chi_sq_d_gauss = :.5}\n{chi_sq_cb = :.5}")


a = datetime.datetime.now()    
main()
b = datetime.datetime.now() - a
print(b)


