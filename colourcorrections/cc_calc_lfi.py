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

outdir = 'plots_2020_10_06/'
print(outdir)
ensure_dir(outdir)

alphas = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
alphas = np.asarray(alphas)

# Below is for Planck LFI

# 2013 release. THE RIMO IS WRONG - it has an incorrect frequency shift of -0.1GHz in the bandpass.
planck_lfi_filename = '/Users/mpeel/Documents/maps/planck2013/LFI_RIMO_R1.12.fits'
bp_planck_30 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=2)
plot_bandpass(bp_planck_30,outdir+'planck_112_30.png')
bp_planck_44 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=3)
plot_bandpass(bp_planck_44,outdir+'planck_112_44.png')
bp_planck_70 = read_lfi_rimo_bandpass(planck_lfi_filename,ext=4)
plot_bandpass(bp_planck_70,outdir+'planck_112_70.png')

# 2015 release. Mistake in previous version fixed. Extra frequency shift from Commander needs to be applied.
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
