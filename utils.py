import ROOT

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

def prepare_trees(tree_main, tree_cell):
    tree_main.SetBranchStatus("*", 0)
    tree_cell.SetBranchStatus("*", 0)

    tree_main.SetBranchStatus("EventInfo.eventNumber", 1)
    tree_cell.SetBranchStatus("EventNumber", 1)

    tree_main.SetBranchStatus("ph.pt", 1)
    tree_main.SetBranchStatus("ph.eta2", 1)
    tree_main.SetBranchStatus("mc_weight.gen", 1)
    tree_main.SetBranchStatus("mc_weight.pu", 1)
    tree_main.SetBranchStatus("mc_weight.xs", 1)
    tree_main.SetBranchStatus("ph.noFF_rphi", 1)
    tree_main.SetBranchStatus("ph.noFF_reta", 1)
    tree_main.SetBranchStatus("ph.rphi", 1)
    tree_main.SetBranchStatus("ph.reta", 1)

    tree_cell.SetBranchStatus("ph_ClusterSize_7x11_L1", 1);
    tree_cell.SetBranchStatus("ph_ClusterSize_7x11_L2", 1);
    tree_cell.SetBranchStatus("ph_ClusterSize_7x11_L3", 1);

    # tree_cell.SetBranchStatus("ph_ClusterCells_7x11_L1_E", 1);
    tree_cell.SetBranchStatus("ph_ClusterCells_7x11_L2_E", 1);
    # tree_cell.SetBranchStatus("ph_ClusterCells_7x11_L3_E", 1);

    tree_cell.BuildIndex('EventNumber')
    tree_main.AddFriend(tree_cell)


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


def pass_acceptance_cut(event):
    ph_abseta = abs(getattr(tree_main, 'ph.eta2'))
    ph_pt = getattr(tree_main, 'ph.pt') * 0.001
            
    if ph_abseta > 2.37 or (ph_abseta > 1.37 and ph_abseta < 1.52):
        return False
                
    if ph_pt < 10:
        return False

    return True

def is_healthy_cluster(event):
    n_L1 = event.ph_ClusterSize_7x11_L1
    n_L2 = event.ph_ClusterSize_7x11_L2
    n_L3 = event.ph_ClusterSize_7x11_L3
            
    if n_L1 != 112 or n_L2 != 77 or n_L3 != 44:
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
