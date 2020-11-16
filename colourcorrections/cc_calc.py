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
from fastcc import *

def get_spectrum_constants():
	const = {
		'h': 6.626e-34,
		'k': 1.381e-23,
		'c': 2.997e8,
		'pi': np.pi,
		'dust_optical_depth_freq': 1198.8,
		'tcmb': 2.7255
	}
	return const

def planckcorr(const, nu_ghz):
	x = const['h'] * np.asarray(nu_ghz) * 1.0e9 / (const['k'] * const['tcmb'])
	value = (np.exp(x)-1.0)**2.0 / (x**2. * np.exp(x))
	return value


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

def plot_bandpass_all(dataset,outname):
	for i in range(0,len(dataset)):
		plt.plot(dataset[i][0],dataset[i][1])#,'b')
	# plt.yscale('log')
	plt.xlabel('Frequency')
	plt.ylabel('Amplitude')
	plt.savefig(outname)
	plt.clf()
	plt.close()
	return


def plot_bandpass(dataset, outname):
	plt.plot(dataset[0],dataset[1],'b')
	# plt.yscale('log')
	plt.xlabel('Frequency')
	plt.ylabel('Amplitude')
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


# def read_quijote_mfi_bandpass(filename):
# 	freq = []
# 	bp1 = []
# 	bp2 = []
# 	bp3 = []
# 	bp4 = []
# 	bp5 = []
# 	bp6 = []
# 	bp7 = []
# 	bp8 = []
# 	with open(filename) as f:
# 		for line in f:
# 			if '(' not in line:
# 				val = line.strip().split()
# 				freq.append(float(val[0]))
# 				bp1.append(float(val[1]))
# 				bp2.append(float(val[2]))
# 				bp3.append(float(val[3]))
# 				bp4.append(float(val[4]))
# 				bp5.append(float(val[5]))
# 				bp6.append(float(val[6]))
# 				bp7.append(float(val[7]))
# 				bp8.append(float(val[8]))
# 	bp1 = bp1 / np.sum(bp1)
# 	bp2 = bp2 / np.sum(bp2)
# 	bp3 = bp3 / np.sum(bp3)
# 	bp4 = bp4 / np.sum(bp4)
# 	bp5 = bp5 / np.sum(bp5)
# 	bp6 = bp6 / np.sum(bp6)
# 	bp7 = bp7 / np.sum(bp7)
# 	bp8 = bp8 / np.sum(bp8)
# 	return np.asarray([freq, bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8])

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
	minval = 0
	minval = -1000
	with open(filename) as f:
		for line in f:
			if '(' not in line and '*' not in line:
				val = line.strip().split()
				freq.append(float(val[0]))
				if float(val[1]) > minval:
					bp1.append(float(val[1]))
				else:
					bp1.append(0.0)
				if float(val[2]) > minval:
					bp2.append(float(val[2]))
				else:
					bp2.append(0.0)
				if float(val[3]) > minval:
					bp3.append(float(val[3]))
				else:
					bp3.append(0.0)
				if float(val[4]) > minval:
					bp4.append(float(val[4]))
				else:
					bp4.append(0.0)
				if float(val[5]) > minval:
					bp5.append(float(val[5]))
				else:
					bp5.append(0.0)
				if float(val[6]) > minval:
					bp6.append(float(val[6]))
				else:
					bp6.append(0.0)
				if float(val[7]) > minval:
					bp7.append(float(val[7]))
				else:
					bp7.append(0.0)
				if float(val[8]) > minval:
					bp8.append(float(val[8]))
				else:
					bp8.append(0.0)
	# bp1 = bp1 / np.sum(bp1)
	# bp2 = bp2 / np.sum(bp2)
	# bp3 = bp3 / np.sum(bp3)
	# bp4 = bp4 / np.sum(bp4)
	# bp5 = bp5 / np.sum(bp5)
	# bp6 = bp6 / np.sum(bp6)
	# bp7 = bp7 / np.sum(bp7)
	# bp8 = bp8 / np.sum(bp8)
	return np.asarray([freq, bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8])

def read_cbass_bandpass(filename):
	freq = []
	bp1 = []
	bp2 = []
	bp3 = []
	bp4 = []
	bp5 = []
	bp6 = []
	bp = np.loadtxt(filename,skiprows=1,delimiter=',')#np.loadtxt(bpFileName)
	for val in bp:
		# val = line.strip().replace(',','').split()
		print(val)
		freq.append(float(val[0]))
		bp1.append(float(val[1]))
		bp2.append(float(val[2]))
		bp3.append(float(val[3]))
		bp4.append(float(val[4]))
		bp5.append(float(val[5]))
		bp6.append(float(val[6]))
	bp1 = bp1 / np.sum(bp1)
	bp2 = bp2 / np.sum(bp2)
	bp3 = bp3 / np.sum(bp3)
	bp4 = bp4 / np.sum(bp4)
	bp5 = bp5 / np.sum(bp5)
	bp6 = bp6 / np.sum(bp6)
	return np.asarray(np.abs([freq, bp1, bp2, bp3, bp4, bp5, bp6]))

# From Luke's code - eq11 of https://arxiv.org/abs/1306.1778
def calc_Kcol(alpha_src,alpha_cal,g,nu0,nu):
    numer = np.trapz(g*np.power(nu/nu0,alpha_cal),nu)
    denom = np.trapz(g*np.power(nu/nu0,alpha_src),nu)
    return numer/denom

# def cc_calc():
# outdir = 'plots_2020_05_22_comb/'
# outdir = 'mfi_orig/'
# outdir = 'mfi_2020_05_21/'
outdir = 'plots_2020_10_06/'
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
plt.savefig(outdir+'cbass_corrections.pdf')
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
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='I_fit')
params = np.polyfit(alphas,cbassQ_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='Q_fit')
params = np.polyfit(alphas,cbassU_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='U_fit')
params = np.polyfit(alphas,cbassP_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='P_fit')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.savefig(outdir+'cbass_corrections_fit.pdf')
plt.clf()
plt.close()
# exit()

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
# pol2 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/Pol2_bandpass.dat')
# pol2 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020_05_21_Pol2_bandpass.dat')
pol2 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020-10_Horn2_bandpass_intensity.dat')
pol2_pol = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020-10_Horn2_bandpass_polarization.dat')
# pol2 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020_05_22_0deg_Pol2_bandpass.dat')
# pol2 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020_05_22_22p5deg_Pol2_bandpass.dat')
# minlength = np.min([len(pol2a[0]),len(pol2b[0])])
# pol2a = pol2a[:,:minlength]
# pol2b = pol2b[:,:minlength]
# pol2a[pol2a < 0.0] = 0.0
# pol2b[pol2b < 0.0] = 0.0
# pol2 = np.sqrt(pol2a**2+pol2b**2)
# for i in range(0,len(pol2)):
# 	pol2[i] = pol2[i] / np.sum(pol2[i])
# pol2[~np.isfinite(pol2)] = 0.0
plot_bandpass([pol2[0], pol2[1]],outdir+'mfi_pol2_ch1.png')
plot_bandpass([pol2[0], pol2[2]],outdir+'mfi_pol2_ch2.png')
plot_bandpass([pol2[0], pol2[3]],outdir+'mfi_pol2_ch3.png')
plot_bandpass([pol2[0], pol2[4]],outdir+'mfi_pol2_ch4.png')
plot_bandpass([pol2[0], pol2[5]],outdir+'mfi_pol2_ch5.png')
plot_bandpass([pol2[0], pol2[6]],outdir+'mfi_pol2_ch6.png')
plot_bandpass([pol2[0], pol2[7]],outdir+'mfi_pol2_ch7.png')
plot_bandpass([pol2[0], pol2[8]],outdir+'mfi_pol2_ch8.png')
# pol3_orig = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/Pol3_bandpass.dat')
# pol3 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/Horn3_bandpass_intensity.dat')
# pol3_pol = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/Horn3_bandpass_polarization.dat')
pol3 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020-10_Horn3_bandpass_intensity.dat')
pol3_pol = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020-10_Horn3_bandpass_polarization.dat')
# pol3 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020_05_22_0deg_Pol3_bandpass.dat')
# pol3 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020_05_22_22p5deg_Pol3_bandpass.dat')
# minlength = np.min([len(pol3a[0]),len(pol3b[0])])
# pol3a = pol3a[:,:minlength]
# pol3b = pol3b[:,:minlength]
# pol3 = np.sqrt(pol3a**2+pol3b**2)
plot_bandpass([pol3[0], pol3[1]],outdir+'mfi_pol3_ch1.png')
plot_bandpass([pol3[0], pol3[2]],outdir+'mfi_pol3_ch2.png')
plot_bandpass([pol3[0], pol3[3]],outdir+'mfi_pol3_ch3.png')
plot_bandpass([pol3[0], pol3[4]],outdir+'mfi_pol3_ch4.png')
plot_bandpass([pol3[0], pol3[5]],outdir+'mfi_pol3_ch5.png')
plot_bandpass([pol3[0], pol3[6]],outdir+'mfi_pol3_ch6.png')
plot_bandpass([pol3[0], pol3[7]],outdir+'mfi_pol3_ch7.png')
plot_bandpass([pol3[0], pol3[8]],outdir+'mfi_pol3_ch8.png')
# pol4 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/Pol4_bandpass.dat')
# pol4 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020_05_21_Pol4_bandpass.dat')
pol4 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020-10_Horn4_bandpass_intensity.dat')
pol4_pol = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020-10_Horn4_bandpass_polarization.dat')
# pol4 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020_05_22_0deg_Pol4_bandpass.dat')
# pol4 = read_quijote_mfi_bandpass('/Users/mpeel/Documents/maps/quijote_mfi/2020_05_22_22p5deg_Pol4_bandpass.dat')
# minlength = np.min([len(pol4a[0]),len(pol4b[0])])
# pol4a = pol4a[:,:minlength]
# pol4b = pol4b[:,:minlength]
# pol4 = np.sqrt(pol4a**2+pol4b**2)
for i in range(1,9):
	pol4[i][pol4[0]<14] = 0.0
plot_bandpass([pol4[0], pol4[1]],outdir+'mfi_pol4_ch1.png')
plot_bandpass([pol4[0], pol4[2]],outdir+'mfi_pol4_ch2.png')
plot_bandpass([pol4[0], pol4[3]],outdir+'mfi_pol4_ch3.png')
plot_bandpass([pol4[0], pol4[4]],outdir+'mfi_pol4_ch4.png')
plot_bandpass([pol4[0], pol4[5]],outdir+'mfi_pol4_ch5.png')
plot_bandpass([pol4[0], pol4[6]],outdir+'mfi_pol4_ch6.png')
plot_bandpass([pol4[0], pol4[7]],outdir+'mfi_pol4_ch7.png')
plot_bandpass([pol4[0], pol4[8]],outdir+'mfi_pol4_ch8.png')

plot_bandpass_all([[pol1[0], pol1[1]], [pol1[0], pol1[2]], [pol1[0], pol1[3]], [pol1[0], pol1[4]], [pol1[0], pol1[5]],[pol1[0], pol1[6]], [pol1[0], pol1[7]], [pol1[0], pol1[8]], [pol2[0], pol2[1]], [pol2[0], pol2[2]], [pol2[0], pol2[3]], [pol2[0], pol2[4]], [pol2[0], pol2[5]], [pol2[0], pol2[6]], [pol2[0], pol2[7]], [pol2[0], pol2[8]], [pol3[0], pol3[1]], [pol3[0], pol3[2]], [pol3[0], pol3[3]], [pol3[0], pol3[4]], [pol3[0], pol3[5]], [pol3[0], pol3[6]], [pol3[0], pol3[7]], [pol3[0], pol3[8]], [pol4[0], pol4[1]], [pol4[0], pol4[2]], [pol4[0], pol4[3]], [pol4[0], pol4[4]], [pol4[0], pol4[5]], [pol4[0], pol4[6]], [pol4[0], pol4[7]],[pol4[0], pol4[8]]], outdir+'mfi_comb.pdf')

mfi111 = combine_bandpasses([pol1[0], pol1[2]], [pol1[0], pol1[4]],[pol1[0], pol1[6]],[pol1[0], pol1[8]])
plot_bandpass(mfi111,outdir+'mfi_111.png')
mfi113 = combine_bandpasses([pol1[0], pol1[1]], [pol1[0], pol1[3]],[pol1[0], pol1[5]],[pol1[0], pol1[7]])
plot_bandpass(mfi113,outdir+'mfi_113.png')
mfi217 = combine_bandpasses([pol2[0], pol2[2]], [pol2[0], pol2[4]],[pol2[0], pol2[6]],[pol2[0], pol2[8]])
plot_bandpass(mfi217,outdir+'mfi_217.png')
mfi219 = combine_bandpasses([pol2[0], pol2[1]], [pol2[0], pol2[3]],[pol2[0], pol2[5]],[pol2[0], pol2[7]])
plot_bandpass(mfi219,outdir+'mfi_219.png')
mfi217_pol = combine_bandpasses([pol2_pol[0], pol2_pol[2]], [pol2_pol[0], pol2_pol[4]],[pol2_pol[0], pol2_pol[6]],[pol2_pol[0], pol2_pol[8]])
plot_bandpass(mfi217_pol,outdir+'mfi_217_pol.png')
mfi219_pol = combine_bandpasses([pol2_pol[0], pol2_pol[1]], [pol2_pol[0], pol2_pol[3]],[pol2_pol[0], pol2_pol[5]],[pol2_pol[0], pol2_pol[7]])
plot_bandpass(mfi219_pol,outdir+'mfi_219_pol.png')
mfi311 = combine_bandpasses([pol3[0], pol3[2]], [pol3[0], pol3[4]],[pol3[0], pol3[6]],[pol3[0], pol3[8]])
plot_bandpass(mfi311,outdir+'mfi_311.png')
mfi313 = combine_bandpasses([pol3[0], pol3[1]], [pol3[0], pol3[3]],[pol3[0], pol3[5]],[pol3[0], pol3[7]])
plot_bandpass(mfi313,outdir+'mfi_313.png')
mfi311pol = combine_bandpasses([pol3_pol[0], pol3_pol[2]], [pol3_pol[0], pol3_pol[4]],[pol3_pol[0], pol3_pol[6]],[pol3_pol[0], pol3_pol[8]])
plot_bandpass(mfi311pol,outdir+'mfi_311_pol.png')
mfi313pol = combine_bandpasses([pol3_pol[0], pol3_pol[1]], [pol3_pol[0], pol3_pol[3]],[pol3_pol[0], pol3_pol[5]],[pol3_pol[0], pol3_pol[7]])
plot_bandpass(mfi313pol,outdir+'mfi_313_pol.png')
# mfi311orig = combine_bandpasses([pol3_orig[0], pol3_orig[2]], [pol3_orig[0], pol3_orig[4]],[pol3_orig[0], pol3_orig[6]],[pol3_orig[0], pol3_orig[8]])
# plot_bandpass(mfi311orig,outdir+'mfi_311_orig.png')
# mfi313orig = combine_bandpasses([pol3_orig[0], pol3_orig[1]], [pol3_orig[0], pol3_orig[3]],[pol3_orig[0], pol3_orig[5]],[pol3_orig[0], pol3_orig[7]])
# plot_bandpass(mfi313orig,outdir+'mfi_313_orig.png')
mfi417 = combine_bandpasses([pol4[0], pol4[2]], [pol4[0], pol4[4]],[pol4[0], pol4[6]],[pol4[0], pol4[8]])
plot_bandpass(mfi417,outdir+'mfi_417.png')
mfi419 = combine_bandpasses([pol4[0], pol4[1]], [pol4[0], pol4[3]],[pol4[0], pol4[5]],[pol4[0], pol4[7]])
plot_bandpass(mfi419,outdir+'mfi_419.png')
mfi417_pol = combine_bandpasses([pol4_pol[0], pol4_pol[2]], [pol4_pol[0], pol4_pol[4]],[pol4_pol[0], pol4_pol[6]],[pol4_pol[0], pol4_pol[8]])
plot_bandpass(mfi417_pol,outdir+'mfi_417.png')
mfi419_pol = combine_bandpasses([pol4_pol[0], pol4_pol[1]], [pol4_pol[0], pol4_pol[3]],[pol4_pol[0], pol4_pol[5]],[pol4_pol[0], pol4_pol[7]])
plot_bandpass(mfi419_pol,outdir+'mfi_419_pol.png')


plot_bandpass_all([mfi111, mfi113, mfi217, mfi219, mfi311, mfi313, mfi417, mfi419], outdir+'mfi_comb_band.pdf')

mfi111_corrections = np.ones(len(alphas))
mfi113_corrections = np.ones(len(alphas))
mfi217_corrections = np.ones(len(alphas))
mfi219_corrections = np.ones(len(alphas))
mfi217_pol_corrections = np.ones(len(alphas))
mfi219_pol_corrections = np.ones(len(alphas))
mfi311_corrections = np.ones(len(alphas))
mfi311pol_corrections = np.ones(len(alphas))
# mfi311orig_corrections = np.ones(len(alphas))
mfi313_corrections = np.ones(len(alphas))
mfi313pol_corrections = np.ones(len(alphas))
# mfi313orig_corrections = np.ones(len(alphas))
mfi417_corrections = np.ones(len(alphas))
mfi419_corrections = np.ones(len(alphas))
mfi417_pol_corrections = np.ones(len(alphas))
mfi419_pol_corrections = np.ones(len(alphas))

calindex = 2.0#-0.3
usecorr = False
for i in range(0,len(alphas)):
	mfi111_corrections[i] = calc_correction(mfi111, 11.2, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi113_corrections[i] = calc_correction(mfi113, 12.8, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi217_corrections[i] = calc_correction(mfi217, 16.7, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi219_corrections[i] = calc_correction(mfi219, 18.7, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi217_pol_corrections[i] = calc_correction(mfi217_pol, 16.7, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi219_pol_corrections[i] = calc_correction(mfi219_pol, 18.7, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi311_corrections[i] = calc_correction(mfi311, 11.1, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi313_corrections[i] = calc_correction(mfi313, 12.9, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi311pol_corrections[i] = calc_correction(mfi311pol, 11.1, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi313pol_corrections[i] = calc_correction(mfi313pol, 12.9, alphas[i],calindex=calindex,usecorr=usecorr)
	# mfi311orig_corrections[i] = calc_correction(mfi311orig, 11.1, alphas[i],calindex=calindex,usecorr=usecorr)
	# mfi313orig_corrections[i] = calc_correction(mfi313orig, 12.9, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi417_corrections[i] = calc_correction(mfi417, 17.0, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi419_corrections[i] = calc_correction(mfi419, 19.0, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi417_pol_corrections[i] = calc_correction(mfi417_pol, 17.0, alphas[i],calindex=calindex,usecorr=usecorr)
	mfi419_pol_corrections[i] = calc_correction(mfi419_pol, 19.0, alphas[i],calindex=calindex,usecorr=usecorr)

print(alphas)
print('From bandpasses:')
print(mfi111_corrections)
print(mfi113_corrections)
print(mfi217_corrections)
print(mfi219_corrections)
print(mfi217_pol_corrections)
print(mfi219_pol_corrections)
print(mfi311_corrections)
print(mfi313_corrections)
print(mfi311pol_corrections)
print(mfi313pol_corrections)
# print(mfi311orig_corrections)
# print(mfi313orig_corrections)
print(mfi417_corrections)
print(mfi419_corrections)
print(mfi417_pol_corrections)
print(mfi419_pol_corrections)
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
# plt.plot(alphas,mfi311orig_corrections,'-g',label='311orig')
# plt.plot(alphas,mfi313orig_corrections,'-.g',label='313orig')
plt.plot(alphas,mfi417_corrections,label='417')
plt.plot(alphas,mfi419_corrections,label='419')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.xlabel('Spectral index')
plt.ylabel('Colour correction')
plt.savefig(outdir+'mfi_corrections.pdf')
plt.clf()
plt.close()

plt.plot(alphas,mfi111_corrections,label='111')
plt.plot(alphas,mfi113_corrections,label='113')
plt.plot(alphas,mfi217_pol_corrections,label='217pol')
plt.plot(alphas,mfi219_pol_corrections,label='219pol')
plt.plot(alphas,mfi311pol_corrections,label='311pol')
plt.plot(alphas,mfi313pol_corrections,label='313pol')
plt.plot(alphas,mfi417_pol_corrections,label='417pol')
plt.plot(alphas,mfi419_pol_corrections,label='419pol')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.xlabel('Spectral index')
plt.ylabel('Colour correction')
plt.savefig(outdir+'mfi_corrections_pol.pdf')
plt.clf()
plt.close()

print('Horn 1:')
params = np.polyfit(alphas,mfi111_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='111_fit')
params = np.polyfit(alphas,mfi113_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='113_fit')
print('Horn 2:')
params = np.polyfit(alphas,mfi217_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='217_fit')
params = np.polyfit(alphas,mfi219_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='219_fit')
params = np.polyfit(alphas,mfi217_pol_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='217pol_fit')
params = np.polyfit(alphas,mfi219_pol_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='219pol_fit')
print('Horn 3:')
params = np.polyfit(alphas,mfi311_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='311_fit')
params = np.polyfit(alphas,mfi313_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='313_fit')
params = np.polyfit(alphas,mfi311pol_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='311pol_fit')
params = np.polyfit(alphas,mfi313pol_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='313pol_fit')
print('Horn 4:')
params = np.polyfit(alphas,mfi417_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='417_fit')
params = np.polyfit(alphas,mfi419_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='419_fit')
params = np.polyfit(alphas,mfi417_pol_corrections,2)
print(params)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='417pol_fit')
params = np.polyfit(alphas,mfi419_pol_corrections,2)
plt.plot(alphas,params[2]+params[1]*alphas+params[0]*alphas**2,'-',label='419pol_fit')
print(params)
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.xlabel('Spectral index')
plt.ylabel('Colour correction')
plt.savefig(outdir+'mfi_corrections_fit.pdf')
plt.clf()
plt.close()

roke_11 = [0.9589, 0.01601, 0.002185]
roke_13 = [1.022, -0.01436, 0.001688]
roke_17 = [1.029, -0.01618,  0.0008349]
roke_19 = [1.029, -0.01588, 0.0007932]
plt.plot(alphas,1.0/(roke_11[0]+roke_11[1]*alphas+roke_11[2]*alphas**2),'-',label='11_roke')
plt.plot(alphas,1.0/(roke_13[0]+roke_13[1]*alphas+roke_13[2]*alphas**2),'-',label='13_roke')
plt.plot(alphas,1.0/(roke_17[0]+roke_17[1]*alphas+roke_17[2]*alphas**2),'-',label='17_roke')
plt.plot(alphas,1.0/(roke_19[0]+roke_19[1]*alphas+roke_19[2]*alphas**2),'-',label='19_roke')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.savefig(outdir+'mfi_corrections_roke.pdf')
plt.clf()
plt.close()

print(mfi219_corrections[alphas == -0.5] - mfi419_corrections[alphas == -0.5])
print(mfi217_corrections[alphas == -0.5] - mfi417_corrections[alphas == -0.5])
exit()
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
	print(str(alphas[i]) + " - " + str(calc_correction(bp_planck_70_ds1, 70.4, alphas[i])) + " - " + str(fastcc('70',alphas[i])) + " - " + str(fastcc('70',alphas[i],detector='1823',latest=True)))

for i in range(0,len(alphas)):
	print(str(alphas[i]) + " - " + str(calc_correction(bp_planck_70, 70.4, alphas[i])) + " - " + str(fastcc('70',alphas[i])) + " - " + str(fastcc('70',alphas[i],latest=True)))

for i in range(0,len(alphas)):
	print(str(alphas[i]) + " - " + str(calc_correction(bp_planck_44, 44.1, alphas[i])) + " - " + str(fastcc('44',alphas[i])) + " - " + str(fastcc('44',alphas[i],latest=True)))

for i in range(0,len(alphas)):
	print(str(alphas[i]) + " - " + str(calc_correction(bp_planck_30, 28.4, alphas[i])) + " - " + str(fastcc('30',alphas[i])) + " - " + str(fastcc('30',alphas[i],latest=True)))
