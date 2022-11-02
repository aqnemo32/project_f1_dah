#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 22:50:27 2022

@author: achilequarante
"""
import numpy as np

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

def double_gauss(x, a_1, mu_1, sig_1, a_2, mu_2, sig_2):
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
    return a_1*np.exp(-np.square(x-mu_1)/(2*np.square(sig_1)))+a_2*np.exp(-np.square(x-mu_2)/(2*np.square(sig_2)))