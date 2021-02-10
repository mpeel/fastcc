FUNCTION fastcc, freq, alpha, td=td, bd=bd, detector=detector,debug=debug,option=option, returnfreq=returnfreq
    ; Apply colour corrections to Planck LFI and WMAP data
    ; freq should be one of 30, 44, 70, K, Ka, Q, V or W, as a string.
    ; Actual frequencies are 28.4, 44.1 or 70.4 for LFI; 22.80 33.00 40.60 60.80 93.50 for WMAP
    ; detector (optional) should be between '18' and '28' inclusive for LFI, as a string; they should of the style 'K11', 'K12', 'K1' for WMAP.
    ; set 'debug' to see debug messages
    ; set 'option=2' to use the 2015 WMAP and Planck numbers (default), otherwise set to '1' use the WMAP9 and Planck 2013 values. DEFAULT is 2
    ; 
    ; Version history:
    ; Mike Peel   01-Feb-2013   v1.0 Initial version
    ; Mike Peel   04-Feb-2013   v1.1 Correct convention
    ; Locke Spencer 05-Feb-2013:  v1.2 Changed name to LFI_fastCC from planckcc (it only works for LFI)
    ;                             Changed nested IF..ELSE groups to case statements
    ;                             Changed invalid detector/frequency output to zero and removed internal stop in the code.
    ; Mike Peel   24-Jul-2014   v2.0 Added WMAP (based on values from Paddy Leahy), renamed to fastcc. Note that function calls from v1 won't work with v2 without modification.
    ; Mike Peel   13-Aug-2014   v2.1 Updated WMAP colour corrections, taking into account frequency drift during the mission (values from Paddy Leahy).
    ; Mike Peel   06-Nov-2014   v2.2 Added 'dev' parameter (updated LFI and WMAP numbers from Paddy Leahy, including LFI bandpass shifts);
    ;                                without this parameter the published values for LFI and WMAP will be returned.
    ; Mike Peel   12-Mar-2015   v2.3 Update 70GHz values to fits to corrected colour corrections from Paddy Leahy
    ; Mike Peel   23-Mar-2015   v2.4 Update WMAP colour corrections to corrected values from Paddy Leahy.
    ; Mike Peel   17-Jul-2019   v2.6 Change 'dev' to 'latest', add initial QUIJOTE MFI points
    ; Mike Peel   17-Jul-2019   v2.6a Revised QUIJOTE MFI points
    ; Mike Peel   18-Jul-2019   v2.7 Adding CBASS
    ; Mike Peel   06-Oct-2020   v2.8 New QUIJOTE numbers
    ; Mike Peel   16-Nov-2020   v2.9 BREAKING CHANGE, 'latest' is now 'option'. HFI added.
    ; Mike Peel   22-Jan-2020   v3.0 BREAKING CHANGE, frequency/detector labels now have prefixes. Upgrading to return frequencies and to prepare for colour corrections for thermal dust models for Planck HFI (not added in this version). Updated numbers for MFI, HFI, C-BASS.

wmap=0 ; Flag used later to determine which formula to use.
IF (~keyword_set(option)) THEN BEGIN
  option = 3
ENDIF

IF (option EQ 3) THEN BEGIN ; 2018 version (mostly the same as 2015)
 IF (keyword_set(detector)) THEN BEGIN
   IF (keyword_set(debug)) THEN print,'Using detector ',detector
   CASE detector OF
    'P18': cc = [0.977484, 0.0185055, -0.00391209, 70.4]
    'P19': cc = [0.965314, 0.0234026, -0.00256943, 70.4]
    'P20': cc = [0.968436, 0.0220869, -0.00285115, 70.4]
    'P21': cc = [0.982854, 0.0142877, -0.00317682, 70.4]
    'P22': cc = [1.049, -0.0237173, -0.00288312, 70.4]
    'P23': cc = [0.990172, 0.0091968, -0.00238961, 70.4]
    'P1823': cc = [0.983195, 0.0141778, -0.00317682, 70.4]
    'P1922': cc = [1.00978, -0.000698302, -0.00328272, 70.4]
    'P2021': cc = [0.97712, 0.0175904, -0.00308092, 70.4]
    'P24': cc = [0.999958, 0.00309391, -0.00177223, 44.1]
    'P25': cc = [0.994381, 0.00591109, -0.00162038, 44.1]
    'P26': cc = [0.990046, 0.00854446, -0.00177223, 44.1]
    'P2526': cc = [0.992115, 0.00717982, -0.00167233, 44.1]
    'P27': cc = [1.00503, 0.00276424, -0.00282717, 28.4]
    'P28': cc = [1.00491, 0.00334266, -0.00313287, 28.4]
    'WK11': cc = [0.939366, 0.0346715, -0.00214346, 22.8]
    'WK12': cc = [1.00894, 0.000982418, -0.00276923, 22.8]
    'WK1': cc = [0.972902, 0.0190469, -0.00276464, 22.8]
    'WKa11': cc = [0.974784, 0.0159578, -0.00161958, 33.0]
    'WKa12': cc = [0.992978, 0.00737502, -0.00200839, 33.0]
    'WKa1': cc = [0.983787, 0.0117567, -0.00183716, 33.0]
    'WQ11': cc = [0.990948, 0.00846474, -0.00204555, 40.6]
    'WQ12': cc = [0.998159, 0.00404356, -0.00167233, 40.6]
    'WQ1': cc = [0.994548, 0.00627672, -0.00186693, 40.6]
    'WQ21': cc = [0.981607, 0.0126181, -0.00166893, 40.6]
    'WQ22': cc = [1.01705, -0.00573297, -0.0016989, 40.6]
    'WQ2': cc = [0.998986, 0.00378172, -0.00176723, 40.6]
    'WV11': cc = [0.939474, 0.0354285, -0.00155105, 60.8]
    'WV12': cc = [0.994737, 0.006396, -0.00217822, 60.8]
    'WV1': cc = [0.966309, 0.0217416, -0.00209331, 60.8]
    'WV21': cc = [1.00662, -0.000113686, -0.00217942, 60.8]
    'WV22': cc = [0.977227, 0.0160255, -0.00220999, 60.8]
    'WV2': cc = [0.991701, 0.0082012, -0.00226214, 60.8]
    'WW11': cc = [0.988343, 0.00956424, -0.00211948, 93.5]
    'WW12': cc = [0.9838, 0.0120015, -0.00173207, 93.5]
    'WW1': cc = [0.986087, 0.0107974, -0.00193167, 93.5]
    'WW21': cc = [0.978714, 0.0149705, -0.00148032, 93.5]
    'WW22': cc = [0.992004, 0.00655744, -0.00146334, 93.5]
    'WW2': cc = [0.985324, 0.0108262, -0.00149331, 93.5]
    'WW31': cc = [0.977457, 0.0155997, -0.00131688, 93.5]
    'WW32': cc = [0.993636, 0.0054001, -0.00134126, 93.5]
    'WW3': cc = [0.985473, 0.0105855, -0.00135485, 93.5]
    'WW41': cc = [0.991452, 0.0072962, -0.00181239, 93.5]
    'WW42': cc = [0.973071, 0.0185705, -0.00153746, 93.5]
    'WW4': cc = [0.982185, 0.0130277, -0.00170889, 93.5]
   ELSE: BEGIN
     print,'Invalid detector specified for fastcc, returning zero.'
     return, 0d
   ENDELSE
   ENDCASE
 ENDIF ELSE BEGIN ; individual frequencies
   IF (keyword_set(debug)) THEN print,'Using frequency ',freq
   CASE freq OF
     'CBASSNI': cc = [1.000103213196618, -0.0007238230723748647, -0.0013363809246677324, 4.76]
     'CBASSNP': cc = [0.998561438218094, -0.0059052869678747595, -0.001680320871507042, 4.76]
     'Q111': cc = [0.9925526276311687, 0.007161407883127753, -0.0017891332783659003, 11.2]
     'Q113': cc = [0.9949649181723395, 0.005394042720463821, -0.0014382949498306515, 12.8]
     'Q111p': cc = [0.9925526276311687, 0.007161407883127753, -0.0017891332783659003, 11.2]
     'Q113p': cc = [0.9949649181723395, 0.005394042720463821, -0.0014382949498306515, 12.8]
     'Q217': cc = [1.0129709167366905, -0.005101169068593444, -0.000683203301567257, 16.7]
     'Q219': cc = [1.0175292512259428, -0.007544762181222079, -0.0006248503973819523, 18.7]
     'Q217p': cc = [1.0165157773037472, -0.006419637626097819, -0.000927550610591879, 16.7]
     'Q219p': cc = [1.0136255722145442, -0.004544629474433171, -0.0010878048910708117, 18.7]
     'Q311': cc = [0.9820571573496972, 0.011947716397192746, -0.0015316600265756597, 11.1]
     'Q313': cc = [1.002376171424373, 0.00087053237460555, -0.0010541678118863593, 12.9]
     'Q311p': cc = [0.9843034690253142, 0.011094990021336104, -0.0016791051042741416, 11.1]
     'Q313p': cc = [0.9958959030027292, 0.0051175051270606255, -0.0014905894344412235, 12.9]
     'Q417': cc = [0.9888926591458963, 0.006986281593109233, -0.0007107060258669477, 17.0]
     'Q419': cc = [0.9886433438856964, 0.007541246196285672, -0.0009156379893644272, 19.0]
     'Q417p': cc = [1.0029823815141663, 0.0008640490621996672, -0.0012140291472187072, 17.0]
     'Q419p': cc = [0.9843617866675408, 0.010330165097893152, -0.0012211561793953436, 19.0]
     'P30': cc = [1.00513, 0.00301399, -0.00300699, 28.4]
     'P44': cc = [0.994769, 0.00596703, -0.00173626, 44.1]
     'P70': cc = [0.989711, 0.0106943, -0.00328671, 70.4]
     'P100': cc = [0.9960219846097942, -0.00654302733954478, -0.00416413824546881, 100.0]
     'P143': cc = [1.0111101391244646, 0.006818336941786147, -0.0043482778766929025, 143.0]
     'P217': cc = [0.9874219751512573, -0.013958018248228142, -0.003712910348781007, 217.0]
     'P353': cc = [0.9855790668991027, -0.015716578392508118, -0.0032909215453657656, 353.0]
     'P545': cc = [0.9857797576167087, -0.01455866885981098, -0.0041925161876140765, 545.0]
     'P857': cc = [1.0026826793529224, 0.0007381414746500997, -0.004248209090549633, 857.0]
     'WK' : cc = [0.972902, 0.0190469, -0.00276464, 22.8]
     'WKa': cc = [0.983787, 0.0117567, -0.00183716, 33.0]
     'WQ' : cc = [0.996854, 0.00496893, -0.00181359, 40.6]
     'WV' : cc = [0.980322, 0.0143631, -0.00223596, 60.8]
     'WW' : cc = [0.984848, 0.0112743, -0.00164595, 93.5]
     'DB10': cc = [1.0056317,   -0.0052173,   -0.0119257, 1249]
     'DB9': cc = [1.0347912,    0.0245728,   -0.0095350, 2141]
     'DB8': cc = [0.9593942,   -0.0469581,   -0.0075185, 2997]
     'DB7': cc = [0.9079217,   -0.0942761,   -0.0068850, 4995]
     'DB6': cc = [0.8160551,   -0.1717965,    0.0103011, 11988]
     'DB5': cc = [0.9816717,   -0.0327394,   -0.0178211, 24975]
     'DB4': cc = [0.9947178,   -0.0060948,   -0.0008378, 61163]
     'DB3': cc = [1.0030533,   -0.0001524,   -0.0032236, 85629]
     'DB2': cc = [1.0064020,    0.0050962,   -0.0012763, 136227]
     'DB1': cc = [1.0073260,    0.0044317,   -0.0028791, 239760]
     'I100': cc = [0.9899184805240909, -0.01970072476335274, -0.007706943391147654, 2997]
     'I60': cc = [0.9510100573154361, -0.06111819772388552, -0.016457316462171055, 4995]
     'I25': cc = [0.9123700815757735, -0.08972760549528734, -0.0056369170040417305, 11988]
     'I12': cc = [0.9083422603187424, -0.09300485963152248, -0.008759896726856715, 24975]
     ELSE: BEGIN
       print,'Invalid frequency specified for fastcc, returning zero.'
       return, 0d
      ENDELSE
   ENDCASE
 ENDELSE
 ENDIF ELSE IF (option EQ 2) THEN BEGIN ; 2015 version
 IF (keyword_set(detector)) THEN BEGIN
   IF (keyword_set(debug)) THEN print,'Using detector ',detector
   CASE detector OF
    'P18': cc = [0.977484, 0.0185055, -0.00391209, 70.4]
    'P19': cc = [0.965314, 0.0234026, -0.00256943, 70.4]
    'P20': cc = [0.968436, 0.0220869, -0.00285115, 70.4]
    'P21': cc = [0.982854, 0.0142877, -0.00317682, 70.4]
    'P22': cc = [1.049, -0.0237173, -0.00288312, 70.4]
    'P23': cc = [0.990172, 0.0091968, -0.00238961, 70.4]
    'P1823': cc = [0.983195, 0.0141778, -0.00317682, 70.4]
    'P1922': cc = [1.00978, -0.000698302, -0.00328272, 70.4]
    'P2021': cc = [0.97712, 0.0175904, -0.00308092, 70.4]
    'P24': cc = [0.999958, 0.00309391, -0.00177223, 44.1]
    'P25': cc = [0.994381, 0.00591109, -0.00162038, 44.1]
    'P26': cc = [0.990046, 0.00854446, -0.00177223, 44.1]
    'P2526': cc = [0.992115, 0.00717982, -0.00167233, 44.1]
    'P27': cc = [1.00503, 0.00276424, -0.00282717, 28.4]
    'P28': cc = [1.00491, 0.00334266, -0.00313287, 28.4]
    'WK11': cc = [0.939366, 0.0346715, -0.00214346, 22.8]
    'WK12': cc = [1.00894, 0.000982418, -0.00276923, 22.8]
    'WK1': cc = [0.972902, 0.0190469, -0.00276464, 22.8]
    'WKa11': cc = [0.974784, 0.0159578, -0.00161958, 33.0]
    'WKa12': cc = [0.992978, 0.00737502, -0.00200839, 33.0]
    'WKa1': cc = [0.983787, 0.0117567, -0.00183716, 33.0]
    'WQ11': cc = [0.990948, 0.00846474, -0.00204555, 40.6]
    'WQ12': cc = [0.998159, 0.00404356, -0.00167233, 40.6]
    'WQ1': cc = [0.994548, 0.00627672, -0.00186693, 40.6]
    'WQ21': cc = [0.981607, 0.0126181, -0.00166893, 40.6]
    'WQ22': cc = [1.01705, -0.00573297, -0.0016989, 40.6]
    'WQ2': cc = [0.998986, 0.00378172, -0.00176723, 40.6]
    'WV11': cc = [0.939474, 0.0354285, -0.00155105, 60.8]
    'WV12': cc = [0.994737, 0.006396, -0.00217822, 60.8]
    'WV1': cc = [0.966309, 0.0217416, -0.00209331, 60.8]
    'WV21': cc = [1.00662, -0.000113686, -0.00217942, 60.8]
    'WV22': cc = [0.977227, 0.0160255, -0.00220999, 60.8]
    'WV2': cc = [0.991701, 0.0082012, -0.00226214, 60.8]
    'WW11': cc = [0.988343, 0.00956424, -0.00211948, 93.5]
    'WW12': cc = [0.9838, 0.0120015, -0.00173207, 93.5]
    'WW1': cc = [0.986087, 0.0107974, -0.00193167, 93.5]
    'WW21': cc = [0.978714, 0.0149705, -0.00148032, 93.5]
    'WW22': cc = [0.992004, 0.00655744, -0.00146334, 93.5]
    'WW2': cc = [0.985324, 0.0108262, -0.00149331, 93.5]
    'WW31': cc = [0.977457, 0.0155997, -0.00131688, 93.5]
    'WW32': cc = [0.993636, 0.0054001, -0.00134126, 93.5]
    'WW3': cc = [0.985473, 0.0105855, -0.00135485, 93.5]
    'WW41': cc = [0.991452, 0.0072962, -0.00181239, 93.5]
    'WW42': cc = [0.973071, 0.0185705, -0.00153746, 93.5]
    'WW4': cc = [0.982185, 0.0130277, -0.00170889, 93.5]
   ELSE: BEGIN
     print,'Invalid detector specified for fastcc, returning zero.'
     return, 0d
   ENDELSE
   ENDCASE
 ENDIF ELSE BEGIN ; individual frequencies
   IF (keyword_set(debug)) THEN print,'Using frequency ',freq
   CASE freq OF
     'CBASSNI': cc = [1.000103213196618, -0.0007238230723748647, -0.0013363809246677324, 4.76]
     'CBASSNP': cc = [0.998561438218094, -0.0059052869678747595, -0.001680320871507042, 4.76]
     'Q111': cc = [0.9925526276311687, 0.007161407883127753, -0.0017891332783659003, 11.2]
     'Q113': cc = [0.9949649181723395, 0.005394042720463821, -0.0014382949498306515, 12.8]
     'Q111p': cc = [0.9925526276311687, 0.007161407883127753, -0.0017891332783659003, 11.2]
     'Q113p': cc = [0.9949649181723395, 0.005394042720463821, -0.0014382949498306515, 12.8]
     'Q217': cc = [1.0129709167366905, -0.005101169068593444, -0.000683203301567257, 16.7]
     'Q219': cc = [1.0175292512259428, -0.007544762181222079, -0.0006248503973819523, 18.7]
     'Q217p': cc = [1.0165157773037472, -0.006419637626097819, -0.000927550610591879, 16.7]
     'Q219p': cc = [1.0136255722145442, -0.004544629474433171, -0.0010878048910708117, 18.7]
     'Q311': cc = [0.9820571573496972, 0.011947716397192746, -0.0015316600265756597, 11.1]
     'Q313': cc = [1.002376171424373, 0.00087053237460555, -0.0010541678118863593, 12.9]
     'Q311p': cc = [0.9843034690253142, 0.011094990021336104, -0.0016791051042741416, 11.1]
     'Q313p': cc = [0.9958959030027292, 0.0051175051270606255, -0.0014905894344412235, 12.9]
     'Q417': cc = [0.9888926591458963, 0.006986281593109233, -0.0007107060258669477, 17.0]
     'Q419': cc = [0.9886433438856964, 0.007541246196285672, -0.0009156379893644272, 19.0]
     'Q417p': cc = [1.0029823815141663, 0.0008640490621996672, -0.0012140291472187072, 17.0]
     'Q419p': cc = [0.9843617866675408, 0.010330165097893152, -0.0012211561793953436, 19.0]
     'P30': cc = [1.00513, 0.00301399, -0.00300699, 28.4]
     'P44': cc = [0.994769, 0.00596703, -0.00173626, 44.1]
     'P70': cc = [0.989711, 0.0106943, -0.00328671, 70.4]
     'P100': cc = [0.9952835351962233, -0.007239481180040377, -0.004211453482240249, 100.0]
     'P143': cc = [1.00994594645371, 0.005811737546852095, -0.004342394286587356, 143.0]
     'P217': cc = [0.9850957294640018, -0.016079422733509176, -0.0035799396324725217, 217.0]
     'P353': cc = [0.9838850223400122, -0.017222883189337086, -0.003294659291023683, 353.0]
     'P545': cc = [0.9858927513258451, -0.01445625909566499, -0.004198782898699968, 545.0]
     'P857': cc = [1.0016037903615955, -0.0002352573927594772, -0.00426643435387609, 857.0]
     'WK' : cc = [0.972902, 0.0190469, -0.00276464, 22.8]
     'WKa': cc = [0.983787, 0.0117567, -0.00183716, 33.0]
     'WQ' : cc = [0.996854, 0.00496893, -0.00181359, 40.6]
     'WV' : cc = [0.980322, 0.0143631, -0.00223596, 60.8]
     'WW' : cc = [0.984848, 0.0112743, -0.00164595, 93.5]
     'DB10': cc = [1.0056317,   -0.0052173,   -0.0119257, 1249]
     'DB9': cc = [1.0347912,    0.0245728,   -0.0095350, 2141]
     'DB8': cc = [0.9593942,   -0.0469581,   -0.0075185, 2997]
     'DB7': cc = [0.9079217,   -0.0942761,   -0.0068850, 4995]
     'DB6': cc = [0.8160551,   -0.1717965,    0.0103011, 11988]
     'DB5': cc = [0.9816717,   -0.0327394,   -0.0178211, 24975]
     'DB4': cc = [0.9947178,   -0.0060948,   -0.0008378, 61163]
     'DB3': cc = [1.0030533,   -0.0001524,   -0.0032236, 85629]
     'DB2': cc = [1.0064020,    0.0050962,   -0.0012763, 136227]
     'DB1': cc = [1.0073260,    0.0044317,   -0.0028791, 239760]
     'I100': cc = [0.9899184805240909, -0.01970072476335274, -0.007706943391147654, 2997]
     'I60': cc = [0.9510100573154361, -0.06111819772388552, -0.016457316462171055, 4995]
     'I25': cc = [0.9123700815757735, -0.08972760549528734, -0.0056369170040417305, 11988]
     'I12': cc = [0.9083422603187424, -0.09300485963152248, -0.008759896726856715, 24975]
     ELSE: BEGIN
       print,'Invalid frequency specified for fastcc, returning zero.'
       return, 0d
      ENDELSE
   ENDCASE
 ENDELSE
ENDIF ELSE BEGIN ; 2013 version
 IF (keyword_set(detector)) THEN BEGIN
   IF (keyword_set(debug)) THEN print,'Using detector ',detector
   CASE detector OF
    'P18': cc = [0.98836, 0.0123556, -0.00394, 70.4]
    'P19': cc = [0.93933, 0.0375844, -0.00225, 70.4]
    'P20': cc = [0.95663, 0.0285644, -0.00273, 70.4]
    'P21': cc = [0.97140, 0.0209690, -0.00318, 70.4]
    'P22': cc = [1.02220,-0.0077263, -0.00327, 70.4]
    'P23': cc = [1.00098, 0.0029940, -0.00240, 70.4]
    'P24': cc = [0.99571, 0.0053247, -0.00175, 44.1]
    'P25': cc = [0.98988, 0.0082248, -0.00161, 44.1]
    'P26': cc = [0.98557, 0.0107023, -0.00175, 44.1]
    'P27': cc = [0.98513, 0.0129780, -0.00288, 28.4]
    'P28': cc = [0.98516, 0.0134605, -0.00318, 28.4]
   ELSE: BEGIN
     print,'Invalid detector specified for fastcc, returning zero.'
     return, 0d
   ENDELSE
   ENDCASE
 ENDIF ELSE BEGIN ; individual frequencies
   IF (keyword_set(debug)) THEN print,'Using frequency ',freq
   CASE freq OF
     'Q111': cc = [0.99278484, 0.00709364, -0.00182065, 11.2]
     'Q113': cc = [0.99583466, 0.00512841, -0.00151745, 12.8]
     'Q217': cc = [1.00166741, 4.87517031e-04, -6.63221982e-04, 16.7]
     'Q219': cc = [0.997955472, 1.66235456e-03, -4.36898290e-04, 18.7]
     'Q311': cc = [0.99421638, 0.00712698, -0.00234507, 11.1]
     'Q313': cc = [0.98683305, 0.01021644, -0.00182772, 12.9]
     'Q417': cc = [0.996066342, 3.10394890e-03, -5.71903939e-04, 17.0]
     'Q419': cc = [0.997016199, 2.40564506e-03, -4.58929918e-04, 19.0]
     'P30': cc = [0.98520, 0.0131778, -0.00302, 28.4]
     'P44': cc = [0.99059, 0.0079600, -0.00169, 44.1]
     'P70': cc = [0.98149, 0.0152737, -0.00325, 70.4]
     'P100': cc = [0.9951437650323804, -0.007369184015019507, -0.004219721586609552, 100.0]
     'P143': cc = [1.010279726985317, 0.006104370487138567, -0.004343504886286414, 143.0]
     'P217': cc = [0.9851008169926466, -0.016072766879219946, -0.0035796643275518014, 217.0]
     'P353': cc = [0.9838102656623505, -0.017294824120252014, -0.0032959086890859243, 353.0]
     'P545': cc = [0.9858044871754406, -0.014536137607886598, -0.004194156574955682, 545.0]
     'P857': cc = [1.0015212847910664, -0.00030701728952350806, -0.004261697246303725, 857.0]
     'WK':  BEGIN
            wmap=1
            nu = [20.6, 22.8, 24.9]
            w = [0.332906, 0.374325, 0.292768]
            dT = 1.013438
           END
     'WKa': BEGIN
            wmap=1
            nu = [30.4, 33.0, 35.6]
            w = [0.322425, 0.387532, 0.290043]
            dT = 1.028413
           END
     'WQ':  BEGIN
            wmap=1
            nu = [37.8, 40.7, 43.8]
            w = [0.353635, 0.342752, 0.303613]
            dT = 1.043500
           END
     'WV':  BEGIN
            wmap=1
            nu = [55.7, 60.7, 66.2]
            w = [0.337805, 0.370797, 0.291399]
            dT = 1.098986
           END
     'WW':  BEGIN
            wmap=1
            nu = [87.0, 93.5, 100.8]
            w = [0.337633, 0.367513, 0.294854]
            dT = 1.247521
           END
     'DB10': cc = [1.0056317,   -0.0052173,   -0.0119257, 1249]
     'DB9': cc = [1.0347912,    0.0245728,   -0.0095350, 2141]
     'DB8': cc = [0.9593942,   -0.0469581,   -0.0075185, 2997]
     'DB7': cc = [0.9079217,   -0.0942761,   -0.0068850, 4995]
     'DB6': cc = [0.8160551,   -0.1717965,    0.0103011, 11988]
     'DB5': cc = [0.9816717,   -0.0327394,   -0.0178211, 24975]
     'DB4': cc = [0.9947178,   -0.0060948,   -0.0008378, 61163]
     'DB3': cc = [1.0030533,   -0.0001524,   -0.0032236, 85629]
     'DB2': cc = [1.0064020,    0.0050962,   -0.0012763, 136227]
     'DB1': cc = [1.0073260,    0.0044317,   -0.0028791, 239760]
     'I100': cc = [0.9899184805240909, -0.01970072476335274, -0.007706943391147654, 2997]
     'I60': cc = [0.9510100573154361, -0.06111819772388552, -0.016457316462171055, 4995]
     'I25': cc = [0.9123700815757735, -0.08972760549528734, -0.0056369170040417305, 11988]
     'I12': cc = [0.9083422603187424, -0.09300485963152248, -0.008759896726856715, 24975]
     ELSE: BEGIN
       print,'Invalid frequency specified for fastcc, returning zero.'
       return, 0d
      ENDELSE
   ENDCASE
 ENDELSE
ENDELSE

retfreq = 0.0
IF (wmap) THEN BEGIN
 beta=-2.0+alpha
 T0 = 1.0 * (nu[0]/nu[1])^beta
 T1 = 1.0
 T2 = 1.0 * (nu[2]/nu[1])^beta
 dT = 1.0 ; Because conversion from T_CMB to T_RJ is done elsewhere.
 fastCC = 1.0/(dT * (w[0]*T0 + w[1]*T1 + w[2]*T2))
 retfreq = nu[1]

ENDIF ELSE BEGIN
 fastCC = cc[0] + cc[1]*alpha + cc[2]*alpha*alpha
 retfreq = cc[3]
ENDELSE

IF (keyword_set(returnfreq)) THEN BEGIN
  returnfreq = retfreq
ENDIF
RETURN, fastCC

END
