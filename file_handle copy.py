#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 14:17:35 2022

@author: s1973088
"""

import numpy as np

def main():
    filename = 'ups-15.bin'
    f = open(filename, 'r')
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
        
    np.save('xmass_big', xmass)
    np.save('mom_tran_pair_big', mom_tran_pair)
    np.save('rap_big', rap)
    np.save('mom_pair_big', mom_pair)
    np.save('mom_tran_1_big', mom_tran_1)
    np.save('mom_tran_2_big', mom_tran_2)
    f.close() 
    
main()
