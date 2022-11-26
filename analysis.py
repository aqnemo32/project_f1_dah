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
    xmass_raw = np.load('ups_big_anal/xmass_big.npy')
    tran_1_ups = np.load('ups_big_anal/mom_tran_1_big.npy')
    tran_2_ups = np.load('ups_big_anal/mom_tran_2_big.npy')


    
    # R is the absolute value of the difference in transverse momentum divided by the sum in transverse momentum (from 0 to 1)

    R = np.absolute(tran_2_ups - tran_1_ups)/(tran_2_ups + tran_1_ups)
    # Using R we clean the data in such a way that the purity of the peaks in the histogram is increased
    xmass = xmass_raw[R<0.42]

    Min_raw = np.min(xmass_raw)
    Max_raw = np.max(xmass_raw)

    _, n_bins = np.modf((Max_raw - Min_raw)/freedman(xmass_raw))
    n_bins = int(n_bins*2)
    print(n_bins)
    

    Min = np.min(xmass)
    Max = np.max(xmass)

    n_bins = (Max_raw - Min_raw)/0.0014454397963081789
    print(n_bins)

    count , bins_w, patches = plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'step', range =(Min, Max), density=False )
    plt.clf()
    print(bins_w[1]-bins_w[0])
    bins = bins_w[1:] - (bins_w[1] - bins_w[0])/2

    #histogram of the peaks from raw data
    bool_1 = (bins > 9.2) & (bins < 9.7)

    bins_1 = bins[bool_1]
    count_1 = count[bool_1]

    bool_2 = (bins > 9.85) & (bins < 10.175)

    bins_2 = bins[bool_2]
    count_2 = count[bool_2]

    bool_3 = (bins >= 10.175) & (bins < 10.55)

    bins_3 = bins[bool_3]
    count_3 = count[bool_3]

    bool_back_1 = (bins <= 9.2) | (bins >= 10.55)
    bool_back_2 = (bins >= 9.7) & (bins <= 9.85)

    bins_back = np.concatenate((bins[bool_back_1], bins[bool_back_2]))
    count_back = np.concatenate((count[bool_back_1], count[bool_back_2]))

    # setting up the peak and background parts of the histogram

    # fitting the exponential decay of the background count
        
    param_back, cov_back = curve_fit(decay, bins_back, count_back)

    background = decay(bins, param_back[0], param_back[1])

    
    count_clean = count - decay(bins, param_back[0], param_back[1])
    
    count_1_clean = count_1 - decay(bins_1, param_back[0], param_back[1])
    count_2_clean = count_2 - decay(bins_2, param_back[0], param_back[1])
    count_3_clean = count_3 - decay(bins_3, param_back[0], param_back[1])
    


    # GAUSSIAN and DECAY fitted simultaneously

    # fitting the singular peaks as gaussians and decay simultaneously to get estaimates before fitting all three peaks and decay as one
    bool_1_p = (bins<9.7)
    
    bool_2_p = (bins >= 9.7) & (bins < 10.175)

    bool_3_p = (bins >= 10.175)

    param_1_s, cov_1_d = curve_fit(
        gauss, bins[bool_1_p], count_clean[bool_1_p], p0 = [10, 9.45, 0.03])

    mu_1 = param_1_s[1]
    sig_1 = param_1_s[2]

    param_2_s, cov_2_d = curve_fit(
        gauss, bins[bool_2_p] , count_clean[bool_2_p] , p0 = [8, 10.0, 0.03])

    mu_2 = param_2_s[1]
    sig_2 = param_2_s[2]

    param_3_s, cov_3_d = curve_fit(
        gauss, bins[bool_3_p], count_clean[bool_3_p], p0 = [400, 10.27, 0.03], maxfev = 20000)

    mu_3 = param_3_s[1]
    sig_3 = param_3_s[2]

    # fitting all three peaks and the decay as one
    def func_xtreme(x, a, b, c, d, e, f, g, h, i, j, k):
        '''
        combines three gaussians and the background decay into one function where all the parameters are fitted in one go
        '''
        return (gauss(x,a,b,c) + gauss(x,d,e,f) + gauss(x,g,h,i) + decay(x,j,k))

    param_f_s, cov_f_d = curve_fit(func_xtreme, bins, count,
     p0 = [param_1_s[0], param_1_s[1], param_1_s[2],
      param_2_s[0], param_2_s[1],param_2_s[2],
       param_3_s[0], param_3_s[1], param_3_s[2],
       param_back[0], param_back[1]], maxfev = 10000)
    a = param_f_s

    print(a)

    gauss_fit = func_xtreme(bins, a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10])

    
    plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'step', range =(Min, Max), density=False, label = 'Raw Data')
    plt.plot(bins, gauss_fit, color = 'r', linestyle = '--', label = 'Fit')
    plt.ylabel('Count')
    plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
    plt.title('Histogram for Muon Mass Pair (Gaussian)')
    plt.legend()
    plt.show()
    plt.clf()

    # DOUBLE GAUSSIAN

    # peak 1
    param_1_d, cov_1_d = curve_fit(
        double_gauss, bins[bool_1_p], count_clean[bool_1_p], p0 = [1.91137114e+04,  9.45630388e+00,  3.56317664e-02,  6.72576220e-02,
        7.65411217e-01])

    print(f"{param_1_d = }")

    param_2_d, cov_2_d = curve_fit(
        double_gauss, bins[bool_2_p], count_clean[bool_2_p], p0 = [5.21651280e+03,  1.00190049e+01,  4.55571720e-02,
        0.06,  8.04943465e-01], maxfev = 20000)

    print(f"{param_2_d = }")

    param_3_d, cov_3_d = curve_fit(
        double_gauss, bins[bool_3_p], count_clean[bool_3_p], p0 = [5000, 10.3, 0.03, 0.3, 0.5], maxfev = 20000)
    
    print(f"{param_3_d = }")

    def func_x_xtreme(x, a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q):
        '''
        Sum of three double gaussiand and expoentitla decay to create one big PDF
        '''
        return double_gauss(x, a,b,c,d,e) + double_gauss(x, f,g,h,i,j) + double_gauss(x, k,l,m,n,o) + decay(x, p,q)

    param_f_d, cov_f_d = curve_fit(func_x_xtreme, bins, count,
     p0 = [param_1_d[0], param_1_d[1], param_1_d[2], param_1_d[3], param_1_d[4],
      param_2_d[0], param_2_d[1], param_2_d[2], param_2_d[3], param_2_d[4],
       param_3_d[0], param_3_d[1], param_3_d[2], param_3_d[3], param_3_d[4],
       param_back[0], param_back[1]], maxfev = 10000)

    b = param_f_d

    print(f"{b = }\n{cov_f_d.diagonal() = }")

    error_d_gauss_param = np.sqrt(cov_f_d.diagonal())/n_bins
    print(error_d_gauss_param)

    double_gauss_fit = func_x_xtreme(bins,
     b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10] ,b[11] ,b[12] ,b[13], b[14], b[15], b[16])
    
    
    plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'step', range =(Min, Max), density=False, label = 'Raw Data' )
    plt.plot(bins, double_gauss_fit, color = 'r', linestyle = '--',label = 'Fit')
    plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
    plt.ylabel('Count')
    plt.title('Histogram of Muon Mass pair (Double Gaussian)')
    plt.legend()
    plt.show()
    plt.clf()
    
    #CRYSTAL BALL FUNC
    # alpha and n are fixed, based on the monte carlo analysis

    # fitting the peaks to crystall ball functions using scipy.curve_fit
    param_crys_1, cryst_cov_1 = curve_fit(fix_crystalball, 
        bins_1, count_1_clean, p0 = [mu_1, sig_1], maxfev = 80000)
    
    print(param_crys_1)
    

    

    param_crys_2, cryst_cov_2 = curve_fit(fix_crystalball, 
        bins_2, count_2_clean, p0 = [mu_2, sig_1 * mu_2/mu_1], maxfev = 80000)
    
    
    print(param_crys_2)

    param_crys_3, cryst_cov_3 = curve_fit(fix_crystalball, 
        bins_3, count_3_clean, p0 = [mu_3, sig_3 * mu_3/mu_1], maxfev = 80000)

    print(param_crys_3)



    def simul_cb_decay(x, a,b,c,d,e,f,g,h):
        '''
        '''
        return fix_crystalball(x, a,b) + fix_crystalball(x, c,d) + fix_crystalball(x, e,f) + decay(x, g,h)

    param_cb_dec, cov_cb_dec = curve_fit(simul_cb_decay, bins, count, 
    p0 = [param_crys_1[0], param_crys_1[1], param_crys_2[0], param_crys_2[1], param_crys_3[0], param_crys_3[1], 4000, -0.6], 
    maxfev = 80000,)

    print(f"{param_cb_dec = }")

    c = param_cb_dec
    crystal_ball_fit = simul_cb_decay(bins, c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7])

    plt.plot(bins,crystal_ball_fit, color = 'r', linestyle = '--', label = 'Fit')
    plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'step', range =(Min, Max), density=False, label = 'Raw Data')
    plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
    plt.ylabel('Count')
    plt.title('Histogram of Muon Mass Pair (Crystal Ball)')
    plt.legend()
    plt.show()
    plt.clf()
    

    plt.hist(xmass, color = 'k', bins = int(n_bins), histtype= 'step', range =(Min, Max), density=False )
    back_sub = decay(np.array(bins_back), param_back[0], param_back[1])
    plt.scatter(bins_back, back_sub, color = 'r')
    plt.plot(bins, decay(bins, param_back[0], param_back[1]), color = 'b')
    plt.title('Histogram of the Muon Pair Invariant mass with selected background regions highlighted and fitted')
    plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
    plt.ylabel('Count')
    plt.legend()
    plt.show()
    plt.clf()


    chi_sq_gauss = chi_sq(gauss_fit, count)
    chi_sq_d_gauss = chi_sq(double_gauss_fit, count)
    chi_sq_cb = chi_sq(crystal_ball_fit, count)

    res_squared_double_gauss = np.square(count - double_gauss_fit)

    plt.scatter(bins, np.log10(res_squared_double_gauss), marker = 'x', color = 'k')
    plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
    plt.ylabel('Squared Residual')
    plt.title('Squared Residuals versus Muon Pair Mass')
    plt.show()
    plt.clf()

    print(f"{chi_sq_gauss = :.5}\n{chi_sq_d_gauss = :.5}\n{chi_sq_cb = :.5}")


a = datetime.datetime.now()    
main()
b = datetime.datetime.now() - a
print(b)


