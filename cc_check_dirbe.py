# Do a comparison between the old numbers for DIRBE and Ricardo's new ones
# 10 February 2021 - Mike Peel - Started
import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from astrocode.astroutils import *
from astrocode.spectra import planckcorr, get_spectrum_constants
from fastcc import *

microns = np.asarray([240, 140, 100, 60, 25, 12, 4.9, 3.5, 2.2, 1.25])
print(1e-9*2.997e8/(microns*1e-6))

spectra = np.asarray([-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])

# Old colour corrections
# DIRBE
ccb10 = 0.99049 + 0.00593407 * spectra + 0.0137063 * spectra**2
ccb9 = 0.967133 - 0.0265934 * spectra + 0.0102697 * spectra**2
ccb8 = 1.04217 + 0.0575824 * spectra + 0.0119081 * spectra**2
ccb7 = 1.1 + 0.136703 * spectra + 0.0241758 * spectra**2
ccb6 = 1.22189 + 0.28956 * spectra + 0.042977 * spectra**2
ccb5 = 1.00685 + 0.00615385 * spectra + 0.000679321 * spectra**2
ccb4 = 1.01622 + 0.0435165 * spectra + 0.0230569 * spectra**2
ccb3 = 0.996643 + 0.0 * spectra + 0.0035964 * spectra**2
ccb2 = 0.993217 - 0.00461538 * spectra + 0.00127872 * spectra**2
ccb1 = 0.992797 - 0.00494505 * spectra + 0.0024975 * spectra**2
# IRAS
cci100 = 1.00951 + 0.0223077 * spectra + 0.00893107 * spectra**2
cci60 = 1.04643 + 0.0882418 * spectra + 0.0282717 * spectra**2
cci25 = 1.09448 + 0.124835 * spectra + 0.0202597 * spectra**2
cci12 = 1.09797 + 0.138022 * spectra + 0.0271728 * spectra**2

frequencies = {
'DB10': [1.0056317,   -0.0052173,   -0.0119257],
'DB9':  [1.0347912,    0.0245728,   -0.0095350],
'DB8':  [0.9593942,   -0.0469581,   -0.0075185],
'DB7':  [0.9079217,   -0.0942761,   -0.0068850],
'DB6':  [0.8160551,   -0.1717965,    0.0103011],
'DB5':  [0.9816717,   -0.0327394,   -0.0178211],
'DB4':  [0.9947178,   -0.0060948,   -0.0008378],
'DB3':  [1.0030533,   -0.0001524,   -0.0032236],
'DB2':  [1.0064020,    0.0050962,   -0.0012763],
'DB1':  [1.0073260,    0.0044317,   -0.0028791]
}

plt.title('Old')
plt.plot(spectra,1.0/ccb10,label='10')
plt.plot(spectra,1.0/ccb9,label='9')
plt.plot(spectra,1.0/ccb8,label='8')
plt.plot(spectra,1.0/ccb7,label='7')
plt.plot(spectra,1.0/ccb6,label='6')
plt.plot(spectra,1.0/ccb5,label='5')
plt.plot(spectra,1.0/ccb4,label='4')
plt.plot(spectra,1.0/ccb3,label='3')
plt.plot(spectra,1.0/ccb2,label='2')
plt.plot(spectra,1.0/ccb1,label='1')
plt.ylim([0.3,1.3])
plt.xlim([-3,4])
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.savefig('DIRBE.png')
plt.clf()

# plt.title('New')
cc = frequencies.get('DB10', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='10')
cc = frequencies.get('DB9', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='9')
cc = frequencies.get('DB8', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='8')
cc = frequencies.get('DB7', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='7')
cc = frequencies.get('DB6', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='6')
cc = frequencies.get('DB5', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='5')
cc = frequencies.get('DB4', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='4')
cc = frequencies.get('DB3', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='3')
cc = frequencies.get('DB2', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='2')
cc = frequencies.get('DB1', 0)
plt.plot(spectra,cc[0] + cc[1]*spectra + cc[2]*(spectra**2),label='1')
plt.ylim([0.3,1.3])
plt.xlim([-3,4])
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.xlabel('Spectral index')
plt.ylabel('Colour correction')
plt.savefig('DIRBEnew.png')
plt.clf()

# Values from https://lambda.gsfc.nasa.gov/product/cobe/dirbe_exsup.cfm table B.0-1
spectra2 = np.asarray([-3.0, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3])
b1 = np.asarray([1.03, 1.02, 1.01, 1.01, 1.0, 1.0, 0.99, 0.99, 0.99, 0.99, 0.99, 1.0, 1.0])
b2 = np.asarray([1.02, 1.01, 1.01, 1.0, 1.0, 1.0, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99])
b3 = np.asarray([1.03, 1.02, 1.01, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.01, 1.02, 1.03])
b4 = np.asarray([0.99, 1.0, 1.0, 1.0, 1.0, 1.0, 1.01, 1.01, 1.01, 1.02, 1.02, 1.03, 1.03])
b5 = np.asarray([1.09, 1.05, 1.02, 1.01, 1.0, 1.0, 1.02, 1.04, 1.08, 1.13, 1.19, 1.27, 1.36])
b6 = np.asarray([0.71, 0.76, 0.83, 0.91, 1.0, 1.1, 1.23, 1.37, 1.53, 1.72, 1.95, 2.21, 2.52])
b7 = np.asarray([0.89, 0.91, 0.93, 0.96, 1.0, 1.05, 1.1, 1.17, 1.25, 1.34, 1.46, 1.59, 1.75])
b8 = np.asarray([0.97, 0.97, 0.98, 0.99, 1.00, 1.02, 1.04, 1.07, 1.11, 1.15, 1.2, 1.26, 1.33])
b9 = np.asarray([1.14, 1.10, 1.06, 1.03, 1.0, 0.98, 0.97, 0.96, 0.95, 0.95, 0.96, 0.96, 0.98])
b10 = np.asarray([1.1, 1.06, 1.03, 1.01, 1.0, 0.99, 0.99, 1.0, 1.01, 1.03, 1.06, 1.09, 1.13])
plt.title('Supplement values')
plt.plot(spectra2,1/b10,label='10')
plt.plot(spectra2,1/b9,label='9')
plt.plot(spectra2,1/b8,label='8')
plt.plot(spectra2,1/b7,label='7')
plt.plot(spectra2,1/b6,label='6')
plt.plot(spectra2,1/b5,label='5')
plt.plot(spectra2,1/b4,label='4')
plt.plot(spectra2,1/b3,label='3')
plt.plot(spectra2,1/b2,label='2')
plt.plot(spectra2,1/b1,label='1')
plt.ylim([0.3,1.3])
plt.xlim([-3,4])
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.xlabel('Spectral index')
plt.ylabel('Colour correction')
plt.savefig('DIRBEpub.png')
plt.clf()

plt.title('Old')
plt.plot(spectra,1.0/cci100,label='I100')
plt.plot(spectra,1.0/cci60,label='I60')
plt.plot(spectra,1.0/cci25,label='I25')
plt.plot(spectra,1.0/cci12,label='I12')
plt.ylim([0.3,1.3])
plt.xlim([-3,4])
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.savefig('IRASold.png')
plt.clf()

# From https://irsa.ipac.caltech.edu/IRASdocs/archives/colorcorr.html
spectra3 = np.asarray([-3.0, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3])
i100 = np.asarray([1.02, 1.01, 1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.04, 1.06, 1.09, 1.12, 1.16])
i60 = np.asarray([1.02, 1.0, 0.99, 0.99, 1.0, 1.02, 1.05, 1.09, 1.15, 1.23, 1.32, 1.44, 1.59])
i25 = np.asarray([0.89, 0.91, 0.93, 0.96, 1.0, 1.04, 1.1, 1.16, 1.23, 1.32, 1.41, 1.53, 1.67])
i12 = np.asarray([0.91, 0.92, 0.94, 0.97, 1.0, 1.04, 1.1, 1.17, 1.25, 1.35, 1.47, 1.61, 1.78])

plt.title('Supplement values')
plt.plot(spectra3,1/i100,label='100um')
plt.plot(spectra3,1/i60,label='60um')
plt.plot(spectra3,1/i25,label='25um')
plt.plot(spectra3,1/i12,label='12um')
plt.ylim([0.3,1.3])
plt.xlim([-3,4])
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.xlabel('Spectral index')
plt.ylabel('Colour correction')
plt.savefig('IRASpub.png')
plt.clf()

# plt.title('New')
params = np.polyfit(spectra3,1.0/i100,2)
print("'I100': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 2997],')
plt.plot(spectra,params[2]+params[1]*spectra+params[0]*spectra**2,label='I100')

params = np.polyfit(spectra3,1.0/i60,2)
print("'I60': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 4995],')
plt.plot(spectra,params[2]+params[1]*spectra+params[0]*spectra**2,label='I60')

params = np.polyfit(spectra3,1.0/i25,2)
print("'I25': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 11988],')
plt.plot(spectra,params[2]+params[1]*spectra+params[0]*spectra**2,label='I25')

params = np.polyfit(spectra3,1.0/i12,2)
print("'I12': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 24975],')
plt.plot(spectra,params[2]+params[1]*spectra+params[0]*spectra**2,label='I12')
plt.ylim([0.3,1.3])
plt.xlim([-3,4])
plt.xlabel('Spectral index')
plt.ylabel('Colour correction')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.savefig('IRASnew.png')
plt.clf()
