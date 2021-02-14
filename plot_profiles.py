import ROOT

from utils import plot_cells

f_d = ROOT.TFile.Open('output_data.root')
f_m = ROOT.TFile.Open('output_mc_rw.root')

p_data  = f_d.Get('h_L2_e_profile')
p_mc    = f_m.Get('h_L2_e_profile')
p_mc_rw = f_m.Get('h_L2_e_profile_rw')

# Projections
h_eta_data  = p_data.ProjectionX().Clone()
h_eta_mc    = p_mc.ProjectionX().Clone()
h_eta_mc_rw = p_mc_rw.ProjectionX().Clone()

h_phi_data  = p_data.ProjectionY().Clone()
h_phi_mc    = p_mc.ProjectionY().Clone()
h_phi_mc_rw = p_mc_rw.ProjectionY().Clone()

# 2D profiles
plot_cells(p_data,  'p_2D_data.pdf')
plot_cells(p_mc,    'p_2D_mc.pdf')
plot_cells(p_mc_rw, 'p_2D_mc_rw.pdf')


# 1D profiles
h_eta_data.SetMarkerStyle(20)
h_eta_data.SetMarkerSize(1.2)
h_eta_data.SetMarkerColor(ROOT.kBlack)
h_eta_data.SetLineColor(ROOT.kBlack)

h_phi_data.SetMarkerStyle(20)
h_phi_data.SetMarkerSize(1.2)
h_phi_data.SetMarkerColor(ROOT.kBlack)
h_phi_data.SetLineColor(ROOT.kBlack)

h_eta_mc.SetLineWidth(2)
h_phi_mc.SetLineWidth(2)
h_eta_mc.SetLineColor(ROOT.kRed)
h_phi_mc.SetLineColor(ROOT.kRed)

h_eta_mc_rw.SetLineWidth(2)
h_phi_mc_rw.SetLineWidth(2)
h_eta_mc_rw.SetLineColor(ROOT.kBlue)
h_phi_mc_rw.SetLineColor(ROOT.kBlue)

# eta profile
c1 = ROOT.TCanvas('', '', 800, 800)

cup   = ROOT.TPad("u", "u", 0., 0.305, 1, 1)
cdown = ROOT.TPad("d", "d", 0., 0.01, 1, 0.295)

cup.SetTicks()
cdown.SetTicks()
cdown.SetGridy()

cup.SetBottomMargin(0)
cup.SetRightMargin (0.05)
cup.SetLeftMargin  (0.10)
cup.SetTopMargin   (0.05)

cdown.SetTickx()
cdown.SetTicky()
cdown.SetTopMargin   (0)
cdown.SetRightMargin (0.05)
cdown.SetLeftMargin  (0.10)
cdown.SetBottomMargin(0.20)

##cup.SetLogy()

cup.Draw()
cdown.Draw()

cup.cd()

h_eta_data.SetTitle('')
h_eta_data.SetStats(0)

h_eta_data.GetYaxis().SetRangeUser(0, 0.8)
h_eta_data.GetYaxis().SetTitle('Normalized Energy')
h_eta_data.GetYaxis().SetTitleOffset(1.5)

h_eta_data.GetYaxis().SetLabelFont(43)
h_eta_data.GetYaxis().SetLabelSize(18)
h_eta_data.GetYaxis().SetTitleFont(43)
h_eta_data.GetYaxis().SetTitleSize(18)

h_eta_data.Draw()
h_eta_mc.Draw('hist same')
h_eta_mc_rw.Draw('hist same')

leg = ROOT.TLegend(0.15, 0.65, 0.45, 0.9)
leg.SetBorderSize(0)
leg.AddEntry(h_eta_data, 'Data', 'p')
leg.AddEntry(h_eta_mc,   'MC', 'l')
leg.AddEntry(h_eta_mc_rw,   'MC reweighted', 'l')
leg.Draw()


# Ratios (MC/Data)
cdown.cd()

r_mc = h_eta_mc.Clone()
r_mc.Divide(h_eta_data)

r_mc_rw = h_eta_mc_rw.Clone()
r_mc_rw.Divide(h_eta_data)


r_mc.SetStats(0)

ax = r_mc.GetXaxis()
ay = r_mc.GetYaxis()

ax.SetTitle('Cells (#eta-profile)')
ay.SetTitle('MC/Data')
ay.CenterTitle()

ay.SetNdivisions(504)
ay.SetRangeUser(0.8, 1.2)

for i in range(1, 8):
    ax.SetBinLabel(i, str(i))

ax.SetLabelFont(43)
ax.SetLabelSize(18)
ax.SetTitleFont(43)
ax.SetTitleSize(18)

ay.SetLabelFont(43)
ay.SetLabelSize(18)
ay.SetTitleFont(43)
ay.SetTitleSize(18)

ax.SetTitleOffset(3.5)
ay.SetTitleOffset(2.0)

r_mc.Draw('hist same')
r_mc_rw.Draw('hist same')

c1.SaveAs('p_eta.pdf')


# phi profile
c2 = ROOT.TCanvas('', '', 800, 800)

cup   = ROOT.TPad("u", "u", 0., 0.305, 1, 1)
cdown = ROOT.TPad("d", "d", 0., 0.01, 1, 0.295)

cup.SetTicks()
cdown.SetTicks()
cdown.SetGridy()

cup.SetBottomMargin(0)
cup.SetRightMargin (0.05)
cup.SetLeftMargin  (0.10)
cup.SetTopMargin   (0.05)

cdown.SetTickx()
cdown.SetTicky()
cdown.SetTopMargin   (0)
cdown.SetRightMargin (0.05)
cdown.SetLeftMargin  (0.10)
cdown.SetBottomMargin(0.20)

cup.Draw()
cdown.Draw()

cup.cd()

h_phi_data.SetTitle('')
h_phi_data.SetStats(0)

h_phi_data.GetYaxis().SetRangeUser(0, 0.8)
h_phi_data.GetYaxis().SetTitle('Normalized Energy')
h_phi_data.GetYaxis().SetTitleOffset(1.5)

h_phi_data.GetYaxis().SetLabelFont(43)
h_phi_data.GetYaxis().SetLabelSize(18)
h_phi_data.GetYaxis().SetTitleFont(43)
h_phi_data.GetYaxis().SetTitleSize(18)

h_phi_data.Draw()
h_phi_mc.Draw('hist same')
h_phi_mc_rw.Draw('hist same')

leg = ROOT.TLegend(0.15, 0.65, 0.45, 0.9)
leg.SetBorderSize(0)
leg.AddEntry(h_phi_data, 'Data', 'p')
leg.AddEntry(h_phi_mc,   'MC', 'l')
leg.AddEntry(h_phi_mc_rw,   'MC reweighted', 'l')
leg.Draw()


# Ratios (MC/Data)
cdown.cd()

r_mc      = h_phi_mc.Clone()
r_mc.Divide(h_phi_data)

r_mc_rw      = h_phi_mc_rw.Clone()
r_mc_rw.Divide(h_phi_data)

r_mc.SetStats(0)

ax = r_mc.GetXaxis()
ay = r_mc.GetYaxis()

ax.SetTitle('#phi-profile')
ay.SetTitle('MC/Data')
ay.CenterTitle()

ay.SetNdivisions(504)
ay.SetRangeUser(0.8, 1.2)

for i in range(1, 12):
    ax.SetBinLabel(i, str(i))

ax.SetLabelFont(43)
ax.SetLabelSize(18)
ay.SetLabelFont(43)
ay.SetLabelSize(18)

ax.SetTitleFont(43)
ax.SetTitleSize(18)
ay.SetTitleFont(43)
ay.SetTitleSize(18)

ax.SetTitleOffset(3.5)
ay.SetTitleOffset(2.0)

r_mc.Draw('hist same')
r_mc_rw.Draw('hist same')

c2.SaveAs('p_phi.pdf')
