; Test code for planckcc
; Run with @planckcc_test -- changed this to a procedure (see below) so now it runs as `LFI_fastcc_test'.
; 
; Version history:
; Mike Peel   01-Feb-2013   v1.0 Initial version
; Mike Peel   04-Feb-2013   v1.1 Update format
; Locke Spencer 05-Feb-2013:  v1.2 changed planckcc to LFI_fastcc within this code to follow changes to LFI_fastcc
;                             renamed this routine LFI_fastcc_test, from planckcc_test, to follow convention of other changes.
;                             changed this routine from a script to a procedure so that it can be included within the hfi_lfi_test_script example routine also.
; Mike Peel   24-Jul-2014   v2.0 Expand to include WMAP, and to use new function calls.
; Mike Peel   06-Nov-2014   v2.1 Add development version.
; Mike Peel   17-Jul-2019   v2.3 Update. Use np.asarray for arrays of spectra.
; Mike Peel   18-Jul-2019   v2.4 Update to add CBASS, and nominal frequencies.
; Mike Peel   06-Oct-2020   v2.7 Update QUIJOTE
; Mike Peel   21-Oct-2020   v2.7.1 Note that WMAP9 in original is different frequencies from latest
; Mike Peel   16-Oct-2020   v2.9 BREAKING CHANGE, 'latest' is now 'option', adding HFI and 2018
PRO fastcc_test

spectra = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

print,'Colour corrections for WMAP, Planck, QUIJOTE and CBASS. The convention is always F_corr = C * F_uncorr.'
print,'2013 VERSION:'
print,'Detector	alpha',spectra
print,'LFI-18',fastcc('70',spectra,detector='18',option=1)
print,'LFI-19',fastcc('70',spectra,detector='19',option=1)
print,'LFI-20',fastcc('70',spectra,detector='20',option=1)
print,'LFI-21',fastcc('70',spectra,detector='21',option=1)
print,'LFI-22',fastcc('70',spectra,detector='22',option=1)
print,'LFI-23',fastcc('70',spectra,detector='23',option=1)
print,'70GHz (70.4GHz)',fastcc('70',spectra,option=1)

print,'LFI-24',fastcc('44',spectra,detector='24',option=1)
print,'LFI-25',fastcc('44',spectra,detector='25',option=1)
print,'LFI-26',fastcc('44',spectra,detector='26',option=1)
print,'44GHz (44.1GHz)',fastcc('44',spectra,option=1)

print,'LFI-27',fastcc('30',spectra,detector='27',option=1)
print,'LFI-28',fastcc('30',spectra,detector='28',option=1)
print,'30GHz (28.4GHz)',fastcc('30',spectra,option=1)
print,'100GHz',fastcc('100',spectra,option=1)
print,'143GHz',fastcc('143',spectra,option=1)
print,'217GHz',fastcc('217',spectra,option=1)
print,'353GHz',fastcc('353',spectra,option=1)
print,'545GHz',fastcc('545',spectra,option=1)
print,'857GHz',fastcc('857',spectra,option=1)

print,'WMAP from Bennet et al. 2012'
print,'K (22.8GHz)',fastcc('K',spectra,option=1)
print,'Ka (33.0GHz)',fastcc('Ka',spectra,option=1)
print,'Q (40.7GHz - different from latest)',fastcc('Q',spectra,option=1)
print,'V (60.7GHz - different from latest)',fastcc('V',spectra,option=1)
print,'W (93.5GHz)',fastcc('W',spectra,option=1)

print,'QUIJOTE 1st version. For 11, 13, 17, 19GHz combined maps, use 311, 313, 217, 219 respectively.'
print,'QUIJOTE 111 (11.2GHz)',fastcc('111',spectra,option=1)
print,'QUIJOTE 113 (12.8GHz)',fastcc('113',spectra,option=1)
print,'QUIJOTE 217 (16.7GHz)',fastcc('217',spectra,option=1)
print,'QUIJOTE 219 (18.7GHz)',fastcc('219',spectra,option=1)
print,'QUIJOTE 311 (11.1GHz)',fastcc('311',spectra,option=1)
print,'QUIJOTE 313 (12.9GHz)',fastcc('313',spectra,option=1)
print,'QUIJOTE 417 (17GHz)',fastcc('417',spectra,option=1)
print,'QUIJOTE 419 (19GHz)',fastcc('419',spectra,option=1)

print,''
print,'2015 VERSION:'
print,'Detector	alpha',spectra
print,'LFI-18',fastcc('70',spectra,detector='18',option=2)
print,'LFI-19',fastcc('70',spectra,detector='19',option=2)
print,'LFI-20',fastcc('70',spectra,detector='20',option=2)
print,'LFI-21',fastcc('70',spectra,detector='21',option=2)
print,'LFI-22',fastcc('70',spectra,detector='22',option=2)
print,'LFI-23',fastcc('70',spectra,detector='23',option=2)
print,'LFI-18-23',fastcc('70',spectra,detector='1823',option=2)
print,'LFI-19-22',fastcc('70',spectra,detector='1922',option=2)
print,'LFI-20-21',fastcc('70',spectra,detector='2021',option=2)
print,'70GHz (70.4GHz)',fastcc('70',spectra,option=2)

print,'LFI-24',fastcc('44',spectra,detector='24',option=2)
print,'LFI-25',fastcc('44',spectra,detector='25',option=2)
print,'LFI-26',fastcc('44',spectra,detector='26',option=2)
print,'LFI-25-26',fastcc('44',spectra,detector='2526',option=2)
print,'44GHz (44.1GHz)',fastcc('44',spectra,option=2)

print,'LFI-27',fastcc('30',spectra,detector='27',option=2)
print,'LFI-28',fastcc('30',spectra,detector='28',option=2)
print,'30GHz (28.4GHz)',fastcc('30',spectra,option=2)

print,'100GHz',fastcc('100',spectra,option=2)
print,'143GHz',fastcc('143',spectra,option=2)
print,'217GHz',fastcc('217',spectra,option=2)
print,'353GHz',fastcc('353',spectra,option=2)
print,'545GHz',fastcc('545',spectra,option=2)
print,'857GHz',fastcc('857',spectra,option=2)

print,'WMAP'
print,'K11',fastcc('K',spectra,detector='K11',option=2)
print,'K12',fastcc('K',spectra,detector='K12',option=2)
print,'K1',fastcc('K',spectra,detector='K1',option=2)
print,'K (22.8GHz)',fastcc('K',spectra,option=2)

print,'Ka11',fastcc('Ka',spectra,detector='Ka11',option=2)
print,'Ka12',fastcc('Ka',spectra,detector='Ka12',option=2)
print,'Ka1',fastcc('Ka',spectra,detector='Ka1',option=2)
print,'Ka (33.0GHz)',fastcc('Ka',spectra,option=2)

print,'Q11',fastcc('Q',spectra,detector='Q11',option=2)
print,'Q12',fastcc('Q',spectra,detector='Q12',option=2)
print,'Q1',fastcc('Q',spectra,detector='Q1',option=2)
print,'Q21',fastcc('Q',spectra,detector='Q21',option=2)
print,'Q22',fastcc('Q',spectra,detector='Q22',option=2)
print,'Q2',fastcc('Q',spectra,detector='Q2',option=2)
print,'Q (40.6GHz)',fastcc('Q',spectra,option=2)

print,'V11',fastcc('V',spectra,detector='V11',option=2)
print,'V12',fastcc('V',spectra,detector='V12',option=2)
print,'V1',fastcc('V',spectra,detector='V1',option=2)
print,'V21',fastcc('V',spectra,detector='V21',option=2)
print,'V22',fastcc('V',spectra,detector='V22',option=2)
print,'V2',fastcc('V',spectra,detector='V2',option=2)
print,'V (60.8GHz)',fastcc('V',spectra,option=2)

print,'W11',fastcc('W',spectra,detector='W11',option=2)
print,'W12',fastcc('W',spectra,detector='W12',option=2)
print,'W1',fastcc('W',spectra,detector='W1',option=2)
print,'W21',fastcc('W',spectra,detector='W21',option=2)
print,'W22',fastcc('W',spectra,detector='W22',option=2)
print,'W2',fastcc('W',spectra,detector='W2',option=2)
print,'W31',fastcc('W',spectra,detector='W31',option=2)
print,'W32',fastcc('W',spectra,detector='W32',option=2)
print,'W3',fastcc('W',spectra,detector='W3',option=2)
print,'W41',fastcc('W',spectra,detector='W41',option=2)
print,'W42',fastcc('W',spectra,detector='W42',option=2)
print,'W4',fastcc('W',spectra,detector='W4',option=2)
print,'W (93.5GHz)',fastcc('W',spectra,option=2)

print,'QUIJOTE 2nd version. For 11, 13, 17, 19GHz combined maps, use 311, 313, 217, 219 respectively.'
print,'QUIJOTE 111 (11.2GHz)',fastcc('111',spectra,option=2)
print,'QUIJOTE 113 (12.8GHz)',fastcc('113',spectra,option=2)
print,'QUIJOTE 111 pol (11.2GHz)',fastcc('111p',spectra,option=2)
print,'QUIJOTE 113 pol (12.8GHz)',fastcc('113p',spectra,option=2)
print,'QUIJOTE 217 (16.7GHz)',fastcc('217',spectra,option=2)
print,'QUIJOTE 219 (18.7GHz)',fastcc('219',spectra,option=2)
print,'QUIJOTE 217 pol (16.7GHz)',fastcc('217p',spectra,option=2)
print,'QUIJOTE 219 pol (18.7GHz)',fastcc('219p',spectra,option=2)
print,'QUIJOTE 311 (11.1GHz)',fastcc('311',spectra,option=2)
print,'QUIJOTE 313 (12.9GHz)',fastcc('313',spectra,option=2)
print,'QUIJOTE 311 pol (11.1GHz)',fastcc('311p',spectra,option=2)
print,'QUIJOTE 313 pol (12.9GHz)',fastcc('313p',spectra,option=2)
print,'QUIJOTE 417 (17GHz)',fastcc('417',spectra,option=2)
print,'QUIJOTE 419 (19GHz)',fastcc('419',spectra,option=2)
print,'QUIJOTE 417 pol (17GHz)',fastcc('417p',spectra,option=2)
print,'QUIJOTE 419 pol (19GHz)',fastcc('419p',spectra,option=2)

print,'CBASS-N, 4.76GHz:'
print,"CBASS-N I1:", fastcc('CBASS', spectra,detector='CBASSNI1',option=2)
print,"CBASS-N Q1:", fastcc('CBASS', spectra,detector='CBASSNQ1',option=2)
print,"CBASS-N U1:", fastcc('CBASS', spectra,detector='CBASSNU1',option=2)
print,"CBASS-N Q2:", fastcc('CBASS', spectra,detector='CBASSNQ2',option=2)
print,"CBASS-N U2:", fastcc('CBASS', spectra,detector='CBASSNU2',option=2)
print,"CBASS-N I2:", fastcc('CBASS', spectra,detector='CBASSNI2',option=2)
print,"CBASS-N I:", fastcc('CBASSNI', spectra,option=2)
print,"CBASS-N Q:", fastcc('CBASSNQ', spectra,option=2)
print,"CBASS-N U:", fastcc('CBASSNU', spectra,option=2)

print,''
print,'2018 VERSION:'
print,'Detector	alpha',spectra
print,'LFI-18',fastcc('70',spectra,detector='18')
print,'LFI-19',fastcc('70',spectra,detector='19')
print,'LFI-20',fastcc('70',spectra,detector='20')
print,'LFI-21',fastcc('70',spectra,detector='21')
print,'LFI-22',fastcc('70',spectra,detector='22')
print,'LFI-23',fastcc('70',spectra,detector='23')
print,'LFI-18-23',fastcc('70',spectra,detector='1823')
print,'LFI-19-22',fastcc('70',spectra,detector='1922')
print,'LFI-20-21',fastcc('70',spectra,detector='2021')
print,'70GHz (70.4GHz)',fastcc('70',spectra)

print,'LFI-24',fastcc('44',spectra,detector='24')
print,'LFI-25',fastcc('44',spectra,detector='25')
print,'LFI-26',fastcc('44',spectra,detector='26')
print,'LFI-25-26',fastcc('44',spectra,detector='2526')
print,'44GHz (44.1GHz)',fastcc('44',spectra)

print,'LFI-27',fastcc('30',spectra,detector='27')
print,'LFI-28',fastcc('30',spectra,detector='28')
print,'30GHz (28.4GHz)',fastcc('30',spectra)

print,'100GHz',fastcc('100',spectra)
print,'143GHz',fastcc('143',spectra)
print,'217GHz',fastcc('217',spectra)
print,'353GHz',fastcc('353',spectra)
print,'545GHz',fastcc('545',spectra)
print,'857GHz',fastcc('857',spectra)

print,'WMAP'
print,'K11',fastcc('K',spectra,detector='K11')
print,'K12',fastcc('K',spectra,detector='K12')
print,'K1',fastcc('K',spectra,detector='K1')
print,'K (22.8GHz)',fastcc('K',spectra)

print,'Ka11',fastcc('Ka',spectra,detector='Ka11')
print,'Ka12',fastcc('Ka',spectra,detector='Ka12')
print,'Ka1',fastcc('Ka',spectra,detector='Ka1')
print,'Ka (33.0GHz)',fastcc('Ka',spectra)

print,'Q11',fastcc('Q',spectra,detector='Q11')
print,'Q12',fastcc('Q',spectra,detector='Q12')
print,'Q1',fastcc('Q',spectra,detector='Q1')
print,'Q21',fastcc('Q',spectra,detector='Q21')
print,'Q22',fastcc('Q',spectra,detector='Q22')
print,'Q2',fastcc('Q',spectra,detector='Q2')
print,'Q (40.6GHz)',fastcc('Q',spectra)

print,'V11',fastcc('V',spectra,detector='V11')
print,'V12',fastcc('V',spectra,detector='V12')
print,'V1',fastcc('V',spectra,detector='V1')
print,'V21',fastcc('V',spectra,detector='V21')
print,'V22',fastcc('V',spectra,detector='V22')
print,'V2',fastcc('V',spectra,detector='V2')
print,'V (60.8GHz)',fastcc('V',spectra)

print,'W11',fastcc('W',spectra,detector='W11')
print,'W12',fastcc('W',spectra,detector='W12')
print,'W1',fastcc('W',spectra,detector='W1')
print,'W21',fastcc('W',spectra,detector='W21')
print,'W22',fastcc('W',spectra,detector='W22')
print,'W2',fastcc('W',spectra,detector='W2')
print,'W31',fastcc('W',spectra,detector='W31')
print,'W32',fastcc('W',spectra,detector='W32')
print,'W3',fastcc('W',spectra,detector='W3')
print,'W41',fastcc('W',spectra,detector='W41')
print,'W42',fastcc('W',spectra,detector='W42')
print,'W4',fastcc('W',spectra,detector='W4')
print,'W (93.5GHz)',fastcc('W',spectra)

print,'QUIJOTE 2nd version. For 11, 13, 17, 19GHz combined maps, use 311, 313, 217, 219 respectively.'
print,'QUIJOTE 111 (11.2GHz)',fastcc('111',spectra)
print,'QUIJOTE 113 (12.8GHz)',fastcc('113',spectra)
print,'QUIJOTE 111 pol (11.2GHz)',fastcc('111p',spectra)
print,'QUIJOTE 113 pol (12.8GHz)',fastcc('113p',spectra)
print,'QUIJOTE 217 (16.7GHz)',fastcc('217',spectra)
print,'QUIJOTE 219 (18.7GHz)',fastcc('219',spectra)
print,'QUIJOTE 217 pol (16.7GHz)',fastcc('217p',spectra)
print,'QUIJOTE 219 pol (18.7GHz)',fastcc('219p',spectra)
print,'QUIJOTE 311 (11.1GHz)',fastcc('311',spectra)
print,'QUIJOTE 313 (12.9GHz)',fastcc('313',spectra)
print,'QUIJOTE 311 pol (11.1GHz)',fastcc('311p',spectra)
print,'QUIJOTE 313 pol (12.9GHz)',fastcc('313p',spectra)
print,'QUIJOTE 417 (17GHz)',fastcc('417',spectra)
print,'QUIJOTE 419 (19GHz)',fastcc('419',spectra)
print,'QUIJOTE 417 pol (17GHz)',fastcc('417p',spectra)
print,'QUIJOTE 419 pol (19GHz)',fastcc('419p',spectra)

print,'CBASS-N, 4.76GHz:'
print,"CBASS-N I1:", fastcc('CBASS', spectra,detector='CBASSNI1')
print,"CBASS-N Q1:", fastcc('CBASS', spectra,detector='CBASSNQ1')
print,"CBASS-N U1:", fastcc('CBASS', spectra,detector='CBASSNU1')
print,"CBASS-N Q2:", fastcc('CBASS', spectra,detector='CBASSNQ2')
print,"CBASS-N U2:", fastcc('CBASS', spectra,detector='CBASSNU2')
print,"CBASS-N I2:", fastcc('CBASS', spectra,detector='CBASSNI2')
print,"CBASS-N I:", fastcc('CBASSNI', spectra)
print,"CBASS-N Q:", fastcc('CBASSNQ', spectra)
print,"CBASS-N U:", fastcc('CBASSNU', spectra)


END