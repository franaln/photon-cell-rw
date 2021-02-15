import sys
import ROOT
from utils import *

def get_entry(tree_main, tree_cell, entry):

    tree_main.GetEntry(entry)

    event_number_main = getattr(tree_main, 'EventInfo.eventNumber')
            
    event_number_cells = tree_cell.EventNumber
    if (event_number_main != event_number_cells):
        st = tree_cell.GetEntryWithIndex(event_number_main)
        if st <= 0:
            return False

    event_number_cells = tree_cell.EventNumber
    if event_number_main != event_number_cells:
        return False

    return True


def pass_selection(event):

    ph_abseta = abs(getattr(event, 'ph.eta2'))
    if ph_abseta > 2.37 or (ph_abseta > 1.37 and ph_abseta < 1.52):
        return False
                
    ph_pt = getattr(event, 'ph.pt')
    if ph_pt < 10000:
        return False

    ph_l_dRmin = getattr(event, 'ph_l.dRmin')
    if ph_l_dRmin < 0.4:
        return False

    ll_m  = getattr(event, 'll.m')
    if ll_m < 40000 or ll_m > 83000:
        return False

    llg_m = getattr(event, 'llg.m')
    if llg_m < 80000 or llg_m > 100000:
        return False

    # isolation cut (??)
    if getattr(event, 'ph.isoloose') == 0:
        return False

    return True

def is_healthy_cluster(event):
    # n_L1 = event.ph_ClusterSize_7x11_L1
    n_L2 = event.ph_ClusterSize_7x11_L2
    # n_L3 = event.ph_ClusterSize_7x11_L3
            
    # if n_L1 != 112 or n_L2 != 77 or n_L3 != 44:
    #     return False

    if n_L2 != 77:
        return False

    cells_E = event.ph_ClusterCells_7x11_L2_E

    maxE, maxE_idx = 0, -1
    for ic in range(77):
        cell_E = cells_E.at(ic)
        if cell_E > maxE:
            maxE =  cell_E
            maxE_idx = ic

    if maxE_idx != 38:
        return False

    return True

def loop(paths_main, paths_cells, is_mc, luminosity, output_name, rw_file=None):

    do_rw = (is_mc and rw_file is not None)

    # Histograms
    h_L2_E_sum  = ROOT.TH1F('h_L2_E_sum', '', 1000, 0, 100000)

    h_L2_E_profile = ROOT.TProfile2D('h_L2_E_profile', '', 7, 0, 7, 11, 0, 11)
    h_L2_e_profile = ROOT.TProfile2D('h_L2_e_profile', '', 7, 0, 7, 11, 0, 11)

    h_L2_E_cell = [ ROOT.TH1F('h_L2_E_cell_%i' % (i+1), '', 5005, -100, 100000) for i in range(77) ]
    h_L2_e_cell = [ ROOT.TH1F('h_L2_e_cell_%i' % (i+1), '', 110, -0.1, 1) for i in range(77) ]

    h_Rphi_ntuple  = ROOT.TH1F('h_Rphi_ntuple', '', 100, 0, 1)
    h_Reta_ntuple  = ROOT.TH1F('h_Reta_ntuple', '', 100, 0, 1)

    if is_mc:
        h_Rphi_ntuple_fudged  = ROOT.TH1F('h_Rphi_ntuple_fudged', '', 100, 0, 1)
        h_Reta_ntuple_fudged  = ROOT.TH1F('h_Reta_ntuple_fudged', '', 100, 0, 1)

    h_Rphi  = ROOT.TH1F('h_Rphi', '', 100, 0, 1)
    h_Reta  = ROOT.TH1F('h_Reta', '', 100, 0, 1)

    if do_rw:
        h_L2_E_sum_rw  = ROOT.TH1F('h_L2_E_sum_rw', '', 1000, 0, 100000)

        h_L2_E_profile_rw = ROOT.TProfile2D('h_L2_E_profile_rw', '', 7, 0, 7, 11, 0, 11)
        h_L2_e_profile_rw = ROOT.TProfile2D('h_L2_e_profile_rw', '', 7, 0, 7, 11, 0, 11)

        h_L2_E_cell_rw = [ ROOT.TH1F('h_L2_E_cell_%i_rw' % (i+1), '', 5005, -100, 100000) for i in range(77) ]
        h_L2_e_cell_rw = [ ROOT.TH1F('h_L2_e_cell_%i_rw' % (i+1), '', 110, -0.1, 1) for i in range(77) ]
        
        h_Rphi_rw  = ROOT.TH1F('h_Rphi_rw', '', 100, 0, 1)
        h_Reta_rw  = ROOT.TH1F('h_Reta_rw', '', 100, 0, 1)

    # RW factors
    if do_rw:
        f_rw = ROOT.TFile.Open(rw_file)
        h_rw = f_rw.Get('h_rw')

        delta_rw = []
        for ic in range(77):
            ceta, cphi = get_L2_eta_phi_cell(ic)
            delta_rw.append(h_rw.GetBinContent(ceta+1, cphi+1))

    # loop over files
    for mpath, cpath in zip(paths_main, paths_cells):

        f_m = ROOT.TFile.Open(dir_main+mpath)
        f_c = ROOT.TFile.Open(dir_cells+cpath)

        tree_main  = f_m.Get('output')
        tree_cell = f_c.Get('ntuple_cells')

        tree_main.SetBranchStatus("*", 0)
        tree_cell.SetBranchStatus("*", 0)

        tree_main.SetBranchStatus("EventInfo.eventNumber", 1)
        tree_cell.SetBranchStatus("EventNumber", 1)

        tree_main.SetBranchStatus("ph.pt", 1)
        tree_main.SetBranchStatus("ph.eta2", 1)
        tree_main.SetBranchStatus("ph_l.dRmin", 1)
        tree_main.SetBranchStatus("ll.m", 1)
        tree_main.SetBranchStatus("llg.m", 1)
        tree_main.SetBranchStatus("ph.isoloose", 1)
        tree_main.SetBranchStatus("mc_weight.gen", 1)
        tree_main.SetBranchStatus("mc_weight.pu", 1)
        tree_main.SetBranchStatus("mc_weight.xs", 1)
        tree_main.SetBranchStatus("ph.noFF_rphi", 1)
        tree_main.SetBranchStatus("ph.noFF_reta", 1)
        tree_main.SetBranchStatus("ph.rphi", 1)
        tree_main.SetBranchStatus("ph.reta", 1)

        # tree_cell.SetBranchStatus("ph_ClusterSize_7x11_L1", 1);
        tree_cell.SetBranchStatus("ph_ClusterSize_7x11_L2", 1);
        # tree_cell.SetBranchStatus("ph_ClusterSize_7x11_L3", 1);

        # tree_cell.SetBranchStatus("ph_ClusterCells_7x11_L1_E", 1);
        tree_cell.SetBranchStatus("ph_ClusterCells_7x11_L2_E", 1);
        # tree_cell.SetBranchStatus("ph_ClusterCells_7x11_L3_E", 1);

        tree_cell.BuildIndex('EventNumber')
        tree_main.AddFriend(tree_cell)


        entries = tree_main.GetEntries()

        ok_entries = 0
        nosel_entries = 0
        nocell_entries = 0
        unhealthy_entries = 0

        print('Processing %i events...' % (entries))
        for entry in range(entries):

            st = get_entry(tree_main, tree_cell, entry)
            if not st:
                nocell_entries += 1
                continue

            if not pass_selection(tree_main):
                nosel_entries += 1
                continue

            if not is_healthy_cluster(tree_cell):
                unhealthy_entries += 1
                continue

            ok_entries += 1

            # weights
            weight = 1.
            if is_mc:
                weight = getattr(tree_main, "mc_weight.gen") * \
                         getattr(tree_main, "mc_weight.pu") * \
                         getattr(tree_main, "mc_weight.xs") * \
                         luminosity * 0.000001

                
            # Layer 2
            cells_E = tree_cell.ph_ClusterCells_7x11_L2_E

            sumE = 0
            for ic in range(77):
                sumE += cells_E.at(ic)

            h_L2_E_sum.Fill(sumE, weight)
                
            for ic in range(77):
                cell_E = cells_E.at(ic)
                cell_E_norm = cell_E / sumE

                h_L2_E_cell[ic].Fill(cell_E, weight)
                h_L2_e_cell[ic].Fill(cell_E_norm, weight)

                ceta, cphi = get_L2_eta_phi_cell(ic)

                h_L2_E_profile.Fill(ceta+0.5, cphi+0.5, cell_E, weight)
                h_L2_e_profile.Fill(ceta+0.5, cphi+0.5, cell_E_norm, weight)

            # Recompute SS
            cells_E = tree_cell.ph_ClusterCells_7x11_L2_E

            e_33 = sum_L2_energy(3, 3, cells_E)
            e_37 = sum_L2_energy(3, 7, cells_E)
            e_77 = sum_L2_energy(7, 7, cells_E)

            rphi = e_33 / e_37
            reta = e_37 / e_77
            
            h_Rphi.Fill(rphi, weight)
            h_Reta.Fill(reta, weight)

            if is_mc:
                h_Rphi_ntuple.Fill(getattr(tree_main, 'ph.noFF_rphi'), weight)
                h_Reta_ntuple.Fill(getattr(tree_main, 'ph.noFF_reta'), weight)

                h_Rphi_ntuple_fudged.Fill(getattr(tree_main, 'ph.rphi'), weight)
                h_Reta_ntuple_fudged.Fill(getattr(tree_main, 'ph.reta'), weight)
            else:
                h_Rphi_ntuple.Fill(getattr(tree_main, 'ph.rphi'), weight)
                h_Reta_ntuple.Fill(getattr(tree_main, 'ph.reta'), weight)

            # RW
            if do_rw:

                # correct cells
                cells_E_rw = ROOT.vector('float')()
                for ic in range(77):

                    E_rw = cells_E.at(ic) + sumE * delta_rw[ic]

                    cells_E_rw.push_back(E_rw)


                # re-compute variables with corrected cells
                e_33 = sum_L2_energy(3, 3, cells_E_rw)
                e_37 = sum_L2_energy(3, 7, cells_E_rw)
                e_77 = sum_L2_energy(7, 7, cells_E_rw)

                rphi = e_33 / e_37
                reta = e_37 / e_77
            
                h_Rphi_rw.Fill(rphi, weight)
                h_Reta_rw.Fill(reta, weight)

                # sumE should be the same, right?
                sumE = 0
                for ic in range(77):
                    sumE += cells_E_rw.at(ic)

                h_L2_E_sum_rw.Fill(sumE, weight)

                for ic in range(77):
                    cell_E = cells_E_rw.at(ic)
                    cell_E_norm = cell_E / sumE

                    h_L2_E_cell_rw[ic].Fill(cell_E, weight)
                    h_L2_e_cell_rw[ic].Fill(cell_E_norm, weight)

                    ceta, cphi = get_L2_eta_phi_cell(ic)

                    h_L2_E_profile_rw.Fill(ceta+0.5, cphi+0.5, cell_E, weight)
                    h_L2_e_profile_rw.Fill(ceta+0.5, cphi+0.5, cell_E_norm, weight)


            
        print("Total Entries = %i, ok = %i, no pass selection = %i, no cell info = %i, unhealthy = %i" % (entries, ok_entries, nosel_entries, nocell_entries, unhealthy_entries))


    print('Saving histograms in %s' % output_name)
    of = ROOT.TFile(output_name, 'recreate')

    h_L2_E_sum.Write()
    h_L2_E_profile.Write()
    h_L2_e_profile.Write()
    for i in range(77):
        h_L2_E_cell[i].Write()
        h_L2_e_cell[i].Write()

    h_Rphi_ntuple.Write()
    h_Reta_ntuple.Write()

    if is_mc:
        h_Rphi_ntuple_fudged.Write()
        h_Reta_ntuple_fudged.Write()

    h_Rphi.Write()
    h_Reta.Write()

    if do_rw:
        h_L2_E_sum_rw.Write()
        h_L2_E_profile_rw.Write()
        h_L2_e_profile_rw.Write()

        for i in range(77):
            h_L2_E_cell_rw[i].Write()
            h_L2_e_cell_rw[i].Write()

        h_Rphi_rw.Write()
        h_Reta_rw.Write()

    of.Close()
        
    return 




##
dir_main   = '/eos/atlas/atlascerngroupdisk/perf-egamma/photonID/NTUP_ZLLG/'
dir_cells  = '/eos/user/f/falonso/data/PhotonID/Cells/Zrad_00-03-01/'

ntuples_mc = [
    'mc16a_13TeV/00-03-01/mc16a.Sh_224_NN30NNLO_eegamma_LO_pty_7_15.DAOD_EGAM3.e7006_e5984_s3126_r9364_r9315_p3956.root',
    'mc16a_13TeV/00-03-01/mc16a.Sh_224_NN30NNLO_eegamma_LO_pty_15_35.DAOD_EGAM3.e7006_e5984_s3126_r9364_r9315_p3956.root',
    'mc16a_13TeV/00-03-01/mc16a.Sh_224_NN30NNLO_eegamma_LO_pty_35_70.DAOD_EGAM3.e7006_e5984_s3126_r9364_r9315_p3956.root',
    'mc16a_13TeV/00-03-01/mc16a.Sh_224_NN30NNLO_eegamma_LO_pty_70_140.DAOD_EGAM3.e7006_e5984_s3126_r9364_r9315_p3956.root',
    'mc16a_13TeV/00-03-01/mc16a.Sh_224_NN30NNLO_eegamma_LO_pty_140_E_CMS.DAOD_EGAM3.e7006_e5984_s3126_r9364_r9315_p3956.root',
]

ntuples_data = [
    'data15_13TeV/00-03-01/target_data15_Zeeg_p3948.root',
    'data16_13TeV/00-03-01/target_data16_Zeeg_p3948.root',
]

cells_mc = [
    'mc16a_13TeV_366140_DAOD_EGAM3_cells.root',
    'mc16a_13TeV_366141_DAOD_EGAM3_cells.root',
    'mc16a_13TeV_366142_DAOD_EGAM3_cells.root',
    'mc16a_13TeV_366143_DAOD_EGAM3_cells.root',
    'mc16a_13TeV_366144_DAOD_EGAM3_cells.root',
]

cells_data = [
    'data15_13TeV_periodAllYear_DAOD_EGAM3_cells.root',
    'data16_13TeV_periodAllYear_DAOD_EGAM3_cells.root',
]


if len(sys.argv) > 1:
    loop(ntuples_mc,   cells_mc,   True,  36184.86, 'output_mc_rw.root', sys.argv[1])
else:
    loop(ntuples_mc,   cells_mc,   True,  36184.86, 'output_mc.root')
    loop(ntuples_data, cells_data, False, 36184.86, 'output_data.root')




