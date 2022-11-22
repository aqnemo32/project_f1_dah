
import numpy as np
import matplotlib.pyplot as plt


from functions import *


xmass = np.load('ups_anal/xmass.npy')
mom_tran_pair = np.load('ups_anal/mom_tran_pair.npy')
rap = np.load('ups_anal/rap.npy')
mom_tran_1 = np.load('ups_anal/mom_tran_1.npy')
mom_tran_2 = np.load('ups_anal/mom_tran_2.npy')
mom_pair = np.load('ups_anal/mom_pair.npy')


#2d Histogram of log10 transverse momenttum versus xmass
mom_tran_pair_log = np.log10(mom_tran_pair)

plt.hist(mom_tran_pair_log, color = 'k', bins= 200, histtype = 'bar')
plt.ylabel('Count')
plt.xlabel('Logarithm base 10 of the Pair Transverse Momentum')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_pair_log', format = 'png')
plt.clf()

plt.hist2d(xmass, mom_tran_pair_log, bins = 200, range = [[9.2, 10.5], [-0.25, 1.3]])
plt.ylabel(' log base 10 Pair Transverse Momentum')
plt.xlabel('Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_pair_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, rap, bins = 200, range = [[9.2, 10.5], [2, 6]])
plt.ylabel('Rapidity')
plt.xlabel('Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/rap_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, mom_tran_1, bins = 200, range = [[9.2, 10.5], [0, 20]])
plt.ylabel('First Muon Transverse Momentum')
plt.xlabel('Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_1_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, np.log10(mom_tran_1), bins = 200, range = [[9.2, 10.5], [0, 1.2]])
plt.ylabel('Logarithm base 10 of the First Muon Transverse Momentum')
plt.xlabel('Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/log_mom_tran_1_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, mom_tran_2, bins = 200, range = [[9.2, 10.5], [0, 20]])
plt.ylabel('Second Muon Transverse Momentum')
plt.xlabel('Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_2_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, np.log10(mom_tran_2), bins = 200, range = [[9.2, 10.5], [0, 1.2]])
plt.ylabel('Logarithm base 10 of the Second Muon Transverse Momentum')
plt.xlabel('Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/log_mom_tran_2_xmass_2d_hist', format = 'png')
plt.clf()


log_mom_pair = np.log10(mom_pair)

plt.hist2d(xmass, mom_pair, bins = 200, range = [[9.2, 10.5], [0, 200]])
plt.ylabel('Muon Pair Momentum')
plt.xlabel('Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_pair_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, log_mom_pair, bins = 200, range = [[9.2, 10.5], [1.4, 2.8]])
plt.ylabel('Logarithm Base 10 Muon Pair Momentum')
plt.xlabel('Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/log_mom_pair_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(mom_tran_1, mom_tran_2, bins = 200, range = [[0,30],[0,30]])
plt.ylabel('Second Muon Transverse Momentum')
plt.xlabel('First Muon Transverse Momentum')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_1_2_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, np.absolute(mom_tran_2 - mom_tran_1)/(mom_tran_2 + mom_tran_1), bins = 200, range = [[9.2,10.5],[0,1]])
plt.ylabel(r'$ \frac{|p_{t_2} - p_{t_1}|}{p_{t_2} + p_{t_1}} $')
plt.xlabel('Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/xmass_sub_mom_tran_1_2_2d_hist', format = 'png')
plt.clf()