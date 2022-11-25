import ROOT
import numpy as np
import matplotlib.pyplot as plt

xmass_mc = np.load('mc_anal/xmass_mc.npy')
count, bins, patches = plt.hist(xmass_mc, bins = 400)
plt.clf()
bins = bins[1:] - (bins[1] - bins[0])/2

hist_mc = ROOT.TH1F('xmass_mc ','m_{ll} , data ' ,500 ,bins[0], bins[-1])
hist_mc.Sumw2


for i in xmass_mc:
    hist_mc.Fill(i)

hist_mc.SetDirectory(0)

canvas = ROOT.TCanvas (' canvas ')
canvas.cd()
canvas.SetLogy( False )

# canvas.Print ( 'xmass_mc_hist.pdf' + '[')

hist_mc.SetStats(1)
hist_mc.SetLineColor( ROOT.kBlack )
hist_mc.SetLineWidth(2)
hist_mc.GetYaxis().SetTitle(" Number of events ")
hist_mc.GetXaxis().SetTitle("m_{ll} [MeV]")
hist_mc.Draw("pe")


gauss_fit = ROOT.TF1(" gaussfit ", "gaus" ,9.0 ,11.0 )

hist_mc.Fit(gauss_fit, 'E')

canvas.Print('xmass_mc_hist.pdf')

chi2 = gauss_fit.GetChisquare()
ndof = gauss_fit.GetNDF()

mean = gauss_fit.GetParameter(1)
sig = gauss_fit.GetParameter(0)

cb_fit = ROOT.TF1("CB_fit", "crystalball", 9.0, 11.0)
# cb_fit.SetParameters(1, 2, 1, mean, sig)

hist_mc.SetStats(1)
hist_mc.SetLineColor( ROOT.kBlack )
hist_mc.SetLineWidth(2)
hist_mc.GetYaxis().SetTitle(" Number of events ")
hist_mc.GetXaxis().SetTitle("m_{ll} [MeV]")
hist_mc.Draw("pe")

hist_mc.Fit(cb_fit, 'E')

canvas.Print('xmass_mc_hist_cb.pdf')

