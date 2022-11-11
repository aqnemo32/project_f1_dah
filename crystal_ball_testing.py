#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 17:29:59 2022

@author: mattkerr
"""

import numpy as np
from functions import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xmass = np.load('xmass.npy')

Min = np.min(xmass)
Max = np.max(xmass)

# b = datetime.datetime.now() - a
# print(b)
count , bins, patches = plt.hist(xmass, color = 'k', bins = 600, histtype= 'bar', range =(Min, Max), density=True )
plt.show()
plt.clf()
bins_x = bins[1:]


# histogram of the peaks from raw data
bins_1 = bins_x[(bins_x > 9.2) & (bins_x < 9.7)]
count_1 = count[(bins_x > 9.2) & (bins_x < 9.7)]

x = np.linspace(-1, 1, 1000)
col = [ 'r', 'y', 'm', 'c', 'b', 'g']
alpha = [0, 1, 1, 1, 2, 2, 2]
n = [1, 1, 2, 3, 4,5,6]
xbar = 0
sigma = 0.5
# for i in range(7):
#     plt.plot(x, crystalball(x, alpha[i], n[i], xbar, sigma), color = col[i], label = f"{alpha[i] = } {n[i] = }")
# plt.legend()
# plt.show()
# plt.clf()


# plt.plot(bins_1, count_1, 'k')
# plt.plot(bins_1, crystalball(bins_1, 2, 3, 9.45, 0.03))
# plt.show()
# plt.clf()

a1 = 1
a2 = 3
n1 = [1,1,2,2]
n2 = [1,2,2,3]
x = double_crystalball(bins_1, 1, 2, 2, 2, 9.45, 0.03)
print(x.shape)
# cbd_p , cbd_c = curve_fit(double_crystalball, bins_1, count_1, p0 = [1, 2, 2, 2, 9.45, 0.03] )
# dp, double_cov = curve_fit(double_crystalball, bins_1, count_1, p0 = [ 1, 1, 2, 2, 9.45, 0.03])
# plt.scatter(bins_1, count_1, label = 'data', marker = 'x', color = 'k')
for i in range(4):
    plt.plot(bins_1, double_crystalball(bins_1, a1, a2, n1[i], n2[i], 9.475, 0.03), col[i], label = f"{n1[i]}, {n2[i]}")
# plt.plot(bins_1, double_crystalball(bins_1, cbd_p[0], cbd_p[1], cbd_p[2], cbd_p[3], cbd_p[4], cbd_p[5]), 'r', label = 'fit')
plt.legend()
plt.show()


