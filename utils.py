import ROOT
from array import array

def get_L2_eta_phi_cell(idx):
    cphi = int(idx % 11)
    ceta = int((idx-cphi) / 11)
    return ceta, cphi

def sum_L2_energy(eta, phi, clusterEnergy):

    etaSize = 7
    phiSize = 11

    etaMin = int(etaSize - 0.5 * (etaSize + eta))
    etaMax = int(etaSize - 0.5 * (etaSize - eta))
    phiMin = int(phiSize - 0.5 * (phiSize + phi))
    phiMax = int(phiSize - 0.5 * (phiSize - phi))

    sumEE = 0
    for e in range(etaMin, etaMax):
        for p in range(phiMin, phiMax):
            sumEE += clusterEnergy.at(p+phiSize*e)

    return sumEE


def calc_weta2(clusterEnergy, clusterEta):

    sumE_3x5 = 0
    sumE_Eta = 0
    sumE_EtaSq = 0
    for phi in range(3, 8):
        for eta in range(2, 5):
            a_e = clusterEnergy.at(phi+11*eta)
            a_eta = abs(clusterEta.at(phi+11*eta))

            sumE_3x5 += a_e
            sumE_Eta += a_e * a_eta
            sumE_EtaSq +=  a_e * a_eta * a_eta

    return math.sqrt( sumE_EtaSq/sumE_3x5 - (sumEEta/sumE3x5)**2)


def plot_cells(h, name):

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)

    stops = array('d', [0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000])
    r = array('d', [ 70./255., 102./255., 157./255., 188./255., 196./255., 214./255., 223./255., 235./255., 251./255.])
    g = array('d', [ 37./255.,  29./255.,  25./255.,  37./255.,  67./255.,  91./255., 132./255., 185./255., 251./255.])
    b = array('d', [ 37./255.,  32./255.,  33./255.,  45./255.,  66./255.,  98./255., 137./255., 187./255., 251./255.])
    # r = array('d', [ 37./255.,  32./255.,  33./255.,  45./255.,  66./255.,  98./255., 137./255., 187./255., 251./255.])
    # g = array('d', [ 37./255.,  29./255.,  25./255.,  37./255.,  67./255.,  91./255., 132./255., 185./255., 251./255.])
    # b = array('d', [ 37./255., 102./255., 157./255., 188./255., 196./255., 214./255., 223./255., 235./255., 251./255.])

    ROOT.TColor.CreateGradientColorTable(len(stops), stops, r, g, b, 999)
    ROOT.gStyle.SetNumberContours(999)
    ROOT.TColor.InvertPalette()

    c = ROOT.TCanvas('', '', 800, 800)

    c.SetRightMargin(0.15)
    c.SetTicks()

    ax = h.GetXaxis()
    ay = h.GetYaxis()

    nx = h.GetNbinsX()
    ny = h.GetNbinsY()

    for i in range(1, nx+1):
        ax.SetBinLabel(i, str(i))

    for i in range(1, ny+1):
        ay.SetBinLabel(i, str(i))

    ay.SetTitle('Cell (#phi direction)')
    ax.SetTitle('Cell (#eta direction)')

    h.SetContour(999)
    # h.GetZaxis().SetRangeUser(0, zmax)
    h.Draw('colz text')

    c.RedrawAxis()

    c.SaveAs(name)

