import matplotlib.pyplot as plt
import numpy as np


xmass = np.load('xmass.npy')
mom_pair = np.load('mom_pair.npy')
mom_tran_1 = np.load('mom_tran_1.npy')
mom_tran_2 = np.load('mom_tran_2.npy')
mom_tran_pair = np.load('mom_tran_pair.npy')
rap = np.load('rap.npy')

plt.hist(xmass, color = 'k' ,bins = 600, histtype= 'bar', density = True)
plt.title('xmass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mass_hist', format = 'png')
plt.clf()

plt.hist(mom_pair, color = 'k' ,bins = 600, histtype= 'bar', density = True)
plt.title('Muon pair momentum (CoM momentum)')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mom_pai', format = 'png')
plt.clf()

plt.hist(mom_tran_1, color = 'k' ,bins = 600, histtype= 'bar', density = True)
plt.title('Transverse momentum 1')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mom_tran_hist', format = 'png')
plt.clf()

plt.hist(mom_tran_2, color = 'k' ,bins = 600, histtype= 'bar', density = True)
plt.title('Transverse momentum 2')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mom_tran_2_hist', format = 'png')
plt.clf()

plt.hist(mom_tran_pair, color = 'k' ,bins = 600, histtype= 'bar', density = True)
plt.title('Transverse momentum of muon pair (CoM transverse momentum)')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mom_tran_1_hist', format = 'png')
plt.clf()

plt.hist(rap, color = 'k' ,bins = 600, histtype= 'bar', density = True)
plt.title('Rapidity')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/rap_hist', format = 'png')
plt.clf()