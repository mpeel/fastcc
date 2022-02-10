#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Functions for cc_calc.py
# 
# Version history:
#
# 16-Jun-2019  M. Peel       Started
# 17-Jun-2019  M. Peel       Tidied up
# 13-Jan-2021  M. Peel       Split from cc_calc.py

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

def read_hfi_rimo_bandpass(filename,ext=0,nu0=100.0):
	inputfits = fits.open(filename)
	# print(len(inputfits))
	print(inputfits[ext].header)
	# print(inputfits.info())
	# exit()

	col_names = inputfits[ext].columns.names
	print(col_names)
	freq = []
	bandpass = []
	error = []
	flag = []
	# print(inputfits[ext].data)
	for i in range(0,len(inputfits[ext].data)):
		# print(inputfits[ext].data[i])
		# Conversion is because HFI uses wierd mks units rather than GHz...
		thisfreq = float(inputfits[ext].data[i][0])*1e-7*2.997e8
		if thisfreq > 0.5*nu0 and thisfreq < 2.0*nu0:
		# if float(inputfits[ext].data[i][1]) > 1e-7:
			freq.append(thisfreq)
			bandpass.append(float(inputfits[ext].data[i][1]))
		# error.append(inputfits[ext].data[i][2])
		# flag[i].append(inputfits[ext].data[i][3])

	# Renormalise the bandpass per eq20
	# const = get_spectrum_constants()
	# total = np.sum(bandpass)* (freq[2] - freq[1])
	# print(total)
	# bandpass /= total
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
		freq = dataset[i][0]
		band = dataset[i][1]
		plt.plot(freq,band/(np.sum(band)*(freq[10]-freq[9])))#,'b')
	# plt.yscale('log')
	plt.xlabel('Frequency (GHz)')
	plt.ylabel('Amplitude (arbitrary)')
	plt.tight_layout()
	plt.savefig(outname)
	plt.clf()
	plt.close()
	return


def plot_bandpass(dataset, outname):
	plt.plot(dataset[0],dataset[1],'b')
	# plt.yscale('log')
	# plt.xscale('log')
	plt.xlabel('Frequency (GHz)')
	plt.ylabel('Amplitude (arbitrary)')
	plt.savefig(outname)
	plt.clf()
	plt.close()
	return

def calc_correction(dataset,nu0,alpha,calindex=2.0,usecorr=True):
	const = get_spectrum_constants()
	# Following eq.17 from Planck 2013 V.
	# dnu = dataset[0][1] - dataset[0][0]
	if usecorr:
		# topsum = np.sum(dataset[1] / planckcorr(const, dataset[0])) * dnu
		# bottomcalc = np.sum(np.asarray(dataset[1]) * (np.asarray(dataset[0]) / nu0)**(alpha-calindex)) * dnu
		topsum = np.trapz(dataset[1] / planckcorr(const, dataset[0]), np.asarray(dataset[0]))
		bottomcalc = np.trapz(np.asarray(dataset[1]) * (np.asarray(dataset[0]) / nu0)**(alpha-calindex), np.asarray(dataset[0]))
		return topsum / ((1.0/planckcorr(const, nu0)) * bottomcalc)
	else:
		# topsum = np.sum(dataset[1]) * dnu
		# bottomcalc = np.sum(np.asarray(dataset[1]) * (np.asarray(dataset[0]) / nu0)**(alpha-calindex)) * dnu
		topsum = np.trapz(dataset[1], np.asarray(dataset[0]))
		bottomcalc = np.trapz(np.asarray(dataset[1]) * (np.asarray(dataset[0]) / nu0)**(alpha-calindex), np.asarray(dataset[0]))
		return topsum / bottomcalc


def calc_correction_hfi(dataset,nu0,alpha,calindex=2.0,usecorr=True):
	const = get_spectrum_constants()
	# Following eq.17 from Planck 2013 V.
	# dnu = dataset[0][1] - dataset[0][0]
	dnu = np.median(np.diff(dataset[0]))
	if usecorr:
		topsum = np.sum(dataset[1] / planckcorr(const, dataset[0])) * dnu
		bottomcalc = np.sum(np.asarray(dataset[1]) * (np.asarray(dataset[0]) / nu0)**(alpha-calindex)) * dnu
		return topsum / ((1.0/planckcorr(const, nu0)) * bottomcalc)
	else:
		topsum = np.trapz(dataset[1] * (nu0/np.asarray(dataset[0])), np.asarray(dataset[0]))
		bottomcalc = np.trapz(np.asarray(dataset[1]) * (np.asarray(dataset[0]) / nu0)**(alpha), np.asarray(dataset[0]))
		return topsum / bottomcalc

def calc_b_hfi(nu):
	const = get_spectrum_constants()
	x = const['h'] * nu * 1.0e9 / (const['k'] * const['tcmb'])
	exp_x = np.exp(x)
	return ((2.0*const['h']*(nu*1e9)**3)/((const['c']**2)*(exp_x-1.0)))*(exp_x/(exp_x-1.0))*((const['h']*nu*1e9)/(const['k']*(const['tcmb']**2)))
	# a = exp_x
	# b = 1.0/(a-1.0)
	# d = (2.0*const['h']**2*(nu*1e9)**4)/(const['c']**2*const['k']*const['tcmb']**2)
	# return a*d*b**2


def calc_unit_hfi(dataset,nu0):
	const = get_spectrum_constants()
	# Following eq.17 from Planck 2013 V.
	# dnu = dataset[0][1] - dataset[0][0]
	# dnu = np.median(np.diff(dataset[0]))
	# print(dataset[1] * calc_b_hfi(np.asarray(dataset[0])))
	# exit()
	# topsum = np.sum(np.multiply(np.asarray(dataset[1]),calc_b_hfi(np.asarray(dataset[0])))) * dnu * 1e20
	# topsum = np.sum(dataset[1] * calc_b_hfi(np.asarray(dataset[0]))) * dnu * 1e20
	# bottomsum = np.sum(np.asarray(dataset[1]) * (nu0/np.asarray(dataset[0]))) * dnu
	topsum = np.trapz(np.multiply(np.asarray(dataset[1]),calc_b_hfi(np.asarray(dataset[0]))), np.asarray(dataset[0])) * 1e20
	bottomsum = np.trapz(np.asarray(dataset[1]) * (nu0/np.asarray(dataset[0])),np.asarray(dataset[0]))
	return topsum / bottomsum

def calc_unit_RJ_hfi(dataset,nu0):
	const = get_spectrum_constants()
	return (2.0e20*const['k']*(nu0*1e9)**2)/(const['c']**2)

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

def trim_bandpass(bp, centralfreq, bandwidth):
	bp[1][bp[0]<(centralfreq-(bandwidth/2.0))] = 0.0
	bp[1][bp[0]>(centralfreq+(bandwidth/2.0))] = 0.0
	return bp
