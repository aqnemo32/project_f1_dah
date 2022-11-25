
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
plt.xlabel(r'log$_{10}$ p$_{t_{pair}}$')
plt.title(r'Histogram of log$_{10}$ p$_{t_{pair}}')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_pair_log', format = 'png')
plt.clf()

plt.hist2d(xmass, mom_tran_pair_log, bins = 200, range = [[9.2, 10.5], [-0.25, 1.3]])
plt.ylabel(r'log$_{10}$ p$_{t_{pair}}$')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title(r'2D Histogram of log$_{10}$ p$_{t_{pair}}$ versus Muon Mass Pair')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_pair_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, rap, bins = 200, range = [[9.2, 10.5], [2, 6]])
plt.ylabel('Rapidity')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title('2D Histogram Rapidity versus Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/rap_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, mom_tran_1, bins = 200, range = [[9.2, 10.5], [0, 20]])
plt.ylabel(r'p$_{t_{1}}$ [GeV/c]')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title(r'2D Histogram of p$_{t_{1}}$ verus Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_1_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, np.log10(mom_tran_1), bins = 200, range = [[9.2, 10.5], [0, 1.2]])
plt.ylabel(r'log$_{10}$ p$_{t_{1}}$')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title(r'2D Histogram of log$_{10}$ p$_{t_{1}}$ versus Muon Mass Pair')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/log_mom_tran_1_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, mom_tran_2, bins = 200, range = [[9.2, 10.5], [0, 20]])
plt.ylabel(r'p$_{t_{2}}$ [GeV/c]')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title(r'2D Histogram of p$_{t_{2}}$ verus Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_2_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, np.log10(mom_tran_2), bins = 200, range = [[9.2, 10.5], [0, 1.2]])
plt.ylabel(r'log$_{10}$ p$_{t_{2}}$')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title(r'2D Histogram of the log$_{10}$ p$_{t_{2}}$ verus Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/log_mom_tran_2_xmass_2d_hist', format = 'png')
plt.clf()


log_mom_pair = np.log10(mom_pair)

plt.hist2d(xmass, mom_pair, bins = 200, range = [[9.2, 10.5], [0, 200]])
plt.ylabel('Muon Pair Momentum [GeV/c]')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title('2D Histogram Muon Pair Momentum versus Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_pair_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(xmass, log_mom_pair, bins = 200, range = [[9.2, 10.5], [1.4, 2.8]])
plt.ylabel(r'log$_{10}$ p$_{pair}$')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title(r'2D Histogram of log$_{10}$ p$_{pair}$ versus Muon Pair Mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/log_mom_pair_xmass_2d_hist', format = 'png')
plt.clf()

plt.hist2d(mom_tran_1, mom_tran_2, bins = 200, range = [[0,15],[0,15]])
plt.ylabel(r'p$_{t_{2}} [GeV/c]$')
plt.xlabel(r'p$_{t_{1}} [GeV/c]$')
plt.title(r'2D Histogram p$_{t_{2}}$ versus p$_{t_{1}}$')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/mom_tran_1_2_2d_hist', format = 'png')
plt.clf()

R = np.absolute(mom_tran_2 - mom_tran_1)/(mom_tran_2 + mom_tran_1)

plt.hist2d(xmass, R, bins = 200, range = [[9.2,10.5],[0,1]])
plt.ylabel(r'$ R = \frac{ | p_{t_2} - p_{t_1} |}{p_{t_2} + p_{t_1}} $')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title('2D Histogram of R versus Muon pair mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/xmass_sub_mom_tran_1_2_2d_hist', format = 'png')
plt.clf()

xmass_new = xmass[R<0.42]
R_new = R[R<0.42]


plt.hist2d(xmass_new, R_new, bins = 200, range = [[9.2,10.5],[0,0.42]])
plt.ylabel(r'$ R = \frac{ | p_{t_2} - p_{t_1} |}{p_{t_2} + p_{t_1}} $')
plt.xlabel(r'Muon Pair Mass [GeV/c$^2$]')
plt.title('Cleaned 2D Histogram of R versus Muon pair mass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/2d_hist/xmass_sub_mom_tran_1_2__clean_2d_hist', format = 'png')
plt.clf()