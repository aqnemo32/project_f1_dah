#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 17:29:59 2022

@author: mattkerr
"""

import numpy as np
from functions import *
import matplotlib.pyplot as plt

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

x = np.linspace(-5, 2, 1000)
col = ['k', 'r', 'y', 'm', 'c', 'b', 'g']
alpha = [0, 1, 1, 1, 2, 2, 2]
n = [1, 1, 2, 3, 4,5,6]
xbar = 0
sigma = 0.5
# for i in range(7):
#     plt.plot(x, crystalball(x, alpha[i], n[i], xbar, sigma), color = col[i], label = f"{alpha[i] = } {n[i] = }")
# plt.legend()
# plt.show()
# plt.clf()


plt.plot(bins_1, count_1, 'k')
plt.plot(bins_1, crystalball(bins_1, 2, 3, 9.45, 0.03))
plt.show()
plt.clf()


