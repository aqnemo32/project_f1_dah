#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:00:55 2022

@author: achilequarante
"""

from ROOT import *

xmass = np.load('xmass.npy')

h1 = TH1F("h1", "MC Histogram")

h1.Fill(xmass)

h1.Draw()

input()