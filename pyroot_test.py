import ROOT
import numpy as np
import matplotlib.pyplot as plt

# Analysis of the MC data

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


gauss_fit_mc = ROOT.TF1(" gaussfit ", "gaus" ,9.0 ,10.0 )

hist_mc.Fit(gauss_fit_mc, 'E')

canvas.Print ( 'xmass_mc_hist.pdf')


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
hist_mc_prime.GetXaxis().SetTitle("m_{ll} [GeV/c^{2}]")
hist_mc_prime.Draw("pe")

hist_mc_prime.Fit(f_cb, 'E') #worked up till here

x= []
for i  in range(5):
    x.append(f_cb.GetParameter(i))

print(x)

alpha_cb = x[3]
n_cb = x[4]

canvas.Print ('xmass_mc_hist_cb.pdf')

chi2_cb = f_cb.GetChisquare()
ndof_cb = f_cb.GetNDF()

print(f"{chi2_gauss/ndof_gauss = }\n{chi2_cb/ndof_cb = }")

# Analysis of the Upsilon data

xmass_dirty = np.load('ups_anal/xmass.npy')
tran_1_ups = np.load('ups_anal/mom_tran_1.npy')
tran_2_ups = np.load('ups_anal/mom_tran_2.npy')


#Cleaning the data using the trnasverse momenta of both particles
R = np.absolute(tran_2_ups - tran_1_ups)/(tran_2_ups + tran_1_ups)

xmass = xmass_dirty[R<0.42]

hist_ups = ROOT.TH1F('xmass ','Number of Events versus Muon Pair Invariant Mass ' ,422 ,bins[0], bins[-1])
hist_ups.Sumw2

for i in xmass:
    hist_ups.Fill(i)

hist_ups.SetDirectory(0)

hist_ups.SetStats(0)
hist_ups.SetLineColor( ROOT.kBlue )
hist_ups.SetLineWidth(2)
hist_ups.GetYaxis().SetTitle(" Number of events ")
hist_ups.GetXaxis().SetTitle("m_{\mu^{+} \mu^{-}} [GeV/c^{2}]")
hist_ups.Draw("pe")

canvas.Print ('xmass_hist.pdf')

# Create gaussian pdf to fit to the Upsilon data

# g_1 = "exp(0.5*((x-[0])/[1])**2)"
# g_2 = "exp(0.5*((x-[2])/[3])**2)"
# g_3 = "exp(0.5*((x-[4])/[5])**2)"
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

canvas.Print('test_gauss_pdf.pdf')

hist_ups.SetDirectory(0)

hist_ups.SetStats(0)
hist_ups.SetLineColor( ROOT.kBlue )
hist_ups.SetLineWidth(2)
hist_ups.GetYaxis().SetTitle(" Number of events ")
hist_ups.GetXaxis().SetTitle("m_{\mu^{+} \mu^{-}} [GeV/c^{2}]")
hist_ups.Draw("pe")

hist_ups.Fit(gauss_fit, 'E')


a = []
for i in range(12):
    a.append(gauss_fit.GetParameter(i))




canvas.Print ('xmass_hist_gauss.pdf')


# Create a double gaussian pdf to fit the Upsilon data

# For Double Gauss parameters in order are:
#       A, mu, sigma * 2 + b (Normalisaton between both gaussians)

d_g_1 = "[5]*[0]*exp(-0.5*((x-[1])/[2])^2) + (1-[5])*[3]*exp(-0.5*((x-[1])/[4])^2)" # 0,1,2 - 3,1,4 - 5
d_g_2 = "[11]*[6]*exp(-0.5*((x-[7])/[8])^2) + (1-[11])*[9]*exp(-0.5*((x-[7])/[10])^2)" # 6,7,8 - 9,7,10 - 11
d_g_3 = "[17]*[12]*exp(-0.5*((x-[13])/[14])^2) + (1-[17])*[12]*exp(-0.5*((x-[13])/[16])^2)" # 12,13,14 - 15,13,16 - 17
decay_dg = "[20]*expo(18)" # 18,19 - 20

pdf_d_gauss = "((%s) + (%s) + (%s) + (%s))"%(d_g_1, d_g_2, d_g_3, decay_dg)

d_gauss_fit = ROOT.TF1("Double Gaussian Fit", pdf_d_gauss, bins[0], bins[-1])


# Peak 1
d_gauss_fit.SetParameter(0, 3500)
d_gauss_fit.SetParameter(1, 9.45)
d_gauss_fit.SetParameter(2, 0.01)
d_gauss_fit.SetParameter(3, 3000)
d_gauss_fit.SetParameter(4, 0.06)
d_gauss_fit.SetParameter(5, 0.5)

# Peak 2
d_gauss_fit.SetParameter(6, 800)
d_gauss_fit.SetParameter(7, 10.01)
d_gauss_fit.SetParameter(8, 0.01)
d_gauss_fit.SetParameter(9, 800)
d_gauss_fit.SetParameter(10, 0.05)
d_gauss_fit.SetParameter(11, 0.6)

# Peak 3
d_gauss_fit.SetParameter(12, 350)
d_gauss_fit.SetParameter(13, 10.35)
d_gauss_fit.SetParameter(14, 0.01)
d_gauss_fit.SetParameter(15, 350)
d_gauss_fit.SetParameter(16, 0.05)
d_gauss_fit.SetParameter(17, 0.6)

# Decay
d_gauss_fit.SetParameter(18, 6)
d_gauss_fit.SetParameter(19, -0.6)
d_gauss_fit.SetParameter(20, 1000)


d_gauss_fit.SetLineColor(ROOT.kBlack)
d_gauss_fit.SetLineWidth(2)
d_gauss_fit.Draw()

canvas.Print('test_d_gauss_pdf.pdf')

hist_ups.SetDirectory(0)

hist_ups.SetStats(0)
hist_ups.SetLineColor( ROOT.kBlue )
hist_ups.SetLineWidth(2)
hist_ups.GetYaxis().SetTitle(" Number of events ")
hist_ups.GetXaxis().SetTitle("m_{\mu^{+} \mu^{-}} [GeV/c^{2}]")
hist_ups.Draw("pe")

hist_ups.Fit(d_gauss_fit, 'E')



canvas.Print ('xmass_hist_d_gauss.pdf')


# Create a Crystal Ball pdf to fit the Upsilon data

cb_1 = "crystalball(0)" #0,1,2,3,4
cb_2 = "crystalball(5)" #5,6,7,8,9
cb_3 = "crystalball(10)" #10,11,12,13,14
decay_cb = "[17]*expo(15)" #15,16,17

pdf_cb = "((%s) + (%s) + (%s) + (%s))"%(cb_1, cb_2, cb_3, decay_cb)

cb_fit = ROOT.TF1("Crystal Ball PDF", pdf_cb, bins[0], bins[-1])

# Parameter Naming Converntion:
#     N = Normalisation
#     mu = mean
#     sig = standard deviation
#     alpha = Alpha of Crystal Ball
#     n = n of Crystal Ball

#Crystal Ball 1
cb_fit.SetParameter(0,3600)
cb_fit.SetParName(0,"N 1")
cb_fit.SetParameter(1,9.45)
cb_fit.SetParName(1,"mu 1")
cb_fit.SetParameter(2,0.03)
cb_fit.SetParName(2,"sig 1")

cb_fit.SetParameter(3,alpha_cb)
cb_fit.SetParName(3,"alpha 1")
cb_fit.FixParameter(3, alpha_cb)
cb_fit.SetParameter(4,n_cb)
cb_fit.SetParName(4,"n 1")
cb_fit.FixParameter(4, n_cb)

#Crystal Ball 2
cb_fit.SetParameter(5,700)
cb_fit.SetParName(5,"N 2")
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
cb_fit.SetParName(10,"N 3")
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
cb_fit.SetParameter(17,938.068)

cb_fit.SetLineColor(ROOT.kBlack)
cb_fit.SetLineWidth(2)
cb_fit.Draw()

canvas.Print('test_cb_pdf.pdf')

hist_ups.SetDirectory(0)

hist_ups.SetStats(0)
hist_ups.SetLineColor( ROOT.kBlue )
hist_ups.SetLineWidth(2)
hist_ups.GetYaxis().SetTitle(" Number of events ")
hist_ups.GetXaxis().SetTitle("m_{\mu^{+} \mu^{-}} [GeV/c^{2}]")
hist_ups.Draw("pe")

hist_ups.Fit(cb_fit, 'E')



canvas.Print ('xmass_hist_cb.pdf')
