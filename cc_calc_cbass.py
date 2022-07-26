#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Calculate colour corrections for C-BASS
#
# Version history:
#
# 16-Jun-2019  M. Peel       Started
# 17-Jun-2019  M. Peel       Tidied up
# 13-Jan-2021  M. Peel       Split from cc_calc.py

import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from astrocode.astroutils import *
from fastcc import *
from cc_calc_functions import *

outdir = 'plots_2021_01_15/'
print(outdir)
ensure_dir(outdir)

alphas = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
alphas = np.asarray(alphas)

# CBASS
cbass_bp = read_cbass_bandpass('/Users/mpeel/Documents/maps/cbass2019/20130625_v02_Passband.csv')
print(cbass_bp[0])
plot_bandpass([cbass_bp[0],cbass_bp[1]],outdir+'cbass_I1.png')
plot_bandpass([cbass_bp[0],cbass_bp[2]],outdir+'cbass_Q1.png')
plot_bandpass([cbass_bp[0],cbass_bp[3]],outdir+'cbass_U1.png')
plot_bandpass([cbass_bp[0],cbass_bp[4]],outdir+'cbass_Q2.png')
plot_bandpass([cbass_bp[0],cbass_bp[5]],outdir+'cbass_U2.png')
plot_bandpass([cbass_bp[0],cbass_bp[6]],outdir+'cbass_I2.png')
cbassI = combine_bandpasses([cbass_bp[0],cbass_bp[1]], [cbass_bp[0],cbass_bp[6]])
cbassQ = combine_bandpasses([cbass_bp[0],cbass_bp[2]], [cbass_bp[0],cbass_bp[4]])
cbassU = combine_bandpasses([cbass_bp[0],cbass_bp[3]], [cbass_bp[0],cbass_bp[5]])
cbassP = combine_bandpasses(cbassQ, cbassU)

plot_bandpass_all([[cbass_bp[0],cbass_bp[1]],[cbass_bp[0],cbass_bp[2]],[cbass_bp[0],cbass_bp[3]],[cbass_bp[0],cbass_bp[4]],[cbass_bp[0],cbass_bp[5]],[cbass_bp[0],cbass_bp[6]]],outdir+'cbass_all.png')


cbassI1_corrections = np.ones(len(alphas))
cbassU1_corrections = np.ones(len(alphas))
cbassQ1_corrections = np.ones(len(alphas))
cbassU2_corrections = np.ones(len(alphas))
cbassQ2_corrections = np.ones(len(alphas))
cbassI2_corrections = np.ones(len(alphas))
cbassI_corrections = np.ones(len(alphas))
cbassU_corrections = np.ones(len(alphas))
cbassQ_corrections = np.ones(len(alphas))
cbassP_corrections = np.ones(len(alphas))

calindex = -0.299
calfreq = 4.76
usecorr = False
for i in range(0,len(alphas)):
	cbassI1_corrections[i] = calc_correction([cbass_bp[0],cbass_bp[1]], calfreq, alphas[i],calindex=calindex,usecorr=usecorr)
	cbassQ1_corrections[i] = calc_correction([cbass_bp[0],cbass_bp[2]], calfreq, alphas[i],calindex=calindex,usecorr=usecorr)
	cbassU1_corrections[i] = calc_correction([cbass_bp[0],cbass_bp[3]], calfreq, alphas[i],calindex=calindex,usecorr=usecorr)
	cbassQ2_corrections[i] = calc_correction([cbass_bp[0],cbass_bp[4]], calfreq, alphas[i],calindex=calindex,usecorr=usecorr)
	cbassU2_corrections[i] = calc_correction([cbass_bp[0],cbass_bp[5]], calfreq, alphas[i],calindex=calindex,usecorr=usecorr)
	cbassI2_corrections[i] = calc_correction([cbass_bp[0],cbass_bp[6]], calfreq, alphas[i],calindex=calindex,usecorr=usecorr)
	cbassI_corrections[i] = calc_correction(cbassI, calfreq, alphas[i],calindex=calindex,usecorr=usecorr)
	cbassQ_corrections[i] = calc_correction(cbassQ, calfreq, alphas[i],calindex=calindex,usecorr=usecorr)
	cbassU_corrections[i] = calc_correction(cbassU, calfreq, alphas[i],calindex=calindex,usecorr=usecorr)
	cbassP_corrections[i] = calc_correction(cbassP, calfreq, alphas[i],calindex=calindex,usecorr=usecorr)

print(alphas)
print('From bandpasses:')
print(cbassI1_corrections)
print(cbassQ1_corrections)
print(cbassU1_corrections)
print(cbassQ2_corrections)
print(cbassU2_corrections)
print(cbassI2_corrections)
print(cbassI_corrections)
print(cbassQ_corrections)
print(cbassU_corrections)
print(cbassP_corrections)
print("Comparison to Luke's numbers for alpha=-1:")
print(cbassI1_corrections[4], calc_Kcol(alphas[4], calindex, cbass_bp[1], calfreq, cbass_bp[0]))
print(cbassQ1_corrections[4], calc_Kcol(alphas[4], calindex, cbass_bp[2], calfreq, cbass_bp[0]))
print(cbassU1_corrections[4], calc_Kcol(alphas[4], calindex, cbass_bp[3], calfreq, cbass_bp[0]))
print(cbassQ2_corrections[4], calc_Kcol(alphas[4], calindex, cbass_bp[4], calfreq, cbass_bp[0]))
print(cbassU2_corrections[4], calc_Kcol(alphas[4], calindex, cbass_bp[5], calfreq, cbass_bp[0]))
print(cbassI2_corrections[4], calc_Kcol(alphas[4], calindex, cbass_bp[6], calfreq, cbass_bp[0]))

# plt.plot(alphas,cbassI1_corrections,label='I1')
# plt.plot(alphas,cbassQ1_corrections,label='Q1')
# plt.plot(alphas,cbassU1_corrections,label='U1')
# plt.plot(alphas,cbassQ2_corrections,label='Q2')
# plt.plot(alphas,cbassU2_corrections,label='U2')
# plt.plot(alphas,cbassI2_corrections,label='I2')
plt.plot(alphas,cbassI_corrections,label='I')
plt.plot(alphas,cbassQ_corrections,label='Q')
plt.plot(alphas,cbassU_corrections,label='U')
plt.plot(alphas,cbassP_corrections,label='P')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.tight_layout()
plt.savefig(outdir+'cbass_corrections.png')
plt.clf()
plt.close()

params = np.polyfit(alphas,cbassI1_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='I1_fit')
params = np.polyfit(alphas,cbassQ1_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='Q1_fit')
params = np.polyfit(alphas,cbassU1_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='U1_fit')
params = np.polyfit(alphas,cbassQ2_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='Q2_fit')
params = np.polyfit(alphas,cbassU2_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='U2_fit')
params = np.polyfit(alphas,cbassI2_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='I2_fit')
params = np.polyfit(alphas,cbassI_corrections,2)
print(params)
print("'CBASSNI': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 4.76],')
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='I_fit')
params = np.polyfit(alphas,cbassQ_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='Q_fit')
params = np.polyfit(alphas,cbassU_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='U_fit')
params = np.polyfit(alphas,cbassP_corrections,2)
print(params)
print("'CBASSNP': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 4.76],')
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='P_fit')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.savefig(outdir+'cbass_corrections_fit.pdf')
plt.clf()
plt.close()
