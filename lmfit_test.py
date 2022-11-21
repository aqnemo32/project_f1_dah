from lmfit import Model
from functions import *
import matplotlib.pyplot as plt

xmass = np.load('mc_anal/xmass_mc.npy')
count, bins, patche = plt.hist(xmass, bins = 200)
plt.clf()

bins = bins[1:] - (bins[1]-bins[0])/2
    
#histogram of the peaks from raw data
bins_1 = bins[(bins > 9.2) & (bins < 9.7)]
count_1 = count[(bins > 9.2) & (bins < 9.7)]

gmodel = Model(gauss)
print(f"parameter names = {gmodel.param_names}")
params = gmodel.make_params(a = 40000, mu = 9.45, sig = 0.03)
result = gmodel.fit(count_1, params, x = bins_1, method = 'leastsq')
result_bis = gmodel.fit(count_1, params, x = bins_1, method = 'nelder')
print(result.fit_report())
print(result_bis.fit_report())
# crystal ball not fitting properly, blowing up alpha and n, especially the errors
model = Model(crystalball)
print(f"parameter names = {model.param_names}")
params_cb = model.make_params( alpha = 1, n= 1.5, mu = 9.46, sig = 0.035)
result_cb = model.fit(count_1, params_cb, x = bins_1)
print(result_cb.fit_report())


