Photon Cell RW
==============

* Create data and MC profiles:

`python do_cells_profile.py`

* Compute correction weights

`python calc_rw.py`

* Re-weight MC cells

`python do_cells_profile.py rw.root`
