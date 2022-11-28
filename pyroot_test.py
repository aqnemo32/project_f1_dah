import ROOT
import numpy as np
from functions import freedman
import matplotlib.pyplot as plt

# Analysis of the MC data

xmass_mc = np.load('mc_anal/xmass_mc.npy')
count, bins, patches = plt.hist(xmass_mc, bins = 400)
plt.clf()
bins = bins[1:] - (bins[1] - bins[0])/2

n_bins = (np.max(xmass_mc) - np.min(xmass_mc))/freedman(xmass_mc)

hist_mc = ROOT.TH1F('xmass_mc ','Number of Events versus Muon Pair Invariant Mass ' ,500 ,bins[0], bins[-1])
hist_mc.Sumw2


for i in xmass_mc:
    hist_mc.Fill(i)

hist_mc.SetDirectory(0)

canvas = ROOT.TCanvas (' canvas ')
canvas.cd()


hist_mc.SetStats(0)
hist_mc.SetLineColor( ROOT.kBlue )
hist_mc.SetLineWidth(2)
hist_mc.GetYaxis().SetTitle(" Number of events ")
hist_mc.GetXaxis().SetTitle("Muon Pair Mass [GeV/c^{2}]")
hist_mc.Draw("pe")


gauss_fit_mc = ROOT.TF1(" gaussfit ", "gaus" ,9.0 ,10.0 )

hist_mc.Fit(gauss_fit_mc, 'E')

canvas.Print ( 'xmass_mc_hist.png')


chi2_gauss = gauss_fit_mc.GetChisquare()
ndof_gauss = gauss_fit_mc.GetNDF()

mean = gauss_fit_mc.GetParameter(1)
sig = gauss_fit_mc.GetParameter(0)

hist_mc_prime = hist_mc

# Setting up Crystal Ball PDF to fit to hist_mc

f_cb = ROOT.TF1("My Crystall Ball", "crystalball", 9.0, 10.0)

f_cb.SetParameters(1, mean, sig, 2, 1)


hist_mc_prime.SetStats(0)
hist_mc_prime.SetLineColor( ROOT.kBlue )
hist_mc_prime.SetLineWidth(2)
hist_mc_prime.GetYaxis().SetTitle(" Number of events ")
hist_mc_prime.GetXaxis().SetTitle("Muon Pair Mass [GeV/c^{2}]")
hist_mc_prime.Draw("pe")

hist_mc_prime.Fit(f_cb, 'E') #worked up till here

x= []
for i  in range(5):
    x.append(f_cb.GetParameter(i))

print(x)

alpha_cb = x[3]
n_cb = x[4]

canvas.Print ('xmass_mc_hist_cb.png')

chi2_cb = f_cb.GetChisquare()
ndof_cb = f_cb.GetNDF()

print(f"{chi2_gauss/ndof_gauss = }\n{chi2_cb/ndof_cb = }")

# Analysis of the Upsilon data

xmass_dirty = np.load('ups_big_anal/xmass_big.npy')
tran_1_ups = np.load('ups_big_anal/mom_tran_1_big.npy')
tran_2_ups = np.load('ups_big_anal/mom_tran_2_big.npy')


#Cleaning the data using the trnasverse momenta of both particles
R = np.absolute(tran_2_ups - tran_1_ups)/(tran_2_ups + tran_1_ups)

xmass = xmass_dirty[R<0.42]

n_bins = (np.max(xmass) - np.min(xmass))/freedman(xmass)

hist_ups = ROOT.TH1F('xmass ','Number of Events versus Muon Pair Invariant Mass ' ,int(n_bins) ,bins[0], bins[-1])
hist_ups.Sumw2

for i in xmass:
    hist_ups.Fill(i)

hist_ups.SetDirectory(0)

hist_ups.SetStats(0)
hist_ups.SetLineColor( ROOT.kBlue )
hist_ups.SetLineWidth(2)
hist_ups.GetYaxis().SetTitle(" Number of events ")
hist_ups.GetXaxis().SetTitle("Muon Pair Mass [GeV/c^{2}]")
hist_ups.Draw("pe")

canvas.Print ('xmass_hist.png')

# Create gaussian pdf to fit to the Upsilon data

g_1 = "gaus(0)" #0,1,2
g_2 = "gaus(3)" #3,4,5
g_3 = "gaus(6)" #6,7,8

decay = "[11]*expo(9)" #9,10,11
pdf_gauss = "((%s) + (%s) + (%s) + (%s))"%(g_1, g_2, g_3, decay)

gauss_fit = ROOT.TF1("Gaussian PDF Fit", pdf_gauss, bins[0], bins[-1])

#9.4559481, 0.041711, 10.01799, 0.03113, 10.3005, -0.4595, 5000, 3000, 1000, 500, 
init_guess = [3613.8583285092777, 9.455918567546822, 0.042843849704360074,
                791.5639053985701, 10.019420108604223, 0.04556928202676283,
                378.86449867221665, 10.349280269096958, 0.04794189766771405,
                6.068596203963025, -0.6108361524095771, 1063.7813169063427]
b = init_guess
gauss_fit.SetParameter(0, b[0])
gauss_fit.SetParameter(1, b[1])
gauss_fit.SetParameter(2, b[2])
gauss_fit.SetParameter(3, b[3])
gauss_fit.SetParameter(4, b[4])
gauss_fit.SetParameter(5, b[5])
gauss_fit.SetParameter(6, b[6])
gauss_fit.SetParameter(7, b[7])
gauss_fit.SetParameter(8, b[8])
gauss_fit.SetParameter(9, b[9])
gauss_fit.SetParameter(10, b[10])
gauss_fit.SetParameter(11, b[11])



gauss_fit.SetLineColor(ROOT.kBlack)
gauss_fit.SetLineWidth(2)
gauss_fit.Draw()

canvas.Print('test_gauss_pdf.png')

hist_ups.SetDirectory(0)

hist_ups.SetStats(0)
hist_ups.SetLineColor( ROOT.kBlue )
hist_ups.SetLineWidth(2)
hist_ups.GetYaxis().SetTitle(" Number of events ")
hist_ups.GetXaxis().SetTitle("m(#mu^{+} #mu^{-}) [GeV/c^{2}]")
hist_ups.Draw("pe")

hist_ups.Fit(gauss_fit, 'L')

legend = ROOT.TLegend(0.7, 0.6, 0.85, 0.75)
legend.AddEntry(hist_ups, "Data")
legend.AddEntry(gauss_fit, "Gaussian Fit")
legend.SetLineWidth(0)
legend.Draw("same")


canvas.Print ('xmass_hist_gauss.png')


# Create a double gaussian pdf to fit the Upsilon data

# For Double Gauss parameters in order are:
#       A, mu, sigma * 2 + b (Normalisaton between both gaussians)

d_g_1 = "[0]*([4]*exp(-0.5*((x-[1])/[2])^2) + (1-[4])*exp(-0.5*((x-[1])/[3])^2))" # 0 - 1,2 - 1,3 - 4
d_g_2 = "[5]*([9]*exp(-0.5*((x-[6])/[7])^2) + (1-[9])*exp(-0.5*((x-[7])/[8])^2))" # 5 - 6,7 - 7,8 - 9
d_g_3 = "[10]*([14]*exp(-0.5*((x-[11])/[12])^2) + (1-[14])*exp(-0.5*((x-[11])/[13])^2))" # 10 - 11,12 - 12,13 - 14
decay_dg = "[17]*expo(15)" # 15,16 - 27

pdf_d_gauss = "((%s) + (%s) + (%s) + (%s))"%(d_g_1, d_g_2, d_g_3, decay_dg)

d_gauss_fit = ROOT.TF1("Double Gaussian Fit", pdf_d_gauss, bins[0], bins[-1])


# Peak 1
d_gauss_fit.SetParameter(0, 4.09667e+04)
d_gauss_fit.SetParName(0, "1 A 1")
d_gauss_fit.SetParameter(1, 9.45579)
d_gauss_fit.SetParName(1, "1 mu")
d_gauss_fit.SetParameter(2, 4.07224e-02)
d_gauss_fit.SetParName(2, "1 sig 1")
d_gauss_fit.SetParameter(3, 1.04659e-01)
d_gauss_fit.SetParName(3, "1 sig 2")
d_gauss_fit.SetParameter(4, 9.50803e-01)
d_gauss_fit.SetParLimits(4, 0, 1)
d_gauss_fit.SetParName(4, "1 b")

# Peak 2
d_gauss_fit.SetParameter(5, 1.20934e+04)
d_gauss_fit.SetParName(5, "2 A 1")
d_gauss_fit.SetParameter(6, 1.00188e+01)
d_gauss_fit.SetParName(6, "2 mu")
d_gauss_fit.SetParameter(7, 4.60835e-02)
d_gauss_fit.SetParName(7, "2 sig 1")
d_gauss_fit.SetParameter(8, 1.10135e+01)
d_gauss_fit.SetParName(8, "2 sig 2")
d_gauss_fit.SetParameter(9, 7.47857e-01)
d_gauss_fit.SetParLimits(9, 0, 1)
d_gauss_fit.SetParName(9, "2 b")

# Peak 3
d_gauss_fit.SetParameter(10, 4.32570e+03)
d_gauss_fit.SetParName(10, "3 A 1")
d_gauss_fit.SetParameter(11, 1.03499e+01)
d_gauss_fit.SetParName(11, "3 mu 1")
d_gauss_fit.SetParameter(12, 4.79953e-02)
d_gauss_fit.SetParName(12, "3 sig 1")
d_gauss_fit.SetParameter(13, 4.29587e+01)
d_gauss_fit.SetParName(13, "3 sig 2")
d_gauss_fit.SetParameter(14, 0.5)
d_gauss_fit.SetParLimits(14, 0, 1)
d_gauss_fit.SetParName(14, "3 b")



# Decay
d_gauss_fit.SetParameter(15, 8.55484)
d_gauss_fit.SetParameter(16, -0.654703)
d_gauss_fit.SetParameter(17, 1.39381e+03)


d_gauss_fit.SetLineColor(ROOT.kBlack)
d_gauss_fit.SetLineWidth(2)
d_gauss_fit.Draw()

canvas.Print('test_d_gauss_pdf.png')

hist_ups.SetDirectory(0)

hist_ups.SetStats(0)
hist_ups.SetLineColor( ROOT.kBlue )
hist_ups.SetLineWidth(2)
hist_ups.GetYaxis().SetTitle(" Number of events ")
hist_ups.GetXaxis().SetTitle("Muon Pair Mass [GeV/c^{2}]")
hist_ups.Draw("pe")

hist_ups.Fit(d_gauss_fit, 'L')

legend = ROOT.TLegend(0.7, 0.6, 0.85, 0.75)
legend.AddEntry(hist_ups, "Data")
legend.AddEntry(d_gauss_fit, "Double Gaussian Fit")
legend.SetLineWidth(0)
legend.Draw("same")

canvas.Print ('xmass_hist_d_gauss.png')

# Create a Crystal Ball pdf to fit the Upsilon data

cb_1 = "crystalball(0)" #0,1,2,3,4
cb_2 = "crystalball(5)" #5,6,7,8,9
cb_3 = "crystalball(10)" #10,11,12,13,14
decay_cb = "[17]*expo(15)" #15,16,17

pdf_cb = "((%s) + (%s) + (%s) + (%s))"%(cb_1, cb_2, cb_3, decay_cb)

cb_fit = ROOT.TF1("Crystal Ball PDF", pdf_cb, bins[0], bins[-1])

# Parameter Naming Converntion:
#     A = Normalisation or Amplitude
#     mu = mean
#     sig = standard deviation
#     alpha = Alpha of Crystal Ball
#     n = n of Crystal Ball

#Crystal Ball 1
cb_fit.SetParameter(0,3600)
cb_fit.SetParName(0,"A 1")
cb_fit.SetParameter(1,9.45)
cb_fit.SetParName(1,"mu 1")
cb_fit.SetParameter(2,0.03)
cb_fit.SetParName(2,"sig 1")

cb_fit.SetParameter(3,alpha_cb) #alpha_cb
cb_fit.SetParName(3,"alpha 1")
cb_fit.FixParameter(3, alpha_cb)
cb_fit.SetParameter(4,n_cb) # 
cb_fit.SetParName(4,"n 1")
cb_fit.FixParameter(4, n_cb)

#Crystal Ball 2
cb_fit.SetParameter(5,700)
cb_fit.SetParName(5,"A 2")
cb_fit.SetParameter(6,10.0)
cb_fit.SetParName(6,"mu 2")
cb_fit.SetParameter(7,0.03)
cb_fit.SetParName(7,"sig 2")

cb_fit.SetParameter(8,alpha_cb)
cb_fit.SetParName(8,"alpha 2")
cb_fit.FixParameter(8, alpha_cb)
cb_fit.SetParameter(9,n_cb)
cb_fit.SetParName(9,"n 2")
cb_fit.FixParameter(9, n_cb)

#Crystal Ball 3
cb_fit.SetParameter(10,300)
cb_fit.SetParName(10,"A 3")
cb_fit.SetParameter(11,10.35)
cb_fit.SetParName(11,"mu 3")
cb_fit.SetParameter(12,0.01)
cb_fit.SetParName(12,"sig 3")

cb_fit.SetParameter(13,alpha_cb)
cb_fit.SetParName(13,"alpha 3")
cb_fit.FixParameter(13, alpha_cb)
cb_fit.SetParameter(14,n_cb)
cb_fit.SetParName(14,"n 3")
cb_fit.FixParameter(14, n_cb)

#Decay
cb_fit.SetParameter(15,5.93248e+00)
cb_fit.SetParameter(16,-0.586445)
cb_fit.SetParameter(17,938)

cb_fit.SetLineColor(ROOT.kBlack)
cb_fit.SetLineWidth(2)
cb_fit.Draw()

canvas.Print('test_cb_pdf.png')


hist_ups.SetDirectory(0)

hist_ups.SetStats(0)
hist_ups.SetLineColor( ROOT.kBlue )
hist_ups.SetLineWidth(2)
hist_ups.GetYaxis().SetTitle(" Number of events ")
hist_ups.GetXaxis().SetTitle("Muon Pair Mass [GeV/c^{2}]")
hist_ups.Draw("pe")

hist_ups.Fit(cb_fit, 'L')

legend = ROOT.TLegend(0.7, 0.6, 0.85, 0.75)
legend.AddEntry(hist_ups, "Data")
legend.AddEntry(cb_fit, "Crystal Ball Fit")
legend.SetLineWidth(0)
legend.Draw("same")

canvas.Print ('xmass_hist_cb.png')

chi2_gauss = gauss_fit.GetChisquare()
gauss_ndof = gauss_fit.GetNDF()


chi2_d_gauss = d_gauss_fit.GetChisquare()
d_gauss_ndof = d_gauss_fit.GetNDF()

chi2_cb = cb_fit.GetChisquare()
cb_ndof = cb_fit.GetNDF()

print(d_gauss_ndof, cb_ndof)
print(f"{chi2_gauss/gauss_ndof = }\n{chi2_d_gauss/d_gauss_ndof = }\n{chi2_cb/cb_ndof = }")

# Finding the areas under the first peaks for the double gaussian and crystal ball for the error estimation




test_d_gauss = ROOT.TF1("test func", d_g_1, 7.5, 10.0)

test_d_gauss.SetParameters(41903.095173652015, 9.455921313503952, 0.03598768850967427, 0.06785006410165306, 0.7728296909250849)

print(f"{test_d_gauss.Integral(9.0, 9.65) = }")



test_cb = ROOT.TF1("test func", cb_1, 7.5, 10.0)
test_cb.SetParameters(40981.299213096754,9.456199461119844,0.04286138281195304,1.809797775245278,1.2147346008187958)

print(f"{test_cb.Integral(9.0, 9.65) = }")

bool_back_1 = (xmass <= 9.2) | (xmass >= 10.55)
bool_back_2 = (xmass >= 9.7) & (xmass <= 9.85)

xmass_back = np.concatenate((xmass[bool_back_1], xmass[bool_back_2]))

hist_back = ROOT.TH1F('xmass_back','Number of Events versus Muon Pair Invariant Mass Background' ,int(n_bins) ,bins[0], bins[-1])
hist_back.Sumw2

for i in xmass_back:
    hist_back.Fill(i)


exp_fit = "expo(0)*[2]"
lin_fit = "[0] * x + [1]"

exp_func = ROOT.TF1("exp func", exp_fit, bins[0], bins[-1])
exp_func.SetParameters(3.0, -0.5, 20000)

lin_func = ROOT.TF1("lin func", lin_fit, bins[0], bins[-1])

hist_back.Fit(exp_func, "L")
hist_back.Fit(lin_func, "L")

print(f"{exp_func.Integral(bins[0], bins[-1]) = }")
print(f"{lin_func.Integral(bins[0], bins[-1]) = }")

print(f"diference {1 - lin_func.Integral(bins[0], bins[-1])/exp_func.Integral(bins[0], bins[-1]})")

