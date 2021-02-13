import ROOT

from utils import *

def loop(paths_main, paths_cells, is_mc, luminosity, output_name):

    # Histograms
    h_L2_E_sum  = ROOT.TH1F('h_L2_E_sum', '', 1000, 0, 100000)

    h_L2_E_cell = [ ROOT.TH1F('h_L2_E_cell_%i' % (i+1), '', 5005, -100, 100000) for i in range(77) ]
    h_L2_e_cell = [ ROOT.TH1F('h_L2_e_cell_%i' % (i+1), '', 200, -1, 1) for i in range(77) ]

    h_L2_E_profile = ROOT.TProfile2D('h_L2_E_profile', '', 7, 0, 7, 11, 0, 11)
    h_L2_e_profile = ROOT.TProfile2D('h_L2_e_profile', '', 7, 0, 7, 11, 0, 11)

    # loop over files
    for mpath, cpath in zip(paths_main, paths_cells):

        f_m = ROOT.TFile.Open(dir_main+mpath)
        f_c = ROOT.TFile.Open(dir_cells+cpath)

        tree_main  = f_m.Get('output')
        tree_cell = f_c.Get('ntuple_cells')

        prepare_trees(tree_main, tree_cell)

        entries = tree_main.GetEntries()

        ok_entries = 0
        nocell_entries = 0
        unhealthy_entries = 0

        print('Processing %i events...' % (entries))
        for entry in range(entries):

            st = get_entry(tree_main, tree_cell, entry)
            if not st:
                nocell_entries += 1
                continue

            if not pass_acceptance_cut(tree_main):
                continue

            if not is_healthy_cluster(tree_cell):
                unhealthy_entries += 1
                continue

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
            for ic in range(n_L2):
                sumE +== cells_E.at(ic)

            h_L2_E_sum.Fill(sumE, weight)
                
            ieta, iphi = 1, 1
            for ic in range(77):
                cell_E = cells_E.at(ic)
                cell_E_norm = cell_E / sumE

                h_L2_E_cell[ic].Fill(cell_E, weight)
                h_L2_e_cell[ic].Fill(cell_E_norm, weight)

                h_L2_E_profile.Fill(ieta-0.5, iphi-0.5, cell_E, weight)
                h_L2_e_profile.Fill(ieta-0.5, iphi-0.5, cell_E_norm, weight)

                iphi += 1
                if iphi > 11:
                    ieta += 1
                    iphi = 1


            ok_entries += 1
            

        print("Total Entries = %i, ok = %i, no cell info = %i, unhealthy = %i" % (entries, ok_entries, nocell_entries, unhealthy_entries))


    print('Saving histograms in %s' % output_name)
    of = ROOT.TFile(output_name, 'recreate')

    h_L2_E_sum.Write()
    for i in range(77):
        h_L2_E_cell[i].Write()
        h_L2_e_cell[i].Write()

    h_L2_E_profile.Write()
    h_L2_e_profile.Write()
    of.Close()
        
    return 




##
loop(ntuples_mc,   cells_mc,   True,  36184.86, 'output_mc.root')
loop(ntuples_data, cells_data, False, 36184.86, 'output_data.root')
