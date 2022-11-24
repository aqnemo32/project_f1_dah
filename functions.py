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


def double_gauss(x, a, mu, sig_1, sig_2, f):
    '''
    
    Parameters
    ----------
    x : numpy array
        histogram bins.
    a : float
        defines the amplitude of the gaussian fit.
    mu : float
        mean of the distribution, defines the x coordinate of the the gaussian fit maxima.
    sig_1 : float
        standard deviation of the distribution, defines the width of the first gaussian fit.
    sig_2 : float
        standard deviation of the distribution, defines the width of the second gaussian fit.
    f : float
        XXXX.


    Returns
    -------
    numpy array
        double gaussian fit for the given bins, defines the y coordinate on the histogram.

    '''
    return a*(f*np.exp(-np.square(x-mu)/(2*np.square(sig_1))) + (f-1)*np.exp(-np.square(x-mu)/(2*np.square(sig_2))))



def gauss_decay(x, a, mu, sig, A, b):
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
    A : float
        amplitude of the exponential decay.
    b : float
        defines the speed of the decay (bigger b steeper curve)


    Returns
    -------
    numpy array
        gaussian fit for the given bins, defines the y coordinate on a graph.

    '''
    return a*np.exp(-np.square(x-mu)/(2*np.square(sig))) + A*np.exp(x*b)

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

def peak_split(x, y, mu, sig):
    '''

    Parameters
    ----------
    x : array
        bins.
    y : array
        counts
    mu : float
        mean from a single gaussian fit of the data.
    sig : float
        standard deviation from a single gaussian fit of the data.

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
    
    tail_2nd = x[x > up_lim]
    count_tail_2nd = y[x > up_lim]

    center = x[(x >= low_lim) & (x <= up_lim)]
    count_center = y[(x >= low_lim) & (x <= up_lim)]
    # print(bins_1, count_1)
            
    return tail_1st, count_tail_1st, center, count_center, tail_2nd, count_tail_2nd
        