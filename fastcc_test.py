#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Test code for fastcc
# 
# Version history:
# Mike Peel   01-Feb-2013   v1.0 Initial version
# Mike Peel   04-Feb-2013   v1.1 Update format
# Locke Spencer 05-Feb-2013:  v1.2 changed planckcc to LFI_fastcc within this code to follow changes to LFI_fastcc
#                             renamed this routine LFI_fastcc_test, from planckcc_test, to follow convention of other changes.
#                             changed this routine from a script to a procedure so that it can be included within the hfi_lfi_test_script example routine also.
# Mike Peel   24-Jul-2014   v2.0 Expand to include WMAP, and to use new function calls.
# Mike Peel   06-Nov-2014   v2.1 Add development version.
# Mike Peel   22-Jan-2016   v2.2 Convert from IDL to Python. Does not currently work on arrays of spectra.
# Mike Peel   17-Jul-2019   v2.3 Update. Use np.asarray for arrays of spectra.
# Mike Peel   18-Jul-2019   v2.4 Update to add CBASS, and nominal frequencies.
# Mike Peel   06-Oct-2020   v2.7 Update QUIJOTE
# Mike Peel   21-Oct-2020   v2.7.1 Note that WMAP9 in original is different frequencies from latest
# Mike Peel   16-Oct-2020   v2.9 BREAKING CHANGE, 'latest' is now 'option', adding HFI and 2018
# Mike Peel   15-Jan-2021   v3.0 BREAKING CHANGE, frequency/detector labels now have prefixes. Upgrading to return frequencies and to prepare for colour corrections for thermal dust models for Planck HFI (not added in this version). Updated numbers for MFI, HFI, C-BASS.
# Mike Peel   10-Feb-2021   v3.1 Adding DIRBE and IRAS
# Mike Peel   26-Feb-2021   v3.2 Updating QUIJOTE, HFI, DIRBE, IRAS, adding HFI modified black body
# Mike Peel   01-Mar-2021   v3.3 Updating QUIJOTE 17 and 19GHz

from fastcc import fastcc
import numpy as np

spectra = np.asarray([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
print('Colour corrections for WMAP, Planck, QUIJOTE and CBASS. The convention is always F_corr = C * F_uncorr.')
print('2013 VERSION:')
print('Detector	alpha',spectra)
print('LFI-18',fastcc('P70',spectra,detector='P18',option=1))
print('LFI-19',fastcc('P70',spectra,detector='P19',option=1))
print('LFI-20',fastcc('P70',spectra,detector='P20',option=1))
print('LFI-21',fastcc('P70',spectra,detector='P21',option=1))
print('LFI-22',fastcc('P70',spectra,detector='P22',option=1))
print('LFI-23',fastcc('P70',spectra,detector='P23',option=1))
print('70GHz (70.4GHz)',fastcc('P70',spectra,option=1))

print('LFI-24',fastcc('P44',spectra,detector='P24',option=1))
print('LFI-25',fastcc('P44',spectra,detector='P25',option=1))
print('LFI-26',fastcc('P44',spectra,detector='P26',option=1))
print('44GHz (44.1GHz)',fastcc('P44',spectra,option=1))

print('LFI-27',fastcc('P30',spectra,detector='P27',option=1))
print('LFI-28',fastcc('P30',spectra,detector='P28',option=1))
print('30GHz (28.4GHz)',fastcc('P30',spectra,option=1))

print('HFI 100GHz',fastcc('P100',spectra,option=1))
print('HFI 143GHz',fastcc('P143',spectra,option=1))
print('HFI 217GHz',fastcc('P217',spectra,option=1))
print('HFI 353GHz',fastcc('P353',spectra,option=1))
print('HFI 545GHz',fastcc('P545',spectra,option=1))
print('HFI 857GHz',fastcc('P857',spectra,option=1))

print('WMAP from Bennet et al. 2012')
print('K (22.8GHz)',fastcc('WK',spectra,option=1))
print('Ka (33.0GHz)',fastcc('WKa',spectra,option=1))
print('Q (40.7GHz - different from latest)',fastcc('WQ',spectra,option=1))
print('V (60.7GHz - different from latest)',fastcc('WV',spectra,option=1))
print('W (93.5GHz)',fastcc('WW',spectra,option=1))

print('QUIJOTE 1st version. For 11, 13, 17, 19GHz combined maps, use 311, 313, 217, 219 respectively.')
print('QUIJOTE 111 (11.2GHz)', fastcc('Q11',spectra,detector='Q111',option=1))
print('QUIJOTE 113 (12.8GHz)', fastcc('Q13',spectra,detector='Q113',option=1))
print('QUIJOTE 217 (16.7GHz)', fastcc('Q17',spectra,detector='Q217',option=1))
print('QUIJOTE 219 (18.7GHz)', fastcc('Q19',spectra,detector='Q219',option=1))
print('QUIJOTE 311 (11.1GHz)', fastcc('Q11',spectra,detector='Q311',option=1))
print('QUIJOTE 313 (12.9GHz)', fastcc('Q13',spectra,detector='Q313',option=1))
print('QUIJOTE 417 (17GHz)', fastcc('Q17',detector='Q417',option=1))
print('QUIJOTE 419 (19GHz)', fastcc('Q19',detector='Q419',option=1))
print('QUIJOTE 11 (11.1GHz)', fastcc('Q11',spectra,option=1))
print('QUIJOTE 13 (12.9GHz)', fastcc('Q13',spectra,option=1))
print('QUIJOTE 17 (16.7GHz)', fastcc('Q17',spectra,option=1))
print('QUIJOTE 19 (18.7GHz)', fastcc('Q19',spectra,option=1))

print('2015 VERSION:')
print('Detector alpha',spectra)
print('LFI-18',fastcc('P70',spectra,detector='P18',option=2))
print('LFI-19',fastcc('P70',spectra,detector='P19',option=2))
print('LFI-20',fastcc('P70',spectra,detector='P20',option=2))
print('LFI-21',fastcc('P70',spectra,detector='P21',option=2))
print('LFI-22',fastcc('P70',spectra,detector='P22',option=2))
print('LFI-23',fastcc('P70',spectra,detector='P23',option=2))
print('LFI-18-23',fastcc('P70',spectra,detector='P1823',option=2))
print('LFI-19-22',fastcc('P70',spectra,detector='P1922',option=2))
print('LFI-20-21',fastcc('P70',spectra,detector='P2021',option=2))
print('70GHz (70.4GHz)',fastcc('P70',spectra,option=2))

print('LFI-24',fastcc('P44',spectra,detector='P24',option=2))
print('LFI-25',fastcc('P44',spectra,detector='P25',option=2))
print('LFI-26',fastcc('P44',spectra,detector='P26',option=2))
print('LFI-25-26',fastcc('P44',spectra,detector='P2526',option=2))
print('44GHz (44.1GHz)',fastcc('P44',spectra,option=2))

print('LFI-27',fastcc('P30',spectra,detector='P27',option=2))
print('LFI-28',fastcc('P30',spectra,detector='P28',option=2))
print('30GHz (28.4GHz)',fastcc('P30',spectra,option=2))

print('HFI 100GHz',fastcc('P100',spectra,option=2))
print('HFI 143GHz',fastcc('P143',spectra,option=2))
print('HFI 217GHz',fastcc('P217',spectra,option=2))
print('HFI 353GHz',fastcc('P353',spectra,option=2))
print('HFI 545GHz',fastcc('P545',spectra,option=2))
print('HFI 857GHz',fastcc('P857',spectra,option=2))


print('WMAP')
print('K11',fastcc('WK',spectra,detector='WK11',option=2))
print('K12',fastcc('WK',spectra,detector='WK12',option=2))
print('K1',fastcc('WK',spectra,detector='WK1',option=2))
print('K (22.8GHz)',fastcc('WK',spectra,option=2))

print('Ka11',fastcc('WKa',spectra,detector='WKa11',option=2))
print('Ka12',fastcc('WKa',spectra,detector='WKa12',option=2))
print('Ka1',fastcc('WKa',spectra,detector='WKa1',option=2))
print('Ka (33.0GHz)',fastcc('WKa',spectra,option=2))

print('Q11',fastcc('WQ',spectra,detector='WQ11',option=2))
print('Q12',fastcc('WQ',spectra,detector='WQ12',option=2))
print('Q1',fastcc('WQ',spectra,detector='WQ1',option=2))
print('Q21',fastcc('WQ',spectra,detector='WQ21',option=2))
print('Q22',fastcc('WQ',spectra,detector='WQ22',option=2))
print('Q2',fastcc('WQ',spectra,detector='WQ2',option=2))
print('Q (40.6GHz)',fastcc('WQ',spectra,option=2))

print('V11',fastcc('WV',spectra,detector='WV11',option=2))
print('V12',fastcc('WV',spectra,detector='WV12',option=2))
print('V1',fastcc('WV',spectra,detector='WV1',option=2))
print('V21',fastcc('WV',spectra,detector='WV21',option=2))
print('V22',fastcc('WV',spectra,detector='WV22',option=2))
print('V2',fastcc('WV',spectra,detector='WV2',option=2))
print('V (60.8GHz)',fastcc('WV',spectra,option=2))

print('W11',fastcc('WW',spectra,detector='WW11',option=2))
print('W12',fastcc('WW',spectra,detector='WW12',option=2))
print('W1',fastcc('WW',spectra,detector='WW1',option=2))
print('W21',fastcc('WW',spectra,detector='WW21',option=2))
print('W22',fastcc('WW',spectra,detector='WW22',option=2))
print('W2',fastcc('WW',spectra,detector='WW2',option=2))
print('W31',fastcc('WW',spectra,detector='WW31',option=2))
print('W32',fastcc('WW',spectra,detector='WW32',option=2))
print('W3',fastcc('WW',spectra,detector='WW3',option=2))
print('W41',fastcc('WW',spectra,detector='WW41',option=2))
print('W42',fastcc('WW',spectra,detector='WW42',option=2))
print('W4',fastcc('WW',spectra,detector='WW4',option=2))
print('W (93.5GHz)',fastcc('WW',spectra,option=2))

print('QUIJOTE 2nd version.')
print('QUIJOTE 111 (11.2GHz)', fastcc('Q11',spectra,detector='Q111',option=2))
print('QUIJOTE 113 (12.8GHz)', fastcc('Q13',spectra,detector='Q113',option=2))
print('QUIJOTE 111 pol (11.2GHz)', fastcc('Q11',spectra,detector='Q111p',option=2))
print('QUIJOTE 113 pol (12.8GHz)', fastcc('Q13',spectra,detector='Q113p',option=2))
print('QUIJOTE 217 (16.7GHz)', fastcc('Q17',spectra,detector='Q217',option=2))
print('QUIJOTE 219 (18.7GHz)', fastcc('Q19',spectra,detector='Q219',option=2))
print('QUIJOTE 217 pol (16.7GHz)', fastcc('Q17',spectra,detector='Q217p',option=2))
print('QUIJOTE 219 pol (18.7GHz)', fastcc('Q19',spectra,detector='Q219p',option=2))
print('QUIJOTE 311 (11.1GHz)', fastcc('Q11',spectra,detector='Q311',option=2))
print('QUIJOTE 313 (12.9GHz)', fastcc('Q13',spectra,detector='Q313',option=2))
print('QUIJOTE 311 pol (11.1GHz)', fastcc('Q11',spectra,detector='Q311p',option=2))
print('QUIJOTE 313 pol (12.9GHz)', fastcc('Q13',spectra,detector='Q313p',option=2))
print('QUIJOTE 417 (17GHz)', fastcc('Q17',spectra,detector='Q417',option=2))
print('QUIJOTE 419 (19GHz)', fastcc('Q19',spectra,detector='Q419',option=2))
print('QUIJOTE 417 pol (17GHz)', fastcc('Q17',spectra,detector='Q417p',option=2))
print('QUIJOTE 419 pol (19GHz)', fastcc('Q19',spectra,detector='Q419p',option=2))

print('QUIJOTE 11 (11.1GHz)', fastcc('Q11',spectra,option=2))
print('QUIJOTE 13 (12.9GHz)', fastcc('Q13',spectra,option=2))
print('QUIJOTE 11 pol (11.1GHz)', fastcc('Q11p',spectra,option=2))
print('QUIJOTE 13 pol (12.9GHz)', fastcc('Q13p',spectra,option=2))
print('QUIJOTE 17 (16.7GHz)', fastcc('Q17',spectra,option=2))
print('QUIJOTE 19 (18.7GHz)', fastcc('Q19',spectra,option=2))
print('QUIJOTE 17 pol (16.7GHz)', fastcc('Q17p',spectra,option=2))
print('QUIJOTE 19 pol (18.7GHz)', fastcc('Q19p',spectra,option=2))

print('CBASS-N, 4.76GHz:')
print("CBASS-N I:", fastcc('CBASSNI', spectra,option=2))
print("CBASS-N P:", fastcc('CBASSNP', spectra,option=2))


print('2018 VERSION:')
print('Detector alpha',spectra)
print('LFI-18',fastcc('P70',spectra,detector='P18'))
print('LFI-19',fastcc('P70',spectra,detector='P19'))
print('LFI-20',fastcc('P70',spectra,detector='P20'))
print('LFI-21',fastcc('P70',spectra,detector='P21'))
print('LFI-22',fastcc('P70',spectra,detector='P22'))
print('LFI-23',fastcc('P70',spectra,detector='P23'))
print('LFI-18-23',fastcc('P70',spectra,detector='P1823'))
print('LFI-19-22',fastcc('P70',spectra,detector='P1922'))
print('LFI-20-21',fastcc('P70',spectra,detector='P2021'))
print('70GHz (70.4GHz)',fastcc('P70',spectra))

print('LFI-24',fastcc('P44',spectra,detector='P24'))
print('LFI-25',fastcc('P44',spectra,detector='P25'))
print('LFI-26',fastcc('P44',spectra,detector='P26'))
print('LFI-25-26',fastcc('P44',spectra,detector='P2526'))
print('44GHz (44.1GHz)',fastcc('P44',spectra))

print('LFI-27',fastcc('P30',spectra,detector='P27'))
print('LFI-28',fastcc('P30',spectra,detector='P28'))
print('30GHz (28.4GHz)',fastcc('P30',spectra))

print('HFI 100GHz',fastcc('P100',spectra))
print('HFI 143GHz',fastcc('P143',spectra))
print('HFI 217GHz',fastcc('P217',spectra))
print('HFI 353GHz',fastcc('P353',spectra))
print('HFI 545GHz',fastcc('P545',spectra))
print('HFI 857GHz',fastcc('P857',spectra))

print('WMAP')
print('K11',fastcc('WK',spectra,detector='WK11'))
print('K12',fastcc('WK',spectra,detector='WK12'))
print('K1',fastcc('WK',spectra,detector='WK1'))
print('K (22.8GHz)',fastcc('WK',spectra))

print('Ka11',fastcc('WKa',spectra,detector='WKa11'))
print('Ka12',fastcc('WKa',spectra,detector='WKa12'))
print('Ka1',fastcc('WKa',spectra,detector='WKa1'))
print('Ka (33.0GHz)',fastcc('WKa',spectra))

print('Q11',fastcc('WQ',spectra,detector='WQ11'))
print('Q12',fastcc('WQ',spectra,detector='WQ12'))
print('Q1',fastcc('WQ',spectra,detector='WQ1'))
print('Q21',fastcc('WQ',spectra,detector='WQ21'))
print('Q22',fastcc('WQ',spectra,detector='WQ22'))
print('Q2',fastcc('WQ',spectra,detector='WQ2'))
print('Q (40.6GHz)',fastcc('WQ',spectra))

print('V11',fastcc('WV',spectra,detector='WV11'))
print('V12',fastcc('WV',spectra,detector='WV12'))
print('V1',fastcc('WV',spectra,detector='WV1'))
print('V21',fastcc('WV',spectra,detector='WV21'))
print('V22',fastcc('WV',spectra,detector='WV22'))
print('V2',fastcc('WV',spectra,detector='WV2'))
print('V (60.8GHz)',fastcc('WV',spectra))

print('W11',fastcc('WW',spectra,detector='WW11'))
print('W12',fastcc('WW',spectra,detector='WW12'))
print('W1',fastcc('WW',spectra,detector='WW1'))
print('W21',fastcc('WW',spectra,detector='WW21'))
print('W22',fastcc('WW',spectra,detector='WW22'))
print('W2',fastcc('WW',spectra,detector='WW2'))
print('W31',fastcc('WW',spectra,detector='WW31'))
print('W32',fastcc('WW',spectra,detector='WW32'))
print('W3',fastcc('WW',spectra,detector='WW3'))
print('W41',fastcc('WW',spectra,detector='WW41'))
print('W42',fastcc('WW',spectra,detector='WW42'))
print('W4',fastcc('WW',spectra,detector='WW4'))
print('W (93.5GHz)',fastcc('WW',spectra))

print('QUIJOTE 2nd version.')
print('QUIJOTE 111 (11.2GHz)', fastcc('Q11',spectra,detector='Q111'))
print('QUIJOTE 113 (12.8GHz)', fastcc('Q13',spectra,detector='Q113'))
print('QUIJOTE 111 pol (11.2GHz)', fastcc('Q11',spectra,detector='Q111p'))
print('QUIJOTE 113 pol (12.8GHz)', fastcc('Q13',spectra,detector='Q113p'))
print('QUIJOTE 217 (16.7GHz)', fastcc('Q17',spectra,detector='Q217'))
print('QUIJOTE 219 (18.7GHz)', fastcc('Q19',spectra,detector='Q219'))
print('QUIJOTE 217 pol (16.7GHz)', fastcc('Q17',spectra,detector='Q217p'))
print('QUIJOTE 219 pol (18.7GHz)', fastcc('Q19',spectra,detector='Q219p'))
print('QUIJOTE 311 (11.1GHz)', fastcc('Q11',spectra,detector='Q311'))
print('QUIJOTE 313 (12.9GHz)', fastcc('Q13',spectra,detector='Q313'))
print('QUIJOTE 311 pol (11.1GHz)', fastcc('Q11',spectra,detector='Q311p'))
print('QUIJOTE 313 pol (12.9GHz)', fastcc('Q13',spectra,detector='Q313p'))
print('QUIJOTE 417 (17GHz)', fastcc('Q17',spectra,detector='Q417'))
print('QUIJOTE 419 (19GHz)', fastcc('Q19',spectra,detector='Q419'))
print('QUIJOTE 417 pol (17GHz)', fastcc('Q17',spectra,detector='Q417p'))
print('QUIJOTE 419 pol (19GHz)', fastcc('Q19',spectra,detector='Q419p'))

print('QUIJOTE 11 (11.1GHz)', fastcc('Q11',spectra))
print('QUIJOTE 13 (12.9GHz)', fastcc('Q13',spectra))
print('QUIJOTE 11 pol (11.1GHz)', fastcc('Q11p',spectra))
print('QUIJOTE 13 pol (12.9GHz)', fastcc('Q13p',spectra))
print('QUIJOTE 17 (16.7GHz)', fastcc('Q17',spectra))
print('QUIJOTE 19 (18.7GHz)', fastcc('Q19',spectra))
print('QUIJOTE 17 pol (16.7GHz)', fastcc('Q17p',spectra))
print('QUIJOTE 19 pol (18.7GHz)', fastcc('Q19p',spectra))

print('CBASS-N, 4.76GHz:')
print("CBASS-N I:", fastcc('CBASSNI', spectra))
print("CBASS-N U:", fastcc('CBASSNP', spectra))

print('DIRBE')
print("B10:", fastcc('DB10', spectra))
print("B9:", fastcc('DB9', spectra))
print("B8:", fastcc('DB8', spectra))
print("B7:", fastcc('DB7', spectra))
print("B6:", fastcc('DB6', spectra))
print("B5:", fastcc('DB5', spectra))
print("B4:", fastcc('DB4', spectra))
print("B3:", fastcc('DB3', spectra))
print("B2:", fastcc('DB2', spectra))
print("B1:", fastcc('DB1', spectra))

print('IRAS')
print("I100:", fastcc('I100', spectra))
print("I60:", fastcc('I60', spectra))
print("I25:", fastcc('I25', spectra))
print("I12:", fastcc('I12', spectra))


# EOF