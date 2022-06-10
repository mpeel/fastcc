# Calculate the effective frequencies for a given spectral index
# MP, 10 June 2022
from fastcc import *
import numpy as np

def calc_freq(nu,cc,alpha):
	return nu * 10**(np.log10(1.0/cc)/alpha)

spectra = -1.0

print('Planck 2013')
cc = fastcc('P30',spectra,option=1)
print("P30: %.2f" % calc_freq(28.4,cc,spectra))
cc = fastcc('P44',spectra,option=1)
print("P44: %.2f" % calc_freq(44.1,cc,spectra))
cc = fastcc('P70',spectra,option=1)
print("P70: %.2f" % calc_freq(70.4,cc,spectra))

print('Planck 2018')
cc = fastcc('P30',spectra)
print("P30: %.2f" % calc_freq(28.4,cc,spectra))
cc = fastcc('P44',spectra)
print("P44: %.2f" % calc_freq(44.1,cc,spectra))
cc = fastcc('P70',spectra)
print("P70: %.2f" % calc_freq(70.4,cc,spectra))

print('WMAP (Bennet et al. 2012)')
cc = fastcc('WK',spectra,option=1)
print("WK: %.2f" % calc_freq(22.8,cc,spectra))
cc = fastcc('WKa',spectra,option=1)
print("WKa: %.2f" % calc_freq(33.0,cc,spectra))
cc = fastcc('WQ',spectra,option=1)
print("WQ: %.2f" % calc_freq(40.7,cc,spectra))
cc = fastcc('WV',spectra,option=1)
print("WV: %.2f" % calc_freq(60.7,cc,spectra))
cc = fastcc('WW',spectra,option=1)
print("WW: %.2f" % calc_freq(93.5,cc,spectra))

print('WMAP (with bandpass shift)')
cc = fastcc('WK',spectra)
print("WK: %.2f" % calc_freq(22.8,cc,spectra))
cc = fastcc('WKa',spectra)
print("WKa: %.2f" % calc_freq(33.0,cc,spectra))
cc = fastcc('WQ',spectra)
print("WQ: %.2f" % calc_freq(40.7,cc,spectra))
cc = fastcc('WV',spectra)
print("WV: %.2f" % calc_freq(60.7,cc,spectra))
cc = fastcc('WW',spectra)
print("WW: %.2f" % calc_freq(93.5,cc,spectra))
