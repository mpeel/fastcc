#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Calculate colour corrections for various instruments
# 
# Version history:
#
# 16-Jun-2019  M. Peel       Started
# 17-Jun-2019  M. Peel       Tidied up

import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from astrocode.fitspectrum.astroutils import *
from fastcc import *
from cc_calc_functions import *

outdir = 'plots_2021_01_15/'
print(outdir)
ensure_dir(outdir)

alphas = [-6.0, -5.5, -5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
alphas = np.asarray(alphas)

# Below is for Planck HFI

# # 2013 release.
option = 1
year = 2013
planck_hfi_filename = 'inputdata/HFI_RIMO_R1.10.fits'
bp_planck_100 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=2,nu0=100.0)
plot_bandpass(bp_planck_100,outdir+'planck_2013_100.png')
bp_planck_143 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=3,nu0=143.0)
plot_bandpass(bp_planck_143,outdir+'planck_2013_143.png')
bp_planck_217 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=4,nu0=217.0)
plot_bandpass(bp_planck_217,outdir+'planck_2013_217.png')
bp_planck_353 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=5,nu0=353.0)
plot_bandpass(bp_planck_353,outdir+'planck_2013_353.png')
bp_planck_545 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=6,nu0=545.0)
plot_bandpass(bp_planck_545,outdir+'planck_2013_545.png')
bp_planck_857 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=7,nu0=857.0)
plot_bandpass(bp_planck_857,outdir+'planck_2013_857.png')

# print(1.0/calc_unit_hfi(bp_planck_100, 100.0))
# print(1.0/calc_unit_hfi(bp_planck_143, 143.0))

# 2015 release.
# option = 2
# year = 2015
# planck_hfi_filename = 'inputdata/HFI_RIMO_R2.00.fits'
# bp_planck_100 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=55,nu0=100.0)
# plot_bandpass(bp_planck_100,outdir+'planck_2015_100.png')
# bp_planck_143 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=56,nu0=143.0)
# plot_bandpass(bp_planck_143,outdir+'planck_2015_143.png')
# bp_planck_217 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=57,nu0=217.0)
# plot_bandpass(bp_planck_217,outdir+'planck_2015_217.png')
# bp_planck_353 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=58,nu0=353.0)
# plot_bandpass(bp_planck_353,outdir+'planck_2015_353.png')
# bp_planck_545 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=59,nu0=545.0)
# plot_bandpass(bp_planck_545,outdir+'planck_2015_545.png')
# bp_planck_857 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=60,nu0=857.0)
# plot_bandpass(bp_planck_857,outdir+'planck_2015_857.png')

# 2018 release
# option = 3
# year = 2018
# planck_hfi_filename = 'inputdata/HFI_RIMO_R3.00.fits'
# bp_planck_100 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=3,nu0=100.0)
# plot_bandpass(bp_planck_100,outdir+'planck_100.png')
# bp_planck_143 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=4,nu0=143.0)
# plot_bandpass(bp_planck_143,outdir+'planck_143.png')
# bp_planck_217 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=5,nu0=217.0)
# plot_bandpass(bp_planck_217,outdir+'planck_217.png')
# bp_planck_353 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=6,nu0=353.0)
# plot_bandpass(bp_planck_353,outdir+'planck_353.png')
# bp_planck_545 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=7,nu0=545.0)
# plot_bandpass(bp_planck_545,outdir+'planck_545.png')
# bp_planck_857 = read_hfi_rimo_bandpass(planck_hfi_filename,ext=8,nu0=857.0)
# plot_bandpass(bp_planck_857,outdir+'planck_857.png')
# bp_planck_353psb = read_hfi_rimo_bandpass(planck_hfi_filename,ext=9,nu0=353.0)
# plot_bandpass(bp_planck_353psb,outdir+'planck_353psb.png')

print(calc_unit_hfi(bp_planck_100, 100.0))
print(calc_unit_hfi(bp_planck_143, 143.0))
print(calc_unit_hfi(bp_planck_217, 217.0))
print(calc_unit_hfi(bp_planck_353, 353.0))
print(calc_unit_hfi(bp_planck_545, 545.0))
print(calc_unit_hfi(bp_planck_857, 857.0))
# exit()

# bp_planck_70_ds1 = combine_bandpasses(bp_planck_70_18, bp_planck_70_23)
# bp_planck_70_ds2 = combine_bandpasses(bp_planck_70_19, bp_planck_70_22)
# bp_planck_70_ds3 = combine_bandpasses(bp_planck_70_20, bp_planck_70_21)

# bp_shift = [0.3, 0.1, -0.4, 1.1, 0.5]
# bp_planck_30[0][:] = bp_planck_30[0][:] + bp_shift[0]
# bp_planck_44[0][:] = bp_planck_44[0][:] + bp_shift[1]
# bp_planck_70_ds1[0][:] = bp_planck_70_ds1[0][:] + bp_shift[2]
# bp_planck_70_ds2[0][:] = bp_planck_70_ds2[0][:] + bp_shift[3]
# bp_planck_70_ds3[0][:] = bp_planck_70_ds3[0][:] + bp_shift[4]

# for i in range(0,len(alphas)):
# 	print(str(alphas[i]) + " - " + str(calc_correction(bp_planck_70_ds1, 70.4, alphas[i])) + " - " + str(fastcc('70',alphas[i])) + " - " + str(fastcc('70',alphas[i],detector='1823',latest=True)))

calindex = -1.0 # Because this is what HFI uses for unit conversion rather than something sensible like +2.0...
usecorr = False
hfi100_corrections = np.ones(len(alphas))
hfi143_corrections = np.ones(len(alphas))
hfi217_corrections = np.ones(len(alphas))
hfi353_corrections = np.ones(len(alphas))
hfi545_corrections = np.ones(len(alphas))
hfi857_corrections = np.ones(len(alphas))
hfi100_corrections_fcc = np.ones(len(alphas))
hfi143_corrections_fcc = np.ones(len(alphas))
hfi217_corrections_fcc = np.ones(len(alphas))
hfi353_corrections_fcc = np.ones(len(alphas))
hfi545_corrections_fcc = np.ones(len(alphas))
hfi857_corrections_fcc = np.ones(len(alphas))
for i in range(0,len(alphas)):
	hfi100_corrections[i] = calc_correction_hfi(bp_planck_100, 100.0, alphas[i],calindex=calindex,usecorr=usecorr)
	hfi100_corrections_fcc[i] = fastcc('P100',alpha=alphas[i],option=option)
	hfi143_corrections[i] = calc_correction_hfi(bp_planck_143, 143.0, alphas[i],calindex=calindex,usecorr=usecorr)
	hfi143_corrections_fcc[i] = fastcc('P143',alpha=alphas[i],option=option)
	hfi217_corrections[i] = calc_correction_hfi(bp_planck_217, 217.0, alphas[i],calindex=calindex,usecorr=usecorr)
	hfi217_corrections_fcc[i] = fastcc('P217',alpha=alphas[i],option=option)
	hfi353_corrections[i] = calc_correction_hfi(bp_planck_353, 353.0, alphas[i],calindex=calindex,usecorr=usecorr)
	hfi353_corrections_fcc[i] = fastcc('P353',alpha=alphas[i],option=option)
	hfi545_corrections[i] = calc_correction_hfi(bp_planck_545, 545.0, alphas[i],calindex=calindex,usecorr=usecorr)
	hfi545_corrections_fcc[i] = fastcc('P545',alpha=alphas[i],option=option)
	hfi857_corrections[i] = calc_correction_hfi(bp_planck_857, 857.0, alphas[i],calindex=calindex,usecorr=usecorr)
	hfi857_corrections_fcc[i] = fastcc('P857',alpha=alphas[i],option=option)
# print(hfi100_corrections)

# print('100GHz')
params = np.polyfit(alphas,hfi100_corrections,2)
print("'P100': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 100.0],')
plt.plot(alphas,hfi100_corrections,'b+')
plt.plot(alphas,hfi100_corrections_fcc,'b.-')
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'b-',label='P100_fit')
# print('143GHz')
params = np.polyfit(alphas,hfi143_corrections,2)
print("'P143': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 143.0],')
plt.plot(alphas,hfi143_corrections,'r+')
plt.plot(alphas,hfi143_corrections_fcc,'r.-')
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'r-',label='P143_fit')
# print('217GHz')
params = np.polyfit(alphas,hfi217_corrections,2)
print("'P217': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 217.0],')
plt.plot(alphas,hfi217_corrections,'g+')
plt.plot(alphas,hfi217_corrections_fcc,'g.-')
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'g-',label='P217_fit')
# print('353GHz')
params = np.polyfit(alphas,hfi353_corrections,2)
print("'P353': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 353.0],')
plt.plot(alphas,hfi353_corrections,'c+')
plt.plot(alphas,hfi353_corrections_fcc,'c.-')
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'c-',label='P353_fit')
# print('545GHz')
params = np.polyfit(alphas,hfi545_corrections,2)
print("'P545': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 545.0],')
plt.plot(alphas,hfi545_corrections,'m+')
plt.plot(alphas,hfi545_corrections_fcc,'m.-')
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'m-',label='P545_fit')
# print('857GHz')
params = np.polyfit(alphas,hfi857_corrections,2)
print("'P857': ["+str(params[2]) + ', ' + str(params[1]) + ', ' + str(params[0]) + ', 857.0],')
plt.plot(alphas,hfi857_corrections,'y+')
plt.plot(alphas,hfi857_corrections_fcc,'y.-')
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'y-',label='P857_fit')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.xlabel('Spectral index')
plt.ylabel('Colour correction')
plt.savefig(outdir+'planck'+str(year)+'_fit.pdf')
plt.clf()
plt.close()
