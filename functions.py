#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 22:50:27 2022

@author: achilequarante
"""
import numpy as np
from scipy.constants import pi
from scipy.special import erf

def gauss(x, a, sig, mu):
    '''
    

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    a : TYPE
        DESCRIPTION.
    sig : TYPE
        DESCRIPTION.
    mu : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return a*np.exp(-np.square(x-mu)/(2*np.square(sig)))

def crystalball(x, alpha, n, xbar, sigma):
    a = np.absolute(alpha)
    A = ((n/a)**n)*np.exp(-((a**2)/2))
    
    B = n/a - a
    C = n/a * 1/(n-1) * np.exp(-((a**2)/2))
    D = np.sqrt(pi/2)*(1+erf(a/np.sqrt(2)))
    N = 1/(sigma*(C + D))

    out  = []
    
    for i in x:
    
        if (i-xbar)/sigma > -alpha:
             out.append(N*np.exp(-np.square(i-xbar)/(2*np.square(sigma))))
        
        else:
            out.append(N*A*(B-((i-xbar)/sigma))**(-n))
            
    return np.array(out)

def decay(x, a, b):
    '''
    

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    a : TYPE
        DESCRIPTION.
    b : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return a*np.exp(x*b)

def double_gauss(x, a_1, mu_1, sig_1, a_2, mu_2, sig_2, mean_gauss_fit, sig_gauss_fit):
    '''
    

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    a_1 : TYPE
        DESCRIPTION.
    a_2 : TYPE
        DESCRIPTION.
    mu_1 : TYPE
        DESCRIPTION.
    mu_2 : TYPE
        DESCRIPTION.
    sig_1 : TYPE
        DESCRIPTION.
    sig_2 : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    tail = []
    center = []
    for i in x:
        if i< mean_gauss_fit-1*sig_gauss_fit or i > mean_gauss_fit-1*sig_gauss_fit:
            tail.append(i)
        else:
            center.append[i]

    return a_2*np.exp(-np.square(tail-mu_2)/(2*np.square(sig_2))) 
    return a_1*np.exp(-np.square(center-mu_1)/(2*np.square(sig_1)))

def chi_sq(fit,data):
    '''
    

    Parameters
    ----------
    fit : TYPE
        DESCRIPTION.
    data : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return np.sum((np.square(data-fit))/fit)

def peak_split(x, y, sig, mu):
    '''
    

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    y : TYPE
        DESCRIPTION
    sig : TYPE
        DESCRIPTION.
    mu : TYPE
        DESCRIPTION.

    Returns
    -------
    int
        DESCRIPTION.

    '''

    #defines the width of the 'center' region
    w = 2
    low_lim = mu - w*sig
    up_lim = mu + w*sig
    # almost working, get Honza to look at it
    tail_1st = x[x < low_lim]
    count_tail_1st = y[x < low_lim]
    
    tail_2nd = x[x >= up_lim]
    count_tail_2nd = y[x >= up_lim]

    center = x[(x >= low_lim) & (x < up_lim)]
    count_center = y[(x >= low_lim) & (x < up_lim)]
    # print(bins_1, count_1)
    
            
    return tail_1st, count_tail_1st, center, count_center, tail_2nd, count_tail_2nd
        