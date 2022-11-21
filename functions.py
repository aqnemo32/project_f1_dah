#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 22:50:27 2022

@author: achilequarante
"""
import numpy as np
from scipy.constants import pi
from scipy.special import erf
from scipy.stats import iqr

def freedman(x):
    return (2/(len(x)**(1/3)))*iqr(x)


def gauss(x, a, mu, sig):
    '''
    
    Parameters
    ----------
    x : numpy array
        histogram bins.
    a : float
        defines the amplitude of the gaussian fit.
    mu : float
        mean of the distribution, defines the x coordinate of the the gaussian fit maxima.
    sig : float
        standard deviation of the distribution, defines the width of the gaussian fit.


    Returns
    -------
    numpy array
        gaussian fit for the given bins, defines the y coordinate on a graph.

    '''
    return a*np.exp(-np.square(x-mu)/(2*np.square(sig)))

def crystalball(x, alpha, n, mu, sig):
    '''
    
    Parameters
    ----------
    x : numpy array
        DESCRIPTION.
    alpha : float
        DESCRIPTION.
    n : float
        DESCRIPTION.
    mu : float
        DESCRIPTION.
    sig : float
        DESCRIPTION.

    Returns
    -------
    numpy array
        DESCRIPTION.
    '''
    a = np.absolute(alpha)
    A = ((n/a)**n)*np.exp(-((a**2)/2))
    
    B = n/a - a
    C = n/a * 1/(n-1) * np.exp(-((a**2)/2))
    D = np.sqrt(pi/2)*(1+erf(a/np.sqrt(2)))
    N = 1/(sig*(C + D))

    out  = []
    
    for i in x:
    
        if (i-mu)/sig > -alpha:
             out.append(N*np.exp(-np.square(i-mu)/(2*np.square(sig))))
        
        else:
            out.append(N*A*(B-((i-mu)/sig))**(-n))
            
    return np.array(out)



def double_crystalball(x, alpha1, alpha2, n1, n2, mu, sig):
    '''
    
    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    alpha1 : TYPE
        DESCRIPTION.
    alpha1 : TYPE
        DESCRIPTION.
    n1 : TYPE
        DESCRIPTION.
    n2 : TYPE
        DESCRIPTION.
    mu : TYPE
        DESCRIPTION.
    sig : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.
    '''
    out = []
    a1 = np.absolute(alpha1)
    a2 = np.absolute(alpha2)

    A1 = ((n1/a1)**n1)*np.exp(-((a1**2)/2))
    B1 = n1/a1 - a1
    C1= n1/a1 * 1/(n1-1) * np.exp(-((a1**2)/2))
    D1 = np.sqrt(pi/2)*(1+erf(a1/np.sqrt(2)))
    N1 = 1/(sig*(C1 + D1))

    A2 = ((n2/a2)**n2)*np.exp(-((a2**2)/2))
    B2 = n2/a2 - a2
    C2= n2/a2 * 1/(n2-1) * np.exp(-((a2**2)/2))
    D2 = np.sqrt(pi/2)*(1+erf(a2/np.sqrt(2)))
    N2 = 1/(sig*(C2 + D2))
    
    N = (N1 + N2)/2

    for i in x:
        if (i-mu)/sig < -a1:
            out.append(N*A1*(B1-((i-mu)/sig))**(-n1))
        elif (i-mu)/sig > -a1 and (i-mu)/sig < a2:
            out.append(N*np.exp(-np.square(i-mu)/(2*np.square(sig))))
        elif (i-mu)/sig > a2:
            out.append(N*A2*(B2-((i-mu)/sig))**(-n2))
            # (i-mu)/sig > a2

    
    return np.array(out)



def decay(x, a, b):
    '''

    Parameters
    ----------
    x : array
        bins of a histogram.
    a : float
        defines the amplitude of the deacy.
    b : float
        defines the speed of the decay (bigger b steeper curve).

    Returns
    -------
    array
        exponential decay background noise

    '''
    return a*np.exp(x*b)


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
    x : array
        bins.
    y : array
        counts
    sig : float
        standard deviation from a single gaussian fit of the data.
    mu : float
        mean from a single gaussian fit of the data.

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
        