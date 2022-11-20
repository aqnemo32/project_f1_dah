import matplotlib.pyplot as plt
import numpy as np
from functions import freedman


xmass = np.load('mc_anal/xmass_mc.npy')
mom_pair = np.load('mc_anal/mom_pair_mc.npy')
mom_tran_1 = np.load('mc_anal/mom_tran_1_mc.npy')
mom_tran_2 = np.load('mc_anal/mom_tran_2_mc.npy')
mom_tran_pair = np.load('mc_anal/mom_tran_pair_mc.npy')
rap = np.load('mc_anal/rap_mc.npy')

_, n_bins_xmass = np.modf((np.max(xmass)-np.min(xmass))/freedman(xmass))

plt.hist(xmass, color = 'k' ,bins = int(n_bins_xmass), histtype= 'bar', density = False)
plt.title('xmass')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mc_hist/mass_mc_hist', format = 'png')
plt.clf()

_, n_bins_mom_pair = np.modf((np.max(mom_pair)-np.min(mom_pair))/freedman(mom_pair))

plt.hist(mom_pair, color = 'k' ,bins = int(n_bins_mom_pair), range = [np.min(mom_pair), 1000], histtype= 'bar', density = False)
plt.title('Muon pair momentum (CoM momentum)')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mc_hist/mom_pair_mc_hist', format = 'png')
plt.clf()

_, n_bins_mom_tran_1 = np.modf((np.max(mom_tran_1)-np.min(mom_tran_1))/freedman(mom_tran_1))

plt.hist(mom_tran_1, color = 'k' ,bins = int(n_bins_mom_tran_1), range = [np.min(mom_tran_1), 100], histtype= 'bar', density = False)
plt.title('Transverse momentum 1')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mc_hist/mom_tran_1_mc_hist', format = 'png')
plt.clf()

_, n_bins_mom_tran_2 = np.modf((np.max(mom_tran_2)-np.min(mom_tran_2))/freedman(mom_tran_2))

plt.hist(mom_tran_2, color = 'k' ,bins = int(n_bins_mom_tran_2), range = [np.min(mom_tran_2), 100], histtype= 'bar', density = False)
plt.title('Transverse momentum 2')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mc_hist/mom_tran_2_mc_hist', format = 'png')
plt.clf()

_, n_bins_mom_tran_pair = np.modf((np.max(mom_tran_pair)-np.min(mom_tran_pair))/freedman(mom_tran_pair))

plt.hist(mom_tran_pair, color = 'k' ,bins = int(n_bins_mom_tran_pair), histtype= 'bar', density = False, range = (0, 50))
plt.title('Transverse momentum of muon pair (CoM transverse momentum)')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mc_hist/mom_tran_pair_mc_hist', format = 'png')
plt.clf()

_, n_bins_rap = np.modf((np.max(rap)-np.min(rap))/freedman(rap))

plt.hist(rap, color = 'k' ,bins = int(n_bins_rap), range = [np.min(rap), 10], histtype= 'bar', density = False)
plt.title('Rapidity')
plt.savefig('/Users/achillequarante/Desktop/dah_graphs_project/mc_hist/rap_mc_hist', format = 'png')
plt.clf()

bin_num = np.array([n_bins_xmass, n_bins_mom_pair, n_bins_mom_tran_1, n_bins_mom_tran_2, n_bins_mom_tran_pair, n_bins_rap])
print(f"{bin_num} = ")