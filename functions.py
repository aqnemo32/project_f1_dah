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
    '''
    '''
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

def double_crystalball(x, alpha1, alpha2, n1, n2, xbar, sigma):
    '''
    '''
    out = []
    a1 = np.absolute(alpha1)
    a2 = np.absolute(alpha2)

    A1 = ((n1/a1)**n1)*np.exp(-((a1**2)/2))
    B1 = n1/a1 - a1
    C1= n1/a1 * 1/(n1-1) * np.exp(-((a1**2)/2))
    D1 = np.sqrt(pi/2)*(1+erf(a1/np.sqrt(2)))
    N1 = 1/(sigma*(C1 + D1))

    A2 = ((n2/a2)**n2)*np.exp(-((a2**2)/2))
    B2 = n2/a2 - a2
    C2= n2/a2 * 1/(n2-1) * np.exp(-((a2**2)/2))
    D2 = np.sqrt(pi/2)*(1+erf(a2/np.sqrt(2)))
    N2 = 1/(sigma*(C2 + D2))
    
    N = (N1 + N2)/2

    for i in x:
        if (i-xbar)/sigma < -a1:
            out.append(A1*(B1-((i-xbar)/sigma))**(-n1))
        elif (i-xbar)/sigma < -a1 and (i-xbar)/sigma > a2:
            out.append(np.exp(-np.square(i-xbar)/(2*np.square(sigma))))
        else:
            out.append(A2*(B2-((i-xbar)/sigma))**(-n2))
            # (i-xbar)/sigma > a2

    
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
        