PRO COL_COR4, nametag, bp30, bp44, bp70, FID=dofid, NOWEIGHT=noweight, $
  TEX=dotex, PS=psfile, DOWRITE=dowrite
;
; Program to determine the spectral-index dependent color correction for
; Planck LFI bands. Cloned from plp_fig4.pro
;
; History for colour_cor3:
; Version 0.1 For DX4 (ERCSC) 28/10/10
; Version 0.1.1  Added horn pairs, tex formatting.
; Version 0.1.2  Added plotting  7/11/10
;
; based on 2009 QUCS bandpasses
;
; Col_cor4: removes scaling by gains (taken out by normalization?)
;           added weighting of pair and band colour corrections
;           corrected half-bin frequency offset
; Version 1.1  Inverted correct per 2013 convention (25 Jan 2013)
; Version 1.2  Added dowrite to write out horn pair band pass (30 Jul 2014)
; Version 1.4 Allow for irregular frequency spacing
; Version 1.5 Implemented LFI frequency shift (30/10/14)
; Version 1.5.1 Corrected accidental swapping of shift for 70 GHz ds2 & ds3
; Version 1.6 Implemented interpolation in frequency to combine horns/pairs with
;             different frequency shifts (12/3/15)
;
COMMON colour_cor_pars, multiplicative

prog = 'COL_COR4'
version = '1.6'
dofid    = KEYWORD_SET(dofid)
dotex    = KEYWORD_SET(dotex)
noweight = KEYWORD_SET(noweight)
tag = 'cc4v1.6'
IF N_ELEMENTS(nametag) GT 0 THEN tag = nametag
dowrite = KEYWORD_SET(dowrite)

IF dowrite THEN BP_HEADER, hdr0, hdr1, hist, prog, version, /PAIR

testing = 0
test_bp = 0
check_rimo = 0
do_radiometer = 0
multiplicative = 1 ; True if corrected = cc*raw; false if corrected = raw/cc

rimofile = 'C:\Users\Patrick Leahy\Documents\Data\lfi\LFI_RIMO_18092012_DX9d.fits'
READ_FITS_S, rimofile,primary,rimo
vars = rimo.net^2/rimo.f_samp ; white noise variance

dir = 'C:\Users\Patrick Leahy\Documents\Research\Planck\bandpass\LFI_bandpasses_QUCS_20091109\'
band = ['70','44','30']
nhorn = [6,3,2]
horn0 = [18,24,27]

; Identify which horns are paired up
npair = (nhorn+1)/2  ; integer divide!

pair   = [intarr(17),0,1,2,2,1,0,0,1,1,0,0]
second = [intarr(17),0,0,0,1,1,1,0,0,1,0,1]
pairname = [replicate('',MAX(npair))]

nomfreq = [70.0, 44.0, 30.0] ; GHz
reffreq = [70.4d, 44.1d, 28.4d]; [70.3, 44.1, 28.5] ; [70.32400, 44.09885, 28.45733] ; GHz
fidfreq = [69.4907, 43.7650, 28.0613]; [69.54, 43.81, 28.11] ; GHz
IF dofid THEN reffreq = fidfreq

; Bandpass shifts from Commander (Paper A12 draft) for each horn, 18-28

shift =[-0.44, 1.07, 0.48, 0.48, 1.07, -0.44, 0.10, 0.10, 0.10, 0.29, 0.29]
;shift = REPLICATE(0.0, 11)

T0 = 2.7255d  ; (K): CMB temperature
pob = 0.04799237 ; (K/GHz) Ratio of Planck to Boltzmann constant

; Set up array of beta values:
alpha = [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
range = MINMAX(alpha)
beta =  alpha - 2.0
nbeta = N_ELEMENTS(beta)
cc = FLTARR(nbeta)

IF ~test_bp THEN BEGIN
; Open gain & weight files & read headers
gainfile = dir + 'KRJ_per_Volt.txt'
readcol, gainfile, gammas, FORMAT='F'
IF N_ELEMENTS(gammas) NE 44 THEN MESSAGE, 'Wrong number of lines in gain file'

weightfile = dir + 'weights_march15_2010.txt'
wt = read_ascii(weightfile, temp = ascii_template(weightfile))
names = wt.field1
weights = wt.field2
IF N_ELEMENTS(weights) NE 44 THEN MESSAGE, 'Wrong number of lines in weight file'

; check:
;fudge = REFORM(TRANSPOSE([[REPLICATE(1,22)],[REPLICATE(0.9,22)]]),44)
;weights /= (gammas*fudge)

; weights /= gammas
ENDIF

; Set up output file
ofile = dir + 'LFI_colour_corrections_pairs' $
        + (dofid ? '_alt' : '') + (noweight ? '_unw' : '') + '_' + tag + (dotex ? '.tex': '.txt')

OPENW, olun, ofile, /GET_LUN
PRINTF, olun, '% Colour corrections for LFI'
PRINTF, olun, '% Written by '+prog+' version '+version

IF multiplicative THEN PRINTF, olun, '% Corrected value = cc x raw value'
PRINTF, olun, reffreq, $
  FORMAT="('% Referenced to ',3F6.2,' GHz in the three bands')"
PRINTF, olun, ''
PRINTF, olun, 'Detector                           Alpha'

fmt = dotex ? '(A14,' + STRING(nbeta, FORMAT = "(I2)") + '(" & $",F7.3,"$"), " \\")' : $
              '(A14,' + STRING(nbeta, FORMAT = "(I2)") + 'F7.3)'
PRINTF, olun, '', alpha, FORMAT = fmt
PRINTF, olun, ''

!X.thick = 3
!Y.thick = 3
!P.charthick = 3
!P.thick = 3

jj = 0
FOR iband = 0,2 DO BEGIN
  ih1 = horn0[iband]
  first = 1
  dlab = 0.0
  varwgt_band = 0d0
  bandname = STRING(band[iband], FORMAT="(I2,' GHz')")
  pairname[*] = ''
  IF KEYWORD_SET(psfile) THEN simple_colour, PS=dir+psfile+'_'+bandname+'.eps'
  !P.color = 13
  !P.linestyle = 0
  PLOT, [0,0], [-0.05,0.15], xstyle=1, ystyle=1, $
  xtitle='!3Spectral index !4a', ytitle='!3Gain error f(!4a,m!D!30!N)', $
  xrange=range, subtitle = STRING(reffreq[iband],FORMAT="('!4m!D!30!N = ',F5.2,' GHz')")
  ;  yrange=[-0.02,0.07]
  OPLOT, range, [0,0]
 
  FOR jhorn = 0, nhorn[iband]-1 DO BEGIN
    jj += 1
    det = (jj-1)*4
    !P.color = jhorn+1
    MESSAGE, /INFORMATIONAL, 'Processing ' + rimo.detector[2*jj-2] + ', ' + rimo.detector[2*jj-1]
    var_horn = (vars[2*jj-2] + vars[2*jj-1]) 
  ; Read data for each horn
    ihorn = ih1+jhorn
    hs = STRING(ihorn, FORMAT='(I2)')
    name = 'LFI-'+hs
    IF test_bp THEN BEGIN
      bp = get_bp(ihorn, NO_WEIGHT=noweight)
      gside = bp.side_gain
      gmain = bp.main_gain
      freq  = bp.frequency
      nfreq = N_ELEMENTS(freq)
    ENDIF ELSE BEGIN
      fileroot =   dir + 'LFI_RCA' + hs + '_'+band[iband]+'GHz_'
      print, 'Reading '+fileroot
      readcol, fileroot+'M-00.dat', freq00, g00, FORMAT = 'F', /SILENT
      readcol, fileroot+'M-01.dat', freq01, g01, FORMAT = 'F', /SILENT
      readcol, fileroot+'S-10.dat', freq10, g10, FORMAT = 'F', /SILENT
      readcol, fileroot+'S-11.dat', freq11, g11, FORMAT = 'F', /SILENT
      IF ~ARRAY_EQUAL(freq00,freq01) || ~ARRAY_EQUAL(freq10,freq11) $
        || ~ ARRAY_EQUAL(freq00,freq10) THEN MESSAGE, fileroot+': mismatched frequency arrays'

      nfreq = N_ELEMENTS(freq00)
      IF g00[nfreq-1] NE 0.0 OR g01[nfreq-1] NE 0.0 OR $
         g10[nfreq-1] NE 0.0 OR g11[nfreq-1] NE 0.0 THEN MESSAGE, 'Last gain value should be zero'
      freq = 0.5d0*(freq00[1:nfreq-1] + freq00[0:nfreq-2])
      nfreq = nfreq - 1
      g00 = g00[0:nfreq-1]
      g01 = g01[0:nfreq-1]
      g10 = g10[0:nfreq-1]
      g11 = g11[0:nfreq-1]
      PRINT, 'Processing '+name, names[det:(det+3)]

; Normalize bands to equal CMB power and take straight average of detectors:
      IF noweight THEN gav, freq, g00, g01, g10, g11, nfreq, gmain, gside $
      ELSE weight_gav, freq, g00, g01, g10, g11, weights[det:(det+3)], nfreq, gmain, gside
    ENDELSE
;
;  Set up high-resolution frequency scale
;
    frange = MINMAX(freq)
    f0 = frange[0]
    f1 = frange[1]
    freqstep = (f1-f0)/(nfreq-1)
    frange[0] -= 1.5    ; Extend frequency range by 1.5 GHz at each end
    frange[1] += 1.5
    nfine = FIX(4*(frange[1]-frange[0])/freqstep)
    finefreq = frange[0] + findgen(nfine)*freqstep/4
    fmod = [f0-2*freqstep,f0-freqstep, freq, f1+freqstep,f1+2*freqstep] + shift[ihorn-18]
    gmain = [0,0,gmain,0,0]
    gside = [0,0,gside,0,0]
    finegmain = INTERPOL(gmain, fmod, finefreq)
    finegside = INTERPOL(gside, fmod, finefreq)

; Check
    IF testing THEN BEGIN
     t1 = getcc(fmod, gmain, reffreq[iband], beta, 1)
     t2 = getcc(finefreq, finegmain, reffreq[iband], beta, 1)
     t3 = getcc(fmod, gside, reffreq[iband], beta, 1)
     t4 = getcc(finefreq, finegside, reffreq[iband], beta, 1)

     PRINT, 'Testing interpolated corrections:'
     PRINT, 'Side arm shifted:    :', t3
     PRINT, 'Side arm interpolated:', t4
     PRINT, 'Main arm shifted:    :', t1
     PRINT, 'Main arm interpolated:', t2
     STOP
    ENDIF
    freq = finefreq
    gmain = finegmain
    gside = finegside
    nfreq = N_ELEMENTS(freq)
    
    IF check_rimo THEN BEGIN
      n_ext = 2+2*(28-ihorn)
      read_fits_s, rimofile, primary, rimo_bp, EXTENSION=n_ext
      PRINT, 'Using ', SXPAR(rimo_bp.hdr,'EXTNAME')
      nn = N_ELEMENTS(rimo_bp.transmission)
      PRINT, 'Number of elements in transmission array:', nn
      df = rimo_bp.wavenumber[1:*] - rimo_bp.wavenumber[0:nn-2]
;      df = (rimo_bp.wavenumber[nn-1]-rimo_bp.wavenumber[0])/(nn-1)
      ff = rimo_bp.wavenumber[0:nn-2] + df/2d
      gside = rimo_bp.transmission[0:nn-2]
      cmbpower = TOTAL(gside*df*etadt(ff),/DOUBLE)
      norm = 1d/cmbpower
      PRINT, 'Rescaling by', norm 
      gside *= norm
      read_fits_s, rimofile, primary, rimo_bp, EXTENSION=n_ext+1
      PRINT, 'Using ', SXPAR(rimo_bp.hdr,'EXTNAME')
      nn = N_ELEMENTS(rimo_bp.transmission)
      PRINT, 'Number of elements in transmission array:', nn
      df = rimo_bp.wavenumber[1:*] - rimo_bp.wavenumber[0:nn-2]
;      df = (rimo_bp.wavenumber[nn-1]-rimo_bp.wavenumber[0])/(nn-1)
      ff = rimo_bp.wavenumber[0:nn-2] + df/2d
      gmain = rimo_bp.transmission[0:nn-2]
      cmbpower = TOTAL(gmain*df*etadt(ff),/DOUBLE)
      norm =1d/cmbpower
      PRINT, 'Rescaling by', norm
      gmain *= norm
    ENDIF
; Unweighted average of arms
    gain = 0.5*(gside + gmain)
    IF N_ELEMENTS(gain) LT 2 THEN MESSAGE, 'Lost gain array!'
  
    IF do_radiometer THEN BEGIN
      cc_m = getcc(freq, gmain, reffreq[iband], beta, 1)
      cc_s = getcc(freq, gside, reffreq[iband], beta, 1)
      PRINTF, olun, name+'M', cc_m, FORMAT = fmt
      PRINTF, olun, name+'S', cc_s, FORMAT = fmt 
    ENDIF
    cc = getcc(freq, gain, reffreq[iband], beta, 1)
    XYOUTS, 0.13+dlab, 0.96, name, /NORMAL, width = doff
    dlab +=1.2*doff

    PRINTF, olun, name, cc, FORMAT = fmt

    IF first THEN BEGIN
       bandgain = gain / var_horn
       pairgain = DBLARR(N_ELEMENTS(gain),npair[iband])
       pairwgt =  DBLARR(npair[iband])
       pairfreq = DBLARR(N_ELEMENTS(freq),npair[iband])
    ENDIF ELSE bandgain += gain / var_horn
    
    pairname[pair[ihorn-1]] += name 
    pairgain[*,pair[ihorn-1]] += gain / var_horn
    varwgt_band += 1d0 / var_horn
    pairwgt(pair[ihorn-1]) += 1d0 / var_horn
    IF NOT second[ihorn-1] THEN pairname[pair[ihorn-1]] += '_'
    IF NOT second[ihorn-1] THEN pairfreq[*,pair[ihorn-1]] = freq
    first = 0
  ENDFOR ; End loop over horns in each band
      
  PRINTF, olun, ''
   ; Work out cc for horn pairs
  FOR jhorn = nhorn[iband]-1,0,-1 DO BEGIN
    ihorn = ih1+jhorn
    IF second[ihorn-1] THEN BEGIN
      !P.color += 1
      !p.linestyle = 3
      gain = pairgain[*,pair[ihorn-1]]/pairwgt[pair[ihorn-1]]
      freq = pairfreq[*,pair[ihorn-1]]
      IF dowrite THEN BEGIN
         output = CREATE_STRUCT( 'HDR', hdr1, 'frequency', freq, $
         'gain', gain)
         heado = hdr0
         SXADDPAR, heado, 'HORN_PAIR', pairname[pair[ihorn-1]],' Planck horn pair'
         SXADDHIST, hist, heado
         heado = [heado,'END         ']
         primo = CREATE_STRUCT('HDR', heado, 'DATA', 0)
         filename = pairname[pair[ihorn-1]]+'_response.fits'
         WRITE_FITS_SB, filename, primo, output, EXTENSION=0, /NOTHEALPIX
      ENDIF
      cc = getcc(freq, gain, reffreq[iband], beta, 1)
      !p.linestyle = 0
      XYOUTS, 0.13+dlab, 0.96, pairname[pair[ihorn-1]], /NORMAL, width = doff
      dlab +=1.2*doff
      PRINTF, olun, pairname[pair[ihorn-1]], cc, FORMAT = fmt
      pairname[pair[ihorn-1]] = ''
    ENDIF
  ENDFOR
  
  !P.LINESTYLE = 3
  !P.color = 13
  bandgain /= varwgt_band
  PRINTF, olun, ''
  IF (check_rimo) THEN BEGIN
     n_ext = 2+22+(2-iband)
     read_fits_s, rimofile, primary, rimo_bp, EXTENSION=n_ext
     PRINT, 'Using', SXPAR(rimo_bp.hdr,'EXTNAME')
     nn = N_ELEMENTS(rimo_bp.transmission)
     PRINT, 'Number of elements in transmission array:', nn
     rimo_gain = rimo_bp.transmission[0:nn-2]
     df = (rimo_bp.wavenumber[nn-1] - rimo_bp.wavenumber[0])/(nn-1)
     rimo_freq = rimo_bp.wavenumber + df/2
     ccr = getcc(rimo_freq,rimo_gain,reffreq[iband], beta, 1)
     PRINTF, olun, bandname+' RIMO', ccr, FORMAT=fmt
  ENDIF
  
  struct = CREATE_STRUCT('FREQUENCY', freq, 'GAIN', bandgain)
  CASE iband OF
    0: bp70 = struct
    1: bp44 = struct
    2: bp30 = struct
  ENDCASE
  IF dowrite THEN BEGIN
    output = CREATE_STRUCT( 'HDR', hdr1, 'frequency', freq, $
      'gain', bandgain)
    heado = hdr0
    SXADDPAR, heado, 'BAND', bandname,' Planck frequncy band'
    SXADDHIST, hist, heado
    heado = [heado,'END         ']
    primo = CREATE_STRUCT('HDR', heado, 'DATA', 0)
    filename = bandname+'_response.fits'
    WRITE_FITS_SB, filename, primo, output, EXTENSION=0, /NOTHEALPIX
  ENDIF
  cc = getcc(freq, bandgain, reffreq[iband], beta, 1)
  PRINTF, olun, bandname, cc, FORMAT = fmt
  PRINTF, olun, ''
  
  IF iband lt 2 THEN BEGIN
    PRINT, 'Press return for next band'
    junk = ''
    READ, junk
  ENDIF
  IF KEYWORD_SET(psfile) THEN DEVICE, /CLOSE
ENDFOR  ; End loop over bands

CLOSE, /ALL
!X.thick = 1
!Y.thick = 1
!P.charthick = 1
!P.thick = 1
!P.linestyle = 0
simple_colour
END