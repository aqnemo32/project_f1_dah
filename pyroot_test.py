import numpy as np
import ROOT
f = ROOT.TF1("f1", "sin(x)/x", 0., 10.)
TCanvas can()
f.Draw()