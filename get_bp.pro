FUNCTION get_bp, ihorn, DO_WRITE=do_write, NO_WEIGHT=no_weight
;
; reads an LFI bandpass into a structure, averaging diodes
; with appropriate weights. If requested, writes out diode-averaged bandpasses
; as FITS files.
;
; Cloned out of sm_preproc3.
;
; INPUTS
;     ihorn: LFI horn to analyse (18 to 28). 
;            If ihorn=0, analyses all horns; returned structure is for LFI-28
;                        (use only with /DO_WRITE)
;
; OPTIONAL INPUTS 
;     do_write: If set, writes out bandpass as a FITS file (one per horn).
;     no_weight: If set, diode weighting is turned off.
;
; RETURNS:
;     structure, with fields:
;          .hdr  : FITS-like header
;          .frequency: Frequencies for each gain value
;          .side_gain: Gain for side arm of the polarimeter (S-10 & S-11)
;          .main_gain: Gain for main arm of the polarimeter (M-00 & M-01)
;
; Input are Nov 2009 QUCS models
;
; Version 0.3 Remove incorrect scaling by detector gains (still reads in gains though!).

prog = 'GET_BP'
version = '0.3'
det  = ['M-00','M-01','S-10','S-11' ]
dir= 'C:\Users\Patrick Leahy\Documents\Research\Planck\bandpass\LFI_bandpasses_QUCS_20091109\'

bx = [0,0,0,0,0,0,1,1,1,2,2]
band = [70, 44, 30]

do_write = KEYWORD_SET(do_write)
no_weight = KEYWORD_SET(no_weight)
do_weight = ~no_weight

BP_HEADER, hdr0, hdr1, hist, prog, version

; Open gain & weight files & read headers
gainfile = dir + 'KRJ_per_Volt.txt'
readcol, gainfile, gammas, FORMAT='F'
IF N_ELEMENTS(gammas) NE 44 THEN MESSAGE, 'Wrong number of lines in gain file'

weightfile = dir + 'weights_march15_2010.txt'
readcol, weightfile, names, weights, FORMAT='A,F'

IF N_ELEMENTS(weights) NE 44 THEN MESSAGE, 'Wrong number of lines in weight file'

;weights /= gammas ; Removed in version 3: not needed as gains equalized by normalization

istart = ihorn EQ 0 ? 18 : ihorn
iend  =  ihorn EQ 0 ? 28 : ihorn

FOR ii=istart,iend DO BEGIN
    det0 = (ii-18)*4
    horn = STRING(ii,FORMAT="('LFI-',I2)")
    deta = STRING(ii,FORMAT="('LFI-',I2,'a')")
    detb = STRING(ii,FORMAT="('LFI-',I2,'b')")
    FOR j=0,3 DO BEGIN
        filename =  STRING(ii,band[bx[ii-18]],det[j], $
                           FORMAT="('LFI_RCA',I2,'_',I2,'GHz_',A4,'.dat')")
        PRINT, 'Reading '+filename
        struct = READ_ASCII(dir+filename, COUNT=nfreq)
        freq = REFORM(struct.field1[0,*])*1d9
        IF j EQ 0 THEN gain = DBLARR(nfreq-1,4)
        gain[j*(nfreq-1)] = REFORM(struct.field1[1,0:nfreq-2])
    ENDFOR
    nf_bp = N_ELEMENTS(freq)
    g00 = gain[*,0]
    g01 = gain[*,1]
    g10 = gain[*,2]
    g11 = gain[*,3]
    freqs = (freq[0:nf_bp-2] + freq[1:nf_bp-1])/2d9
    nf_bp -= 1
    
    IF no_weight THEN gav, freqs, g00, g01, g10, g11, nfreq, gmain, gside $
    ELSE BEGIN
      PRINT, 'Using weights for detectors:', names[det0:(det0+3)]
      PRINT, '                        ', weights[det0:(det0+3)]
      weight_gav, freqs, g00, g01, g10, g11, weights[det0:(det0+3)], nfreq, gmain, gside
    ENDELSE
    IF nfreq NE nf_bp THEN MESSAGE, 'Index mismatch'
    
    output = CREATE_STRUCT( 'HDR', hdr1, 'frequency', freqs, $
      'side_gain', gside, 'main_gain', gmain) 
    IF do_write THEN BEGIN
      heado = hdr0
      SXADDPAR, heado, 'DETECTOR', horn,' Planck horn name'
      SXADDHIST, hist, heado
      heado = [heado,'END         ']
      primo = CREATE_STRUCT('HDR', heado, 'DATA', 0) 
      filename = horn+'_response.fits'
      WRITE_FITS_SB, filename, primo, output, EXTENSION=0, /NOTHEALPIX
    ENDIF
ENDFOR

RETURN, output

END
