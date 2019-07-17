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

PRO fastcc_test

spectra = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

print,'2013 VERSION:'
print,'Detector	alpha',spectra
print,'LFI-18',fastcc('70',spectra,detector='18')
print,'LFI-19',fastcc('70',spectra,detector='19')
print,'LFI-20',fastcc('70',spectra,detector='20')
print,'LFI-21',fastcc('70',spectra,detector='21')
print,'LFI-22',fastcc('70',spectra,detector='22')
print,'LFI-23',fastcc('70',spectra,detector='23')
print,'70GHz',fastcc('70',spectra)

print,'LFI-24',fastcc('44',spectra,detector='24')
print,'LFI-25',fastcc('44',spectra,detector='25')
print,'LFI-26',fastcc('44',spectra,detector='26')
print,'44GHz',fastcc('44',spectra)

print,'LFI-27',fastcc('30',spectra,detector='27')
print,'LFI-28',fastcc('30',spectra,detector='28')
print,'30GHz',fastcc('30',spectra)

print,'WMAP'
;print,'K11',fastcc('K',spectra,detector='K11')
;print,'K12',fastcc('K',spectra,detector='K12')
;print,'K1',fastcc('K',spectra,detector='K1')
print,'K',fastcc('K',spectra)

;print,'Ka11',fastcc('Ka',spectra,detector='Ka11')
;print,'Ka12',fastcc('Ka',spectra,detector='Ka12')
;print,'Ka1',fastcc('Ka',spectra,detector='Ka1')
print,'Ka',fastcc('Ka',spectra)

;print,'Q11',fastcc('Q',spectra,detector='Q11')
;print,'Q12',fastcc('Q',spectra,detector='Q12')
;print,'Q1',fastcc('Q',spectra,detector='Q1')
;print,'Q21',fastcc('Q',spectra,detector='Q21')
;print,'Q22',fastcc('Q',spectra,detector='Q22')
;print,'Q2',fastcc('Q',spectra,detector='Q2')
print,'Q',fastcc('Q',spectra)

;print,'V11',fastcc('V',spectra,detector='V11')
;print,'V12',fastcc('V',spectra,detector='V12')
;print,'V1',fastcc('V',spectra,detector='V1')
;print,'V21',fastcc('V',spectra,detector='V21')
;print,'V22',fastcc('V',spectra,detector='V22')
;print,'V2',fastcc('V',spectra,detector='V2')
print,'V',fastcc('V',spectra)

;print,'W11',fastcc('W',spectra,detector='W11')
;print,'W12',fastcc('W',spectra,detector='W12')
;print,'W1',fastcc('W',spectra,detector='W1')
;print,'W21',fastcc('W',spectra,detector='W21')
;print,'W22',fastcc('W',spectra,detector='W22')
;print,'W2',fastcc('W',spectra,detector='W2')
;print,'W31',fastcc('W',spectra,detector='W31')
;print,'W32',fastcc('W',spectra,detector='W32')
;print,'W3',fastcc('W',spectra,detector='W3')
;print,'W41',fastcc('W',spectra,detector='W41')
;print,'W42',fastcc('W',spectra,detector='W42')
;print,'W4',fastcc('W',spectra,detector='W4')
print,'W',fastcc('W',spectra)

print,'LATEST VERSION:'
print,'Detector	alpha',spectra
print,'LFI-18',fastcc('70',spectra,detector='18',/latest)
print,'LFI-19',fastcc('70',spectra,detector='19',/latest)
print,'LFI-20',fastcc('70',spectra,detector='20',/latest)
print,'LFI-21',fastcc('70',spectra,detector='21',/latest)
print,'LFI-22',fastcc('70',spectra,detector='22',/latest)
print,'LFI-23',fastcc('70',spectra,detector='23',/latest)
print,'LFI-18-23',fastcc('70',spectra,detector='1823',/latest)
print,'LFI-19-22',fastcc('70',spectra,detector='1922',/latest)
print,'LFI-20-21',fastcc('70',spectra,detector='2021',/latest)
print,'70GHz',fastcc('70',spectra,/latest)

print,'LFI-24',fastcc('44',spectra,detector='24',/latest)
print,'LFI-25',fastcc('44',spectra,detector='25',/latest)
print,'LFI-26',fastcc('44',spectra,detector='26',/latest)
print,'LFI-25-26',fastcc('44',spectra,detector='2526',/latest)
print,'44GHz',fastcc('44',spectra,/latest)

print,'LFI-27',fastcc('30',spectra,detector='27',/latest)
print,'LFI-28',fastcc('30',spectra,detector='28',/latest)
print,'30GHz',fastcc('30',spectra,/latest)

print,'WMAP'
print,'K11',fastcc('K',spectra,detector='K11',/latest)
print,'K12',fastcc('K',spectra,detector='K12',/latest)
print,'K1',fastcc('K',spectra,detector='K1',/latest)
print,'K',fastcc('K',spectra,/latest)

print,'Ka11',fastcc('Ka',spectra,detector='Ka11',/latest)
print,'Ka12',fastcc('Ka',spectra,detector='Ka12',/latest)
print,'Ka1',fastcc('Ka',spectra,detector='Ka1',/latest)
print,'Ka',fastcc('Ka',spectra,/latest)

print,'Q11',fastcc('Q',spectra,detector='Q11',/latest)
print,'Q12',fastcc('Q',spectra,detector='Q12',/latest)
print,'Q1',fastcc('Q',spectra,detector='Q1',/latest)
print,'Q21',fastcc('Q',spectra,detector='Q21',/latest)
print,'Q22',fastcc('Q',spectra,detector='Q22',/latest)
print,'Q2',fastcc('Q',spectra,detector='Q2',/latest)
print,'Q',fastcc('Q',spectra,/latest)

print,'V11',fastcc('V',spectra,detector='V11',/latest)
print,'V12',fastcc('V',spectra,detector='V12',/latest)
print,'V1',fastcc('V',spectra,detector='V1',/latest)
print,'V21',fastcc('V',spectra,detector='V21',/latest)
print,'V22',fastcc('V',spectra,detector='V22',/latest)
print,'V2',fastcc('V',spectra,detector='V2',/latest)
print,'V',fastcc('V',spectra,/latest)

print,'W11',fastcc('W',spectra,detector='W11',/latest)
print,'W12',fastcc('W',spectra,detector='W12',/latest)
print,'W1',fastcc('W',spectra,detector='W1',/latest)
print,'W21',fastcc('W',spectra,detector='W21',/latest)
print,'W22',fastcc('W',spectra,detector='W22',/latest)
print,'W2',fastcc('W',spectra,detector='W2',/latest)
print,'W31',fastcc('W',spectra,detector='W31',/latest)
print,'W32',fastcc('W',spectra,detector='W32',/latest)
print,'W3',fastcc('W',spectra,detector='W3',/latest)
print,'W41',fastcc('W',spectra,detector='W41',/latest)
print,'W42',fastcc('W',spectra,detector='W42',/latest)
print,'W4',fastcc('W',spectra,detector='W4',/latest)
print,'W',fastcc('W',spectra,/latest)

print,'MFI 111',fastcc('111',spectra,/latest)
print,'MFI 113',fastcc('113',spectra,/latest)
print,'MFI 217',fastcc('217',spectra,/latest)
print,'MFI 219',fastcc('219',spectra,/latest)
print,'MFI 311',fastcc('311',spectra,/latest)
print,'MFI 313',fastcc('313',spectra,/latest)
print,'MFI 417',fastcc('417',spectra,/latest)
print,'MFI 419',fastcc('419',spectra,/latest)


END