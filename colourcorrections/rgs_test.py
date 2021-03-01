from fastcc import *
from fastcc_old import *

import numpy as np
import matplotlib.pyplot as plt

spectra = np.asarray([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])

to_test = ['Q217', 'Q219', 'Q311', 'Q313', 'Q417','Q419','Q217p', 'Q219p', 'Q311p', 'Q313p', 'Q417p','Q419p']
for band in to_test:
	old = fastcc(band, spectra,option=3)
	new1 = fastcc_old(band, spectra,option=3)
	new2 = fastcc_old(band+'a', spectra,option=3)
	new = 2./(1/new1+1/new2)
	print(band + ": " + "{:2.2f}".format(np.max(old-new)*100.0)+"%")
exit()

to_test = ['WK', 'WKa', 'WQ', 'WV', 'WW','P30','P44','P70']
for band in to_test:
	old = fastcc(band, spectra,option=3)
	new = fastcc_old(band, spectra,option=3)
	print(band + ": " + "{:2.2f}".format(np.max(old-new)*100.0)+"%")
exit()
to_test = ['P100', 'P143', 'P217', 'P353', 'P545', 'P857']
for band in to_test:
	old = fastcc(band, spectra,option=1)
	new = fastcc_old(band, spectra,option=1)
	print(band + ": " + "{:2.2f}".format(np.max(old-new)*100.0)+"%")
	old = fastcc(band, spectra,option=2)
	new = fastcc_old(band, spectra,option=2)
	print(band + ": " + "{:2.2f}".format(np.max(old-new)*100.0)+"%")
	old = fastcc(band, spectra,option=3)
	new = fastcc_old(band, spectra,option=3)
	print(band + ": " + "{:2.2f}".format(np.max(old-new)*100.0)+"%")
exit()

to_test = ['DB10','DB9','DB8','DB7','DB6','DB5','DB4','DB3','DB2','DB1','I100','I60','I25','I12']
for band in to_test:
	old = fastcc(band, spectra,option=2)
	new = fastcc(band, spectra,option=3)
	print(band + ": " + "{:2.2f}".format(np.max(old-new)*100.0)+"%")

plt.plot(spectra, fastcc('I100', spectra,option=2),'.',label='100-old')
plt.plot(spectra, fastcc('I100', spectra,option=3),label='100-new')
plt.plot(spectra, fastcc('I60', spectra,option=2),'.',label='60-old')
plt.plot(spectra, fastcc('I60', spectra,option=3),label='60-new')
plt.plot(spectra, fastcc('I25', spectra,option=2),'.',label='25-old')
plt.plot(spectra, fastcc('I25', spectra,option=3),label='25-new')
plt.plot(spectra, fastcc('I12', spectra,option=2),'.',label='12-old')
plt.plot(spectra, fastcc('I12', spectra,option=3),label='12-new')
plt.legend()
plt.savefig('iras_comparison.png')