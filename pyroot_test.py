import ROOT
import numpy as np
import matplotlib.pyplot as plt

xmass_mc = np.load('mc_anal/xmass_mc.npy')
count, bins, patches = plt.hist(xmass_mc, bins = 400)
plt.clf()
bins = bins[1:] - (bins[1] - bins[0])/2

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
hist_mc.GetXaxis().SetTitle("m_{ll} [GeV/c^{2}]")
hist_mc.Draw("pe")


gauss_fit = ROOT.TF1(" gaussfit ", "gaus" ,9.0 ,10.0 )

hist_mc.Fit(gauss_fit, 'E')

canvas.Print ( 'xmass_mc_hist.pdf')


chi2_gauss = gauss_fit.GetChisquare()
ndof_gauss = gauss_fit.GetNDF()

mean = gauss_fit.GetParameter(1)
sig = gauss_fit.GetParameter(0)

hist_mc_prime = hist_mc

# Setting up Crystal Ball PDF to fit to hist_mc

f_cb = ROOT.TF1("My Crystall Ball", "crystalball", 9.0, 10.0)

f_cb.SetParameters(1, mean, sig, 2, 1)


hist_mc_prime.SetStats(0)
hist_mc_prime.SetLineColor( ROOT.kBlue )
hist_mc_prime.SetLineWidth(2)
hist_mc_prime.GetYaxis().SetTitle(" Number of events ")
hist_mc_prime.GetXaxis().SetTitle("m_{ll} [GeV/c^{2}]")
hist_mc_prime.Draw("pe")

hist_mc_prime.Fit(f_cb, 'E') #worked up till here




canvas.Print ('xmass_mc_hist_cb.pdf')

chi2_cb = f_cb.GetChisquare()
ndof_cb = f_cb.GetNDF()

print(f"{chi2_gauss/ndof_gauss = }\n{chi2_cb/ndof_cb = }")

