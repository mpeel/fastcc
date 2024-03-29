# Calculate the effective frequencies for a given spectral index
# MP, 17 October 2022
from fastcc import *
import numpy as np

def calc_freq_S(nu,cc,alpha):
	return nu / cc**(1/alpha)

def calc_freq_T(nu,cc,alpha):
	return nu / cc**(1/(alpha-2.0))

np.set_printoptions(precision=2)
spectra = np.asarray([-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0])
print('Flux density units')
print(spectra)
print('Planck 2013')
cc = fastcc('P30',spectra,option=1)
print("P30: ", calc_freq_S(28.4,cc,spectra))
cc = fastcc('P44',spectra,option=1)
print("P44: ", calc_freq_S(44.1,cc,spectra))
cc = fastcc('P70',spectra,option=1)
print("P70: ", calc_freq_S(70.4,cc,spectra))

print('Planck 2018')
cc = fastcc('P30',spectra)
print("P30: ", calc_freq_S(28.4,cc,spectra))
cc = fastcc('P44',spectra)
print("P44: ", calc_freq_S(44.1,cc,spectra))
cc = fastcc('P70',spectra)
print("P70: ", calc_freq_S(70.4,cc,spectra))
cc = fastcc('P100',spectra,option=1)
print("P100: ", calc_freq_S(100.0,cc,spectra))
cc = fastcc('P143',spectra,option=1)
print("P143: ", calc_freq_S(143.0,cc,spectra))
cc = fastcc('P217',spectra,option=1)
print("P217: ", calc_freq_S(217.0,cc,spectra))
cc = fastcc('P353',spectra,option=1)
print("P353: ", calc_freq_S(353.0,cc,spectra))
cc = fastcc('P545',spectra,option=1)
print("P545: ", calc_freq_S(545.0,cc,spectra))
cc = fastcc('P857',spectra,option=1)
print("P857: ", calc_freq_S(857.0,cc,spectra))

print('WMAP (Bennet et al. 2012)')
cc = fastcc('WK',spectra,option=1)
print("WK: ", calc_freq_S(22.8,cc,spectra))
cc = fastcc('WKa',spectra,option=1)
print("WKa: ", calc_freq_S(33.0,cc,spectra))
cc = fastcc('WQ',spectra,option=1)
print("WQ: ", calc_freq_S(40.7,cc,spectra))
cc = fastcc('WV',spectra,option=1)
print("WV: ", calc_freq_S(60.7,cc,spectra))
cc = fastcc('WW',spectra,option=1)
print("WW: ", calc_freq_S(93.5,cc,spectra))

print('WMAP (with bandpass shift)')
cc = fastcc('WK',spectra)
print("WK: ", calc_freq_S(22.8,cc,spectra))
cc = fastcc('WKa',spectra)
print("WKa: ", calc_freq_S(33.0,cc,spectra))
cc = fastcc('WQ',spectra)
print("WQ: ", calc_freq_S(40.7,cc,spectra))
cc = fastcc('WV',spectra)
print("WV: ", calc_freq_S(60.7,cc,spectra))
cc = fastcc('WW',spectra)
print("WW: ", calc_freq_S(93.5,cc,spectra))

print('Temperature units')
print(spectra)
print('Planck 2013')
cc = fastcc('P30',spectra,option=1)
print("P30: ", calc_freq_T(28.4,cc,spectra))
cc = fastcc('P44',spectra,option=1)
print("P44: ", calc_freq_T(44.1,cc,spectra))
cc = fastcc('P70',spectra,option=1)
print("P70: ", calc_freq_T(70.4,cc,spectra))

print('Planck 2018')
cc = fastcc('P30',spectra)
print("P30: ", calc_freq_T(28.4,cc,spectra))
cc = fastcc('P44',spectra)
print("P44: ", calc_freq_T(44.1,cc,spectra))
cc = fastcc('P70',spectra)
print("P70: ", calc_freq_T(70.4,cc,spectra))
cc = fastcc('P100',spectra,option=1)
print("P100: ", calc_freq_T(100.0,cc,spectra))
cc = fastcc('P143',spectra,option=1)
print("P143: ", calc_freq_T(143.0,cc,spectra))
cc = fastcc('P217',spectra,option=1)
print("P217: ", calc_freq_T(217.0,cc,spectra))
cc = fastcc('P353',spectra,option=1)
print("P353: ", calc_freq_T(353.0,cc,spectra))
cc = fastcc('P545',spectra,option=1)
print("P545: ", calc_freq_T(545.0,cc,spectra))
cc = fastcc('P857',spectra,option=1)
print("P857: ", calc_freq_T(857.0,cc,spectra))

print('WMAP (Bennet et al. 2012)')
cc = fastcc('WK',spectra,option=1)
print("WK: ", calc_freq_T(22.8,cc,spectra))
cc = fastcc('WKa',spectra,option=1)
print("WKa: ", calc_freq_T(33.0,cc,spectra))
cc = fastcc('WQ',spectra,option=1)
print("WQ: ", calc_freq_T(40.7,cc,spectra))
cc = fastcc('WV',spectra,option=1)
print("WV: ", calc_freq_T(60.7,cc,spectra))
cc = fastcc('WW',spectra,option=1)
print("WW: ", calc_freq_T(93.5,cc,spectra))

print('WMAP (with bandpass shift)')
cc = fastcc('WK',spectra)
print("WK: ", calc_freq_T(22.8,cc,spectra))
cc = fastcc('WKa',spectra)
print("WKa: ", calc_freq_T(33.0,cc,spectra))
cc = fastcc('WQ',spectra)
print("WQ: ", calc_freq_T(40.7,cc,spectra))
cc = fastcc('WV',spectra)
print("WV: ", calc_freq_T(60.7,cc,spectra))
cc = fastcc('WW',spectra)
print("WW: ", calc_freq_T(93.5,cc,spectra))
