#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Calculate colour corrections for various instruments
# 
# Version history:
#
# 16-Jun-2019  M. Peel       Started
# 17-Jun-2019  M. Peel       Tidied up

import healpy as hp
import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from astrocode.fitspectrum.astroutils import *
from astrocode.fitspectrum.spectra import planckcorr, get_spectrum_constants
from fastcc import *

def read_lfi_rimo_bandpass(filename,ext=0):
	inputfits = fits.open(filename)
	# print(len(inputfits))
	print(inputfits[ext].header)

	col_names = inputfits[ext].columns.names
	print(col_names)
	freq = []
	bandpass = []
	error = []
	flag = []
	# print(inputfits[ext].data)
	for i in range(0,len(inputfits[ext].data)):
		# print(inputfits[ext].data[i])
		freq.append(float(inputfits[ext].data[i][0]))
		bandpass.append(float(inputfits[ext].data[i][1]))
		# error.append(inputfits[ext].data[i][2])
		# flag[i].append(inputfits[ext].data[i][3])

	# Renormalise the bandpass per eq20
	const = get_spectrum_constants()
	total = np.sum(bandpass * planckcorr(const, freq) * (freq[1] - freq[0]))
	# print(total)
	bandpass /= total
	# total = np.sum(bandpass * planckcorr(const, freq) * (freq[1] - freq[0]))
	# print(total)
	return np.asarray([freq, bandpass])#, error]

def combine_bandpasses(dataset1,dataset2,dataset3=[],dataset4=[]):
	newdataset = dataset1.copy()
	if dataset3 == []:
		newdataset[1] = (dataset1[1] + dataset2[1])/2.0
	elif dataset4 == []:
		newdataset[1] = (dataset1[1] + dataset2[1] + dataset3[1])/3.0
	else:
		newdataset[1] = (dataset1[1] + dataset2[1] + dataset3[1] + dataset4[1])/4.0
	return newdataset

def plot_bandpass(dataset, outname):
	plt.plot(dataset[0],dataset[1],'b')
	plt.savefig(outname)
	plt.clf()
	plt.close()
	return

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
		return topsum / bottomcalc


def read_quijote_mfi_bandpass(filename):
	freq = []
	bp1 = []
	bp2 = []
	bp3 = []
	bp4 = []
	bp5 = []
	bp6 = []
	bp7 = []
	bp8 = []
	with open(filename) as f:
		for line in f:
			if '(' not in line:
				val = line.strip().split()
				freq.append(float(val[0]))
				bp1.append(float(val[1]))
				bp2.append(float(val[2]))
				bp3.append(float(val[3]))
				bp4.append(float(val[4]))
				bp5.append(float(val[5]))
				bp6.append(float(val[6]))
				bp7.append(float(val[7]))
				bp8.append(float(val[8]))
	return np.asarray([freq, bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8])


outdir = 'plots/'
ensure_dir(outdir)

alphas = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
alphas = np.asarray(alphas)
# QUIJOTE MFI
pol1 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/Pol1_bandpass.dat')
plot_bandpass([pol1[0], pol1[1]],outdir+'mfi_pol1_ch1.png')
plot_bandpass([pol1[0], pol1[2]],outdir+'mfi_pol1_ch2.png')
plot_bandpass([pol1[0], pol1[3]],outdir+'mfi_pol1_ch3.png')
plot_bandpass([pol1[0], pol1[4]],outdir+'mfi_pol1_ch4.png')
plot_bandpass([pol1[0], pol1[5]],outdir+'mfi_pol1_ch5.png')
plot_bandpass([pol1[0], pol1[6]],outdir+'mfi_pol1_ch6.png')
plot_bandpass([pol1[0], pol1[7]],outdir+'mfi_pol1_ch7.png')
plot_bandpass([pol1[0], pol1[8]],outdir+'mfi_pol1_ch8.png')
pol2 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/Pol2_bandpass.dat')
plot_bandpass([pol2[0], pol2[1]],outdir+'mfi_pol2_ch1.png')
plot_bandpass([pol2[0], pol2[2]],outdir+'mfi_pol2_ch2.png')
plot_bandpass([pol2[0], pol2[3]],outdir+'mfi_pol2_ch3.png')
plot_bandpass([pol2[0], pol2[4]],outdir+'mfi_pol2_ch4.png')
plot_bandpass([pol2[0], pol2[5]],outdir+'mfi_pol2_ch5.png')
plot_bandpass([pol2[0], pol2[6]],outdir+'mfi_pol2_ch6.png')
plot_bandpass([pol2[0], pol2[7]],outdir+'mfi_pol2_ch7.png')
plot_bandpass([pol2[0], pol2[8]],outdir+'mfi_pol2_ch8.png')
pol3 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/Pol3_bandpass.dat')
plot_bandpass([pol3[0], pol3[1]],outdir+'mfi_pol3_ch1.png')
plot_bandpass([pol3[0], pol3[2]],outdir+'mfi_pol3_ch2.png')
plot_bandpass([pol3[0], pol3[3]],outdir+'mfi_pol3_ch3.png')
plot_bandpass([pol3[0], pol3[4]],outdir+'mfi_pol3_ch4.png')
plot_bandpass([pol3[0], pol3[5]],outdir+'mfi_pol3_ch5.png')
plot_bandpass([pol3[0], pol3[6]],outdir+'mfi_pol3_ch6.png')
plot_bandpass([pol3[0], pol3[7]],outdir+'mfi_pol3_ch7.png')
plot_bandpass([pol3[0], pol3[8]],outdir+'mfi_pol3_ch8.png')

mfi111 = combine_bandpasses([pol1[0], pol1[2]], [pol1[0], pol1[4]],[pol1[0], pol1[6]],[pol1[0], pol1[8]])
plot_bandpass(mfi111,outdir+'mfi_111.png')
mfi113 = combine_bandpasses([pol1[0], pol1[1]], [pol1[0], pol1[3]],[pol1[0], pol1[5]],[pol1[0], pol1[7]])
plot_bandpass(mfi113,outdir+'mfi_113.png')
mfi217 = combine_bandpasses([pol2[0], pol2[2]], [pol2[0], pol2[4]],[pol2[0], pol2[6]],[pol2[0], pol2[8]])
plot_bandpass(mfi217,outdir+'mfi_217.png')
mfi219 = combine_bandpasses([pol2[0], pol2[1]], [pol2[0], pol2[3]],[pol2[0], pol2[5]],[pol2[0], pol2[7]])
plot_bandpass(mfi219,outdir+'mfi_219.png')
mfi311 = combine_bandpasses([pol3[0], pol3[2]], [pol3[0], pol3[4]],[pol3[0], pol3[6]],[pol3[0], pol3[8]])
plot_bandpass(mfi311,outdir+'mfi_311.png')
mfi313 = combine_bandpasses([pol3[0], pol3[1]], [pol3[0], pol3[3]],[pol3[0], pol3[5]],[pol3[0], pol3[7]])
plot_bandpass(mfi313,outdir+'mfi_313.png')

# For testing a top-hat bandpass
# mfi219[1][:] = 1.0
# mfi219[1][mfi111[0] <= 18.0] = 0
# mfi219[1][mfi111[0] >= 20.0] = 0

mfi111_corrections = np.ones(len(alphas))
mfi113_corrections = np.ones(len(alphas))
mfi217_corrections = np.ones(len(alphas))
mfi219_corrections = np.ones(len(alphas))
mfi311_corrections = np.ones(len(alphas))
mfi313_corrections = np.ones(len(alphas))

calindex = 2.0#-0.3
usecorr = False
for i in range(0,len(alphas)):
	mfi111_corrections[i] = calc_correction(mfi111, 11.0, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi113_corrections[i] = calc_correction(mfi113, 13.0, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi217_corrections[i] = calc_correction(mfi217, 17.0, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi219_corrections[i] = calc_correction(mfi219, 19.0, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi311_corrections[i] = calc_correction(mfi311, 11.0, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi313_corrections[i] = calc_correction(mfi313, 13.0, alphas[i],calindex=calindex,usecorr=usecorr)

print(alphas)
print('From bandpasses:')
print(mfi111_corrections)
print(mfi113_corrections)
print(mfi217_corrections)
print(mfi219_corrections)
print(mfi311_corrections)
print(mfi313_corrections)
print('From fastcc:')
print(fastcc('111',alpha=alphas))
print(fastcc('113',alpha=alphas))
print(fastcc('217',alpha=alphas))
print(fastcc('219',alpha=alphas))
print(fastcc('311',alpha=alphas))
print(fastcc('313',alpha=alphas))

plt.plot(alphas,mfi111_corrections,label='111')
plt.plot(alphas,mfi113_corrections,label='113')
plt.plot(alphas,mfi217_corrections,label='217')
plt.plot(alphas,mfi219_corrections,label='219')
plt.plot(alphas,mfi311_corrections,label='311')
plt.plot(alphas,mfi313_corrections,label='313')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.savefig(outdir+'mfi_corrections.pdf')
plt.clf()
plt.close()

params = np.polyfit(alphas,mfi111_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='111_fit')
params = np.polyfit(alphas,mfi113_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='113_fit')
params = np.polyfit(alphas,mfi217_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='217_fit')
params = np.polyfit(alphas,mfi219_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='219_fit')
params = np.polyfit(alphas,mfi311_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='311_fit')
params = np.polyfit(alphas,mfi313_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='313_fit')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.savefig(outdir+'mfi_corrections_fit.pdf')
plt.clf()
plt.close()

# Below is for Planck LFI

# 2013 release. THE RIMO IS WRONG - it has an incorrect frequency shift in the bandpass.
planck_lfi_filename = '/Users/mpeel/Documents/maps/planck2013/LFI_RIMO_R1.12.fits'
bp_planck_30 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=2)
plot_bandpass(bp_planck_30,outdir+'planck_112_30.png')
bp_planck_44 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=3)
plot_bandpass(bp_planck_44,outdir+'planck_112_44.png')
bp_planck_70 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=4)
plot_bandpass(bp_planck_70,outdir+'planck_112_70.png')

# 2015 release. Mistake in previous version fixed. Extra frequency shift needs to be applied.
planck_lfi_filename = '/Users/mpeel/Documents/maps/planck2015/LFI_RIMO_R2.50.fits'
bp_planck_30 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=25)
plot_bandpass(bp_planck_30,outdir+'planck_250_30.png')
bp_planck_44 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=26)
plot_bandpass(bp_planck_44,outdir+'planck_250_44.png')
bp_planck_70 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=27)
plot_bandpass(bp_planck_70,outdir+'planck_250_70.png')

# 2018 release - actually the same as the 2015 release.
planck_lfi_filename = '/Users/mpeel/Documents/maps/planck2018/LFI_RIMO_R3.31.fits'
bp_planck_30_28S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=3)
plot_bandpass(bp_planck_30_28S,outdir+'planck_30_28S.png')
bp_planck_30_28M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=4)
plot_bandpass(bp_planck_30_28S,outdir+'planck_30_28M.png')
bp_planck_30_27S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=5)
plot_bandpass(bp_planck_30_28S,outdir+'planck_30_27S.png')
bp_planck_30_27M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=6)
plot_bandpass(bp_planck_30_27M,outdir+'planck_30_27M.png')
bp_planck_44_26S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=7)
plot_bandpass(bp_planck_44_26S,outdir+'planck_44_26S.png')
bp_planck_44_26M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=8)
plot_bandpass(bp_planck_44_26M,outdir+'planck_44_26M.png')
bp_planck_44_25S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=9)
plot_bandpass(bp_planck_44_25S,outdir+'planck_44_25S.png')
bp_planck_44_25M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=10)
plot_bandpass(bp_planck_44_25M,outdir+'planck_44_25M.png')
bp_planck_44_24S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=11)
plot_bandpass(bp_planck_44_24S,outdir+'planck_44_24S.png')
bp_planck_44_24M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=12)
plot_bandpass(bp_planck_44_24M,outdir+'planck_44_24M.png')

bp_planck_70_23S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=13)
plot_bandpass(bp_planck_70_23S,outdir+'planck_70_23S.png')
bp_planck_70_23M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=14)
plot_bandpass(bp_planck_70_23M,outdir+'planck_70_23M.png')
bp_planck_70_23 = combine_bandpasses(bp_planck_70_23S, bp_planck_70_23M)
plot_bandpass(bp_planck_70_23,outdir+'planck_70_23.png')

bp_planck_70_22S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=15)
plot_bandpass(bp_planck_70_22S,outdir+'planck_70_22S.png')
bp_planck_70_22M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=16)
plot_bandpass(bp_planck_70_22M,outdir+'planck_70_22M.png')
bp_planck_70_22 = combine_bandpasses(bp_planck_70_22S, bp_planck_70_22M)
plot_bandpass(bp_planck_70_22,outdir+'planck_70_22.png')

bp_planck_70_21S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=17)
plot_bandpass(bp_planck_70_21S,outdir+'planck_70_21S.png')
bp_planck_70_21M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=18)
plot_bandpass(bp_planck_70_21M,outdir+'planck_70_21M.png')
bp_planck_70_21 = combine_bandpasses(bp_planck_70_21S, bp_planck_70_21M)
plot_bandpass(bp_planck_70_21,outdir+'planck_70_18.png')

bp_planck_70_20S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=19)
plot_bandpass(bp_planck_70_20S,outdir+'planck_70_20S.png')
bp_planck_70_20M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=20)
plot_bandpass(bp_planck_70_20M,outdir+'planck_70_20M.png')
bp_planck_70_20 = combine_bandpasses(bp_planck_70_20S, bp_planck_70_20M)
plot_bandpass(bp_planck_70_20,outdir+'planck_70_20.png')

bp_planck_70_19S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=21)
plot_bandpass(bp_planck_70_19S,outdir+'planck_70_19S.png')
bp_planck_70_19M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=22)
plot_bandpass(bp_planck_70_19M,outdir+'planck_70_19M.png')
bp_planck_70_19 = combine_bandpasses(bp_planck_70_19S, bp_planck_70_19M)
plot_bandpass(bp_planck_70_19,outdir+'planck_70_19.png')

bp_planck_70_18S = read_lfi_rimo_bandpass(planck_lfi_filename,ext=23)
plot_bandpass(bp_planck_70_18S,outdir+'planck_70_18S.png')
bp_planck_70_18M = read_lfi_rimo_bandpass(planck_lfi_filename,ext=24)
plot_bandpass(bp_planck_70_18M,outdir+'planck_70_18M.png')
bp_planck_70_18 = combine_bandpasses(bp_planck_70_18S, bp_planck_70_18M)
plot_bandpass(bp_planck_70_18,outdir+'planck_70_18.png')

bp_planck_30 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=25)
plot_bandpass(bp_planck_30,outdir+'planck_30.png')
bp_planck_44 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=26)
plot_bandpass(bp_planck_44,outdir+'planck_44.png')
bp_planck_70 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=27)
plot_bandpass(bp_planck_70,outdir+'planck_70.png')

bp_planck_70_ds1 = combine_bandpasses(bp_planck_70_18, bp_planck_70_23)
bp_planck_70_ds2 = combine_bandpasses(bp_planck_70_19, bp_planck_70_22)
bp_planck_70_ds3 = combine_bandpasses(bp_planck_70_20, bp_planck_70_21)

bp_shift = [0.3, 0.1, -0.4, 1.1, 0.5]
bp_planck_30[0][:] = bp_planck_30[0][:] + bp_shift[0]
bp_planck_44[0][:] = bp_planck_44[0][:] + bp_shift[1]
bp_planck_70_ds1[0][:] = bp_planck_70_ds1[0][:] + bp_shift[2]
bp_planck_70_ds2[0][:] = bp_planck_70_ds2[0][:] + bp_shift[3]
bp_planck_70_ds3[0][:] = bp_planck_70_ds3[0][:] + bp_shift[4]

for i in range(0,len(alphas)):
	print(str(alphas[i]) + " - " + str(calc_correction(bp_planck_70_ds1, 70.4, alphas[i])) + " - " + str(fastcc('70',alphas[i])) + " - " + str(fastcc('70',alphas[i],detector='1823',dev=True)))

for i in range(0,len(alphas)):
	print(str(alphas[i]) + " - " + str(calc_correction(bp_planck_70, 70.4, alphas[i])) + " - " + str(fastcc('70',alphas[i])) + " - " + str(fastcc('70',alphas[i],dev=True)))

for i in range(0,len(alphas)):
	print(str(alphas[i]) + " - " + str(calc_correction(bp_planck_44, 44.1, alphas[i])) + " - " + str(fastcc('44',alphas[i])) + " - " + str(fastcc('44',alphas[i],dev=True)))

for i in range(0,len(alphas)):
	print(str(alphas[i]) + " - " + str(calc_correction(bp_planck_30, 28.4, alphas[i])) + " - " + str(fastcc('30',alphas[i])) + " - " + str(fastcc('30',alphas[i],dev=True)))



