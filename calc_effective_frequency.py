# Calculate the effective frequencies for a given spectral index
# MP, 10 June 2022
from fastcc import *
import numpy as np

def calc_freq(nu,cc,alpha,calindex=-2):
	if alpha + calindex == 0:
		return nu
	else:
		return nu / cc**(1/(alpha+calindex))
	# return nu * 10**(np.log10(1.0/cc)/alpha)

# specs = [-1.0]
specs = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0]
for spectra in specs:
	print('Planck 2013')
	cc = fastcc('P30',spectra,option=1)
	print("P30: %.2f" % calc_freq(28.4,cc,spectra,-2.0))
	cc = fastcc('P44',spectra,option=1)
	print("P44: %.2f" % calc_freq(44.1,cc,spectra,-2.0))
	cc = fastcc('P70',spectra,option=1)
	print("P70: %.2f" % calc_freq(70.4,cc,spectra,-2.0))

	print('Planck 2018')
	print(spectra)
	cc = fastcc('P30',spectra)
	print("P30: %.2f" % calc_freq(28.4,cc,spectra,-2.0))
	cc = fastcc('P44',spectra)
	print("P44: %.2f" % calc_freq(44.1,cc,spectra,-2.0))
	cc = fastcc('P70',spectra)
	print("P70: %.2f" % calc_freq(70.4,cc,spectra,-2.0))
	cc = fastcc('P100',spectra,option=1)
	print("P100: %.2f" % calc_freq(100.0,cc,spectra,1.0))
	cc = fastcc('P143',spectra,option=1)
	print("P143: %.2f" % calc_freq(143.0,cc,spectra,1.0))
	cc = fastcc('P217',spectra,option=1)
	print("P217: %.2f" % calc_freq(217.0,cc,spectra,1.0))
	cc = fastcc('P353',spectra,option=1)
	print("P353: %.2f" % calc_freq(353.0,cc,spectra,1.0))
	cc = fastcc('P545',spectra,option=1)
	print("P545: %.2f" % calc_freq(545.0,cc,spectra,1.0))
	cc = fastcc('P857',spectra,option=1)
	print("P857: %.2f" % calc_freq(857.0,cc,spectra,1.0))

	print('WMAP (Bennet et al. 2012)')
	cc = fastcc('WK',spectra,option=1)
	print("WK: %.2f" % calc_freq(22.8,cc,spectra,-2.0))
	cc = fastcc('WKa',spectra,option=1)
	print("WKa: %.2f" % calc_freq(33.0,cc,spectra,-2.0))
	cc = fastcc('WQ',spectra,option=1)
	print("WQ: %.2f" % calc_freq(40.7,cc,spectra,-2.0))
	cc = fastcc('WV',spectra,option=1)
	print("WV: %.2f" % calc_freq(60.7,cc,spectra,-2.0))
	cc = fastcc('WW',spectra,option=1)
	print("WW: %.2f" % calc_freq(93.5,cc,spectra,-2.0))

	print('WMAP (with bandpass shift)')
	cc = fastcc('WK',spectra)
	print("WK: %.2f" % calc_freq(22.8,cc,spectra,-2.0))
	cc = fastcc('WKa',spectra)
	print("WKa: %.2f" % calc_freq(33.0,cc,spectra,-2.0))
	cc = fastcc('WQ',spectra)
	print("WQ: %.2f" % calc_freq(40.7,cc,spectra,-2.0))
	cc = fastcc('WV',spectra)
	print("WV: %.2f" % calc_freq(60.7,cc,spectra,-2.0))
	cc = fastcc('WW',spectra)
	print("WW: %.2f" % calc_freq(93.5,cc,spectra,-2.0))
