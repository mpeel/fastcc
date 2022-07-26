import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from astrocode.astroutils import *
from astrocode.spectra import planckcorr, get_spectrum_constants
from fastcc import *
from cc_calc import *

def calc_correction(dataset,nu0,alpha,calindex=2.0,usecorr=True):
	const = get_spectrum_constants()
	# Following eq.17 from Planck 2013 V.
	dnu = dataset[0][1] - dataset[0][0]
	if usecorr:
		topsum = np.sum(dataset[1] / planckcorr(const, dataset[0])) * dnu
		bottomcalc = np.sum(np.asarray(dataset[1]) * (np.asarray(dataset[0]) / nu0)**(alpha-calindex)) * dnu
		return topsum / ((1.0/planckcorr(const, nu0)) * bottomcalc)
	else:
		topsum = np.sum(dataset[1]) * dnu
		bottomcalc = np.sum(np.asarray(dataset[1]) * (np.asarray(dataset[0]) / nu0)**(alpha-calindex)) * dnu
		print(topsum)
		print(bottomcalc)
		return topsum / bottomcalc

alphas = np.asarray([-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])

pol3_orig = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/Pol3_bandpass.dat')
mfi311orig = combine_bandpasses([pol3_orig[0], pol3_orig[2]], [pol3_orig[0], pol3_orig[4]],[pol3_orig[0], pol3_orig[6]],[pol3_orig[0], pol3_orig[8]])
mfi311orig_corrections = np.ones(len(alphas))
calindex = 2.0#-0.3
usecorr = False

# for i in range(0,len(alphas)):
# 	mfi311orig_corrections[i] = calc_correction(mfi311orig, 11.1, alphas[i],calindex=calindex,usecorr=usecorr)

# print(mfi311orig_corrections)

print(calc_correction(mfi311orig, 11.155, -0.7,calindex=calindex,usecorr=usecorr))
