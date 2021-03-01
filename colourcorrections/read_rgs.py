import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from astrocode.fitspectrum.astroutils import *
from fastcc import *
from cc_calc_functions import *

# cc = fits.open('ricardo_cc/c_alpha_dirbe.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_alpha_iras.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_td_beta_dirbe.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['CA'])
# cc.close()

# cc = fits.open('ricardo_cc/c_td_beta_iras.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['CA'])
# cc.close()


# cc = fits.open('ricardo_cc/c_alpha_hfi_bps_pr3.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()
# cc = fits.open('ricardo_cc/c_alpha_hfi_bps_pr2.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_alpha_hfi_pr1.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_td_beta_hfi_bps_pr3.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()
# cc = fits.open('ricardo_cc/c_td_beta_hfi_bps_pr2.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_td_beta_hfi_pr1.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_alpha_wmap_bps.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_alpha_lfi_bps_pr3.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_alpha_mfi_p6.fits')
# print(cc.info())
# print(cc[1].header)
# # print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()
cc = fits.open('ricardo_cc/c_alpha_mfi_p6_pol.fits')
print(cc.info())
print(cc[1].header)
# print(cc[1].data['BANDS'])
print(cc[1].data['PF'])
cc.close()




