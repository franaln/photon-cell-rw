Photon Cell RW
==============

1. Create data and MC profiles:

python do_cells_profile.py

2. Compute correction weights

python calc_rw.py

3. Reweight MC cells

python do_cells_profile.py rw.root