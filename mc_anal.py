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
    xmass = np.load('xmass.npy')
    
    Min = np.min(xmass)
    Max = np.max(xmass)

    # b = datetime.datetime.now() - a
    # print(b)
    count , bins, patches = plt.hist(xmass, color = 'k', bins = 600, histtype= 'bar', range =(Min, Max), density=True )
    plt.show()
    plt.clf()
    bins = bins[1:]

    
    #histogram of the peaks from raw data
    bins_1 = bins[(bins > 9.2) & (bins < 9.7)]
    count_1 = count[(bins > 9.2) & (bins < 9.7)]


    # for the MC simulaton assuming ther is no background
    
    param_1, cov_1 = curve_fit(gauss, bins_1, count_1, p0 = [10, 0.05,9.45])
    mean_1 = param_1[2]
    std_1 = param_1[1]
    print(f"{mean_1=}\n{std_1=}")
    gauss_fit = gauss(bins_1, param_1[0], param_1[1], param_1[2]) 
    
    chi_sq_gauss = chi_sq(gauss_fit, count_1)

    tail_1st, count_tail_1st, center, count_center, tail_2nd, count_tail_2nd = peak_split(bins_1, count_1, std_1, mean_1)

    tail = np.concatenate((tail_1st, tail_2nd))
    count_tail = np.concatenate((count_tail_1st, count_tail_2nd))
    
    param_tail, cov_t = curve_fit(gauss, tail, count_tail, p0 = [5, 0.1, 9.45], maxfev = 1600)
    param_center, cov_c = curve_fit(gauss, center, count_center, p0= [10, 0.04, 9.45])
    
    
    tail_fit = gauss(tail, param_tail[0], param_tail[1], param_tail[2])
    center_fit = gauss(center, param_center[0], param_center[1], param_center[2])

    double_gauss_fit = np.concatenate((tail_fit[:len(tail_1st)], center_fit, tail_fit[len(tail_1st):]))
    chi_sq_d_gauss = chi_sq(double_gauss_fit, count_1)
    
    plt.scatter(bins_1, double_gauss_fit, marker = 'x')
    plt.plot(bins_1, count_1, '--', color = 'k')
    plt.show()
    plt.clf()
    print(f'{chi_sq_gauss=}\n{chi_sq_d_gauss=}')
    
    
    
    #CRYSTAL BALL FUNC
    print(f"{bins_1.shape = }{count_1.shape = }")
    crys_param, cryst_cov = curve_fit(crystalball, bins_1, count_1, p0 = [1.52, 2, 9.45, 0.03])
    print(f"{crys_param=}")
    # crys_param=array([1.52761093, 1.96427377, 9.46309005, 0.03492454])
    plt.scatter(bins_1, count_1, color = 'k', lw = 0.8, marker = 'x', label = 'data')
    plt.plot(bins_1, crystalball(bins_1, crys_param[0], crys_param[1], crys_param[2], crys_param[3]), 'r', label = 'fit')
    plt.title('Normalised count versus mass (Crystal Ball fit)')
    plt.xlabel('Mass')
    plt.ylabel('Count')
    plt.legend()
    plt.show()
    plt.clf()
    
    
    
    
    
    
    
    
    # p0 = [1, 2, mean_1, std_1]), 

    
    # crystal = Root.crystalball_function(bins_1,p0 = [1, 2, mean_1, std_1])
    # plt.plot(bins_1, crystal)
    # plt.show()
    # plt.clf()
    # need to find a way of combining the tail and center of the double gaussian fit


    # now that i made the double gaussian, need to find a way of combining the two gaussians into one, 
    # possible using 

        
    

    

    # count_1_d_fit = double_gauss(bins_1, param_1_d[0], param_1_d[1], param_1_d[2],
    #                 param_1_d[3], param_1_d[4], param_1_d[5], param_1[0], param_1[1]) 
    # count_2_fit = gauss(bins_2, param_2[0], param_2[1], param_2[2]) + decay(
    #     np.array(bins_2), param_back[0], param_back[1])
    # count_3_fit = gauss(bins_3, param_3[0], param_3[1], param_3[2]) + decay(
    #     np.array(bins_3), param_back[0], param_back[1])
    
    
    
    # plt.plot(bins[1:], count)
    # plt.plot(bins_1, count_1_fit, '--', lw=2)
    # plt.plot(bins_1, count_1_d_fit,'r', lw=1)
    # # plt.plot(bins_2, count_2_fit)
    # # plt.plot(bins_3, count_3_fit)
    # plt.xlabel('Bin Count')
    # plt.ylabel('Mass (units)')
    # plt.show()
    # plt.clf()
    
    # plt.plot(tail,count_tail, label = 'tail')
    # plt.plot(center, count_center, 'k', label = 'center')
    # plt.legend()
    # plt.show()
    # plt.clf
    
    #Residual
    
    # res_1 = count_1_fit - count_1
    # res_1_d = count_1_d_fit - count_1
    # res_1_d_sq = np.square(res_1_d)
    # res_1_sq = np.square(res_1)
    # res_2 = count_2_fit - count_2
    # res_3 = count_3_fit - count_3
    
    # r_sq_1 = 1 - (np.sum((count_1- count_1_fit)**2)/(np.sum((count_1-np.mean(count_1))**2)))
    # r_sq_1_d = 1 - (np.sum((count_1- count_1_d_fit)**2)/(np.sum((count_1-np.mean(count_1))**2)))
    
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
    # plt.plot(tail, tail_fit, 'k', label = 'gauss tail')
    # plt.plot(center, center_fit, 'r', label = 'gauss center')
    # plt.plot(tail,count_tail, label = 'tail')
    # plt.plot(center, count_center, 'y', label = 'center')
    # plt.legend()
    # plt.show()
    # plt.clf
    
    # plt.plot(bins_1, double_gauss_fit, 'r')
    # plt.plot(bins_1, count_1, 'k', '--')
    # plt.show()
    # plt.clf()

# a = datetime.datetime.now()    
main()
# b = datetime.datetime.now() - a
# print(b)