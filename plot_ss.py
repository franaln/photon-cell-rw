import ROOT

f_d = ROOT.TFile.Open('output_data.root')
f_m = ROOT.TFile.Open('output_mc_rw.root')

for variable in ('Rphi', 'Reta'):

    h_data_ss  = f_d.Get('h_%s' % variable)
    h_mc_ss    = f_m.Get('h_%s' % variable)
    h_mc_ss_rw = f_m.Get('h_%s_rw' % variable)

    # h_data_ss_ntuple  = f_d.Get('h_%s_ntuple' % variable)
    # h_mc_ss_ntuple    = f_m.Get('h_%s_ntuple' % variable)
    h_mc_ss_ntuple_fudged = f_m.Get('h_%s_ntuple_fudged' % variable)

    h_data_ss.Scale(1/h_data_ss.Integral())
    h_mc_ss.Scale(1/h_mc_ss.Integral())
    h_mc_ss_rw.Scale(1/h_mc_ss_rw.Integral())

    # h_data_ss_ntuple.Scale(1/h_data_ss_ntuple.Integral())
    # h_mc_ss_ntuple.Scale(1/h_mc_ss_ntuple.Integral())
    h_mc_ss_ntuple_fudged.Scale(1/h_mc_ss_ntuple_fudged.Integral())

    h_data_ss.SetMarkerStyle(20)
    h_data_ss.SetMarkerSize(1.2)
    h_data_ss.SetMarkerColor(ROOT.kBlack)
    h_data_ss.SetLineColor(ROOT.kBlack)

    h_mc_ss.SetLineColor(ROOT.TColor.GetColor('#FF2545'))
    h_mc_ss_rw.SetLineColor(ROOT.TColor.GetColor('#3F5BFF'))

    h_mc_ss.SetLineWidth(2)    
    h_mc_ss_rw.SetLineWidth(2)

    # h_data_ss_ntuple.SetLineStyle(2)
    # h_data_ss_ntuple.SetLineColor(ROOT.kBlue)

    # h_mc_ss_ntuple.SetLineColor(ROOT.kRed)
    # h_mc_ss_ntuple.SetLineStyle(2)
    h_mc_ss_ntuple_fudged.SetLineColor(ROOT.TColor.GetColor('#F19200'))
    h_mc_ss_ntuple_fudged.SetLineStyle(2)
    h_mc_ss_ntuple_fudged.SetLineWidth(2)

    c = ROOT.TCanvas('', '', 800, 800)

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

    #cup.SetLogy()

    cup.Draw()
    cdown.Draw()

    cup.cd()

    h_data_ss.SetTitle('')
    h_data_ss.SetStats(0)

    h_data_ss.GetYaxis().SetRangeUser(0, 0.25)
    h_data_ss.GetXaxis().SetRangeUser(0.8, 1)
    h_data_ss.GetYaxis().SetTitle('Entries')
    h_data_ss.GetYaxis().SetTitleOffset(1.5)

    h_data_ss.GetYaxis().SetLabelFont(43)
    h_data_ss.GetYaxis().SetLabelSize(18)
    h_data_ss.GetYaxis().SetTitleFont(43)
    h_data_ss.GetYaxis().SetTitleSize(18)

    h_data_ss.Draw()
    h_mc_ss.Draw('hist same')
    h_mc_ss_rw.Draw('hist same')

    # h_data_ss_ntuple.Draw('hist same')
    # h_mc_ss_ntuple.Draw('hist same')
    h_mc_ss_ntuple_fudged.Draw('hist same')

    leg = ROOT.TLegend(0.15, 0.65, 0.45, 0.9)
    leg.SetBorderSize(0)
    leg.AddEntry(h_data_ss, 'Data')
    leg.AddEntry(h_mc_ss,   'MC')
    leg.AddEntry(h_mc_ss_ntuple_fudged,   'MC fudged')
    leg.AddEntry(h_mc_ss_rw, 'MC re-weighted')
    leg.Draw()


    # Ratios (MC/Data)
    cdown.cd()

    r_mc      = h_mc_ss.Clone()
    r_mc.Divide(h_data_ss)

    r_mc_rw      = h_mc_ss_rw.Clone()
    r_mc_rw.Divide(h_data_ss)

    r_mc_ntuple_fudged      = h_mc_ss_ntuple_fudged.Clone()
    r_mc_ntuple_fudged.Divide(h_data_ss)


    r_mc.SetStats(0)

    r_mc.GetXaxis().SetTitle(variable)
    r_mc.GetYaxis().SetTitle('MC/Data')
    r_mc.GetYaxis().CenterTitle()

    r_mc.GetXaxis().SetRangeUser(0.8, 1) ##xranges[variable][0], xranges[variable][1])
    r_mc.GetYaxis().SetNdivisions(504)
    r_mc.GetYaxis().SetRangeUser(0.4, 1.6)

    r_mc.GetXaxis().SetLabelFont(43)
    r_mc.GetXaxis().SetLabelSize(18)
    r_mc.GetYaxis().SetLabelFont(43)
    r_mc.GetYaxis().SetLabelSize(18)

    r_mc.GetXaxis().SetTitleFont(43)
    r_mc.GetXaxis().SetTitleSize(18)
    r_mc.GetYaxis().SetTitleFont(43)
    r_mc.GetYaxis().SetTitleSize(18)

    r_mc.GetXaxis().SetTitleOffset(3.5)
    r_mc.GetYaxis().SetTitleOffset(2.0)

    r_mc.Draw('hist same')
    r_mc_rw.Draw('hist same')
    r_mc_ntuple_fudged.Draw('hist same')

    c.SaveAs('ss_%s.pdf' % variable)
