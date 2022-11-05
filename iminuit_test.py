#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:25:39 2022

@author: achilequarante
"""

from iminuit import Minuit
import probfit
import numpy as np
import matplotlib.pyplot as plt


xmass = np.load('xmass.npy')
# count , bins, patches = plt.hist(xmass, color = 'k', bins = 600, histtype= 'bar', range =(Min, Max), density=True )
# plt.clf()

probfit.pdf.crystallball(xmass,1.0, 2.0, np.mean(xmass), np.std(xmass))
plt.show()