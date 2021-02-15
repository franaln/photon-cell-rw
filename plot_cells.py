import ROOT

f_d = ROOT.TFile.Open('output_data.root')
f_m = ROOT.TFile.Open('output_mc_rw.root')

for cell in range(38, 41):

    h_data  = f_d.Get('h_L2_e_cell_%i' % cell)
    h_mc    = f_m.Get('h_L2_e_cell_%i' % cell)
    h_mc_rw = f_m.Get('h_L2_e_cell_%i_rw' % cell)

    h_data.Scale(1/h_data.Integral())
    h_mc.Scale(1/h_mc.Integral())
    h_mc_rw.Scale(1/h_mc_rw.Integral())
    
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(1.2)
    h_data.SetMarkerColor(ROOT.kBlack)
    h_data.SetLineColor(ROOT.kBlack)

    h_mc.SetLineWidth(2)
    h_mc.SetLineColor(ROOT.kRed)

    h_mc_rw.SetLineWidth(2)
    h_mc_rw.SetLineColor(ROOT.kBlue)

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

    cup.SetLogy()

    cup.Draw()
    cdown.Draw()

    cup.cd()

    h_data.SetTitle('')
    h_data.SetStats(0)

    if cell == 39:
        xmin, xmax = 0, 1
    else:
        xmin, xmax = -0.1, 0.5

    h_data.GetXaxis().SetRangeUser(xmin, xmax)
    h_data.GetYaxis().SetTitle('a.u.')
    h_data.GetYaxis().SetTitleOffset(1.5)

    h_data.GetYaxis().SetLabelFont(43)
    h_data.GetYaxis().SetLabelSize(18)
    h_data.GetYaxis().SetTitleFont(43)
    h_data.GetYaxis().SetTitleSize(18)

    h_data.Draw()
    h_mc.Draw('hist same')
    h_mc_rw.Draw('hist same')

    leg = ROOT.TLegend(0.65, 0.65, 0.85, 0.9)
    leg.SetBorderSize(0)
    leg.AddEntry(h_data, 'Data', 'p')
    leg.AddEntry(h_mc,   'MC', 'l')
    leg.AddEntry(h_mc_rw,   'MC rw', 'l')
    leg.Draw()


    # Ratios (MC/Data)
    cdown.cd()

    r_mc = h_mc.Clone()
    r_mc.Divide(h_data)

    r_mc_rw = h_mc_rw.Clone()
    r_mc_rw.Divide(h_data)


    r_mc.SetStats(0)

    ax = r_mc.GetXaxis()
    ay = r_mc.GetYaxis()

    ax.SetTitle('E (cell %i)/E' % cell)
    ay.SetTitle('MC/Data')
    ay.CenterTitle()

    ay.SetNdivisions(504)
    ay.SetRangeUser(0, 2)

    ax.SetRangeUser(xmin, xmax)

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

    c1.SaveAs('c_e_cell_%i.pdf' % cell)
