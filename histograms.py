import numpy as np
import matplotlib.pyplot as plt

xmass = np.load('xmass.npy')
mom_pair = np.load('mom_pair.npy')
mom_tran_1 = np,load('mom_tran_1.npy')
mom_tran_2 = np.load('mom_tran_2.npy')
mom_tran_pair = np.load('mom_tran_pain.npy')
rap = np.load('rap.npy')

plt.hist(xmass, color = 'k' ,bins = 600, histtype= 'bar', density = True)
plt.title('xmass')
plt.clf()