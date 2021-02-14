import sys
import ROOT
from utils import plot_cells

f_data = ROOT.TFile.Open('output_data.root')
f_mc   = ROOT.TFile.Open('output_mc.root')

p_data = f_data.Get('h_L2_e_profile')
p_mc   = f_mc.Get('h_L2_e_profile')

h_rw = ROOT.TH2F('h_rw', '', 7, 0, 7, 11, 0, 11)

for ieta in range(1, 8):
    for iphi in range(1, 12):
        
        e_data = p_data.GetBinContent(ieta, iphi)
        e_mc   = p_mc  .GetBinContent(ieta, iphi)

        m = e_data - e_mc

        h_rw.SetBinContent(ieta, iphi, m)



plot_cells(h_rw, 'c_rw.pdf')

of = ROOT.TFile('rw.root', 'recreate')
h_rw.Write()
of.Close()
