FUNCTION fastcc, freq, alpha, detector=detector, pair=pair,debug=debug,option=option
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

wmap=0 ; Flag used later to determine which formula to use.
IF (~keyword_set(option)) THEN BEGIN
  option = 3
ENDIF

IF (option EQ 3) THEN BEGIN ; 2018 version (mostly the same as 2015)
 IF (keyword_set(detector)) THEN BEGIN
   IF (keyword_set(debug)) THEN print,'Using detector ',detector
   CASE detector OF
   'CBASSNI1': cc = [1.00034365, -2.77979154e-05, -1.42647298e-03]
   'CBASSNQ1': cc = [1.00174566, 4.90209927e-03, -9.91547651e-04]
   'CBASSNU1': cc = [0.99528283, -0.01636643, -0.00203991]
   'CBASSNQ2': cc = [1.00262617, 7.94492681e-03, -8.33609206e-04]
   'CBASSNU2': cc = [0.99435903, -0.01924111, -0.00211413]
   'CBASSNI2': cc = [0.99986369, -0.00142099, -0.00124559]
   '18':   cc = [0.977484, 0.0185055, -0.00391209]
   '19':   cc = [0.965314, 0.0234026, -0.00256943]
   '20':   cc = [0.968436, 0.0220869, -0.00285115]
   '21':   cc = [0.982854, 0.0142877, -0.00317682]
   '22':   cc = [1.049, -0.0237173, -0.00288312]
   '23':   cc = [0.990172, 0.0091968, -0.00238961]
   '1823': cc = [0.983195, 0.0141778, -0.00317682]
   '1922': cc = [1.00978, -0.000698302, -0.00328272]
   '2021': cc = [0.97712, 0.0175904, -0.00308092]
   '24':   cc = [0.999958, 0.00309391, -0.00177223]
   '25':   cc = [0.994381, 0.00591109, -0.00162038]
   '26':   cc = [0.990046, 0.00854446, -0.00177223]
   '2526': cc = [0.992115, 0.00717982, -0.00167233]
   '27':   cc = [1.00503, 0.00276424, -0.00282717]
   '28':   cc = [1.00491, 0.00334266, -0.00313287]
   'K11':  cc = [0.939366, 0.0346715, -0.00214346]
   'K12':  cc = [1.00894, 0.000982418, -0.00276923]
   'K1':   cc = [0.972902, 0.0190469, -0.00276464]
   'Ka11': cc = [0.974784, 0.0159578, -0.00161958]
   'Ka12': cc = [0.992978, 0.00737502, -0.00200839]
   'Ka1':  cc = [0.983787, 0.0117567, -0.00183716]
   'Q11':  cc = [0.990948, 0.00846474, -0.00204555]
   'Q12':  cc = [0.998159, 0.00404356, -0.00167233]
   'Q1':   cc = [0.994548, 0.00627672, -0.00186693]
   'Q21':  cc = [0.981607, 0.0126181, -0.00166893]
   'Q22':  cc = [1.01705, -0.00573297, -0.0016989]
   'Q2':   cc = [0.998986, 0.00378172, -0.00176723]
   'V11':  cc = [0.939474, 0.0354285, -0.00155105]
   'V12':  cc = [0.994737, 0.006396, -0.00217822]
   'V1':   cc = [0.966309, 0.0217416, -0.00209331]
   'V21':  cc = [1.00662, -0.000113686, -0.00217942]
   'V22':  cc = [0.977227, 0.0160255, -0.00220999]
   'V2':   cc = [0.991701, 0.0082012, -0.00226214]
   'W11':  cc = [0.988343, 0.00956424, -0.00211948]
   'W12':  cc = [0.9838, 0.0120015, -0.00173207]
   'W1':   cc = [0.986087, 0.0107974, -0.00193167]
   'W21':  cc = [0.978714, 0.0149705, -0.00148032]
   'W22':  cc = [0.992004, 0.00655744, -0.00146334]
   'W2':   cc = [0.985324, 0.0108262, -0.00149331]
   'W31':  cc = [0.977457, 0.0155997, -0.00131688]
   'W32':  cc = [0.993636, 0.0054001, -0.00134126]
   'W3':   cc = [0.985473, 0.0105855, -0.00135485]
   'W41':  cc = [0.991452, 0.0072962, -0.00181239]
   'W42':  cc = [0.973071, 0.0185705, -0.00153746]
   'W4':   cc = [0.982185, 0.0130277, -0.00170889]
   ELSE: BEGIN
     print,'Invalid detector specified for fastcc, returning zero.'
     return, 0d
   ENDELSE
   ENDCASE
 ENDIF ELSE BEGIN ; individual frequencies
   IF (keyword_set(debug)) THEN print,'Using frequency ',freq
   CASE freq OF
     'CBASSNI': cc = [1.00010321, -7.23821956e-04, -1.33638136e-03]
     'CBASSNQ': cc = [1.00218686, 6.42043451e-03, -9.15401174e-04]
     'CBASSNU': cc = [0.99482118, -0.0178066, -0.00207946]
     '30': cc = [1.00513, 0.00301399, -0.00300699]
     '44': cc = [0.994769, 0.00596703, -0.00173626]
     '70': cc = [0.989711, 0.0106943, -0.00328671]
     '100': cc = [9.9714231e-01, -6.9773742e-03, -4.3697958e-03]
     '143': cc = [1.0125265e+00,  7.5433883e-03, -4.7070021e-03]
     '217': cc = [9.8706579e-01, -1.6046101e-02, -3.7911625e-03]
     '353': cc = [9.8564571e-01, -1.7143920e-02, -3.3450378e-03]
     '545': cc = [9.8595744e-01, -1.7003248e-02, -4.2110542e-03]
     '857': cc = [1.0033977e+00, -3.3857918e-04, -4.4123940e-03]
     'K':  cc = [0.972902, 0.0190469, -0.00276464]
     'Ka': cc = [0.983787, 0.0117567, -0.00183716]
     'Q':  cc = [0.996854, 0.00496893, -0.00181359]
     'V':  cc = [0.980322, 0.0143631, -0.00223596]
     'W':  cc = [0.984848, 0.0112743, -0.00164595]
     '111': cc = [0.99278484, 0.00709364, -0.00182065]
     '113': cc = [0.99583466, 0.00512841, -0.00151745]
     '111p': cc = [0.99278484, 0.00709364, -0.00182065]
     '113p': cc = [0.99583466, 0.00512841, -0.00151745]
     '217': cc = [1.01297024, -5.10076638e-03, -6.83231540e-04]
     '219': cc = [1.01753081, -7.54598924e-03, -6.24661331e-04]
     '217p': cc = [1.01651591, -6.41886504e-03, -9.27987505e-04]
     '219p': cc = [1.01362151, -0.00454101, -0.00108849]
     '311': cc = [0.98205768, 0.01194747, -0.00153167]
     '313': cc = [1.00237737, 8.69627158e-04, -1.05404485e-03]
     '311p': cc = [0.9843027, 0.01109582, -0.00167935]
     '313p': cc = [0.99589013, 0.00512221, -0.00149134]
     '417': cc = [9.88881900e-01, 6.99633538e-03, -7.13114820e-04]
     '419': cc = [9.88613460e-01, 7.56366528e-03, -9.18841805e-04]
     '417p': cc = [1.00297783, 8.68521956e-04, -1.21513713e-03]
     '419p': cc = [0.98434787, 0.01034064, -0.00122269]
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
   'CBASSNI1': cc = [1.00034365, -2.77979154e-05, -1.42647298e-03]
   'CBASSNQ1': cc = [1.00174566, 4.90209927e-03, -9.91547651e-04]
   'CBASSNU1': cc = [0.99528283, -0.01636643, -0.00203991]
   'CBASSNQ2': cc = [1.00262617, 7.94492681e-03, -8.33609206e-04]
   'CBASSNU2': cc = [0.99435903, -0.01924111, -0.00211413]
   'CBASSNI2': cc = [0.99986369, -0.00142099, -0.00124559]
   '18':   cc = [0.977484, 0.0185055, -0.00391209]
   '19':   cc = [0.965314, 0.0234026, -0.00256943]
   '20':   cc = [0.968436, 0.0220869, -0.00285115]
   '21':   cc = [0.982854, 0.0142877, -0.00317682]
   '22':   cc = [1.049, -0.0237173, -0.00288312]
   '23':   cc = [0.990172, 0.0091968, -0.00238961]
   '1823': cc = [0.983195, 0.0141778, -0.00317682]
   '1922': cc = [1.00978, -0.000698302, -0.00328272]
   '2021': cc = [0.97712, 0.0175904, -0.00308092]
   '24':   cc = [0.999958, 0.00309391, -0.00177223]
   '25':   cc = [0.994381, 0.00591109, -0.00162038]
   '26':   cc = [0.990046, 0.00854446, -0.00177223]
   '2526': cc = [0.992115, 0.00717982, -0.00167233]
   '27':   cc = [1.00503, 0.00276424, -0.00282717]
   '28':   cc = [1.00491, 0.00334266, -0.00313287]
   'K11':  cc = [0.939366, 0.0346715, -0.00214346]
   'K12':  cc = [1.00894, 0.000982418, -0.00276923]
   'K1':   cc = [0.972902, 0.0190469, -0.00276464]
   'Ka11': cc = [0.974784, 0.0159578, -0.00161958]
   'Ka12': cc = [0.992978, 0.00737502, -0.00200839]
   'Ka1':  cc = [0.983787, 0.0117567, -0.00183716]
   'Q11':  cc = [0.990948, 0.00846474, -0.00204555]
   'Q12':  cc = [0.998159, 0.00404356, -0.00167233]
   'Q1':   cc = [0.994548, 0.00627672, -0.00186693]
   'Q21':  cc = [0.981607, 0.0126181, -0.00166893]
   'Q22':  cc = [1.01705, -0.00573297, -0.0016989]
   'Q2':   cc = [0.998986, 0.00378172, -0.00176723]
   'V11':  cc = [0.939474, 0.0354285, -0.00155105]
   'V12':  cc = [0.994737, 0.006396, -0.00217822]
   'V1':   cc = [0.966309, 0.0217416, -0.00209331]
   'V21':  cc = [1.00662, -0.000113686, -0.00217942]
   'V22':  cc = [0.977227, 0.0160255, -0.00220999]
   'V2':   cc = [0.991701, 0.0082012, -0.00226214]
   'W11':  cc = [0.988343, 0.00956424, -0.00211948]
   'W12':  cc = [0.9838, 0.0120015, -0.00173207]
   'W1':   cc = [0.986087, 0.0107974, -0.00193167]
   'W21':  cc = [0.978714, 0.0149705, -0.00148032]
   'W22':  cc = [0.992004, 0.00655744, -0.00146334]
   'W2':   cc = [0.985324, 0.0108262, -0.00149331]
   'W31':  cc = [0.977457, 0.0155997, -0.00131688]
   'W32':  cc = [0.993636, 0.0054001, -0.00134126]
   'W3':   cc = [0.985473, 0.0105855, -0.00135485]
   'W41':  cc = [0.991452, 0.0072962, -0.00181239]
   'W42':  cc = [0.973071, 0.0185705, -0.00153746]
   'W4':   cc = [0.982185, 0.0130277, -0.00170889]
   ELSE: BEGIN
     print,'Invalid detector specified for fastcc, returning zero.'
     return, 0d
   ENDELSE
   ENDCASE
 ENDIF ELSE BEGIN ; individual frequencies
   IF (keyword_set(debug)) THEN print,'Using frequency ',freq
   CASE freq OF
     'CBASSNI': cc = [1.00010321, -7.23821956e-04, -1.33638136e-03]
     'CBASSNQ': cc = [1.00218686, 6.42043451e-03, -9.15401174e-04]
     'CBASSNU': cc = [0.99482118, -0.0178066, -0.00207946]
     '30': cc = [1.00513, 0.00301399, -0.00300699]
     '44': cc = [0.994769, 0.00596703, -0.00173626]
     '70': cc = [0.989711, 0.0106943, -0.00328671]
     '100': cc = [0.99627715, -0.00786048, -0.00442135]
     '143': cc = [1.0112897,   0.00638959, -0.00468345]
     '217': cc = [0.9849717,  -0.01795939, -0.00363461]
     '353': cc = [0.98404306, -0.01867278, -0.00333562]
     '545': cc = [ 0.9860728,  -0.01689775, -0.00421863]
     '857': cc = [1.0023118,  -0.001392,   -0.00442368]
     'K':  cc = [0.972902, 0.0190469, -0.00276464]
     'Ka': cc = [0.983787, 0.0117567, -0.00183716]
     'Q':  cc = [0.996854, 0.00496893, -0.00181359]
     'V':  cc = [0.980322, 0.0143631, -0.00223596]
     'W':  cc = [0.984848, 0.0112743, -0.00164595]
     '111': cc = [0.99278484, 0.00709364, -0.00182065]
     '113': cc = [0.99583466, 0.00512841, -0.00151745]
     '111p': cc = [0.99278484, 0.00709364, -0.00182065]
     '113p': cc = [0.99583466, 0.00512841, -0.00151745]
     '217': cc = [1.01297024, -5.10076638e-03, -6.83231540e-04]
     '219': cc = [1.01753081, -7.54598924e-03, -6.24661331e-04]
     '217p': cc = [1.01651591, -6.41886504e-03, -9.27987505e-04]
     '219p': cc = [1.01362151, -0.00454101, -0.00108849]
     '311': cc = [0.98205768, 0.01194747, -0.00153167]
     '313': cc = [1.00237737, 8.69627158e-04, -1.05404485e-03]
     '311p': cc = [0.9843027, 0.01109582, -0.00167935]
     '313p': cc = [0.99589013, 0.00512221, -0.00149134]
     '417': cc = [9.88881900e-01, 6.99633538e-03, -7.13114820e-04]
     '419': cc = [9.88613460e-01, 7.56366528e-03, -9.18841805e-04]
     '417p': cc = [1.00297783, 8.68521956e-04, -1.21513713e-03]
     '419p': cc = [0.98434787, 0.01034064, -0.00122269]
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
   '18':   cc = [0.98836, 0.0123556, -0.00394]
   '19':   cc = [0.93933, 0.0375844, -0.00225]
   '20':   cc = [0.95663, 0.0285644, -0.00273]
   '21':   cc = [0.97140, 0.0209690, -0.00318]
   '22':   cc = [1.02220,-0.0077263, -0.00327]
   '23':   cc = [1.00098, 0.0029940, -0.00240]
   '1823': BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   '1922': BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   '2021': BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   '24':   cc = [0.99571, 0.0053247, -0.00175]
   '25':   cc = [0.98988, 0.0082248, -0.00161]
   '26':   cc = [0.98557, 0.0107023, -0.00175]
   '2526': BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   '27':   cc = [0.98513, 0.0129780, -0.00288]
   '28':   cc = [0.98516, 0.0134605, -0.00318]
   'K11':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'K12':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'K1':   BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'Ka11': BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'Ka12': BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'Ka1':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'Q11':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'Q12':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'Q1':   BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'Q21':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'Q22':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'Q2':   BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'V11':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'V12':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'V1':   BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'V21':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'V22':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'V2':   BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W11':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W12':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W1':   BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W21':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W22':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W2':   BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W31':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W32':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W3':   BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W41':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W42':  BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   'W4':   BEGIN
            print, 'Not coded for stable configuration, returning zero'
            return, 0d
           END
   ELSE: BEGIN
     print,'Invalid detector specified for fastcc, returning zero.'
     return, 0d
   ENDELSE
   ENDCASE
 ENDIF ELSE BEGIN ; individual frequencies
   IF (keyword_set(debug)) THEN print,'Using frequency ',freq
   CASE freq OF
     '30': cc = [0.98520, 0.0131778, -0.00302]
     '44': cc = [0.99059, 0.0079600, -0.00169]
     '70': cc = [0.98149, 0.0152737, -0.00325]
     '100': cc = [0.9961675, -0.00797581, -0.00443089]
     '143': cc = [1.0116307,  0.0067101,  -0.00468848]
     '217': cc = [0.98497796,-0.01795222, -0.003634  ]
     '353': cc = [0.9840204,  -0.01869955, -0.00333974]
     '545': cc = [0.985983,   -0.01698006, -0.00421302]
     '857': cc = [1.002219,   -0.00147517, -0.0044173 ]
     '111': cc = [0.99278484, 0.00709364, -0.00182065]
     '113': cc = [0.99583466, 0.00512841, -0.00151745]
     '217': cc = [1.00166741, 4.87517031e-04, -6.63221982e-04]
     '219': cc = [0.997955472, 1.66235456e-03, -4.36898290e-04]
     '311': cc = [0.99421638, 0.00712698, -0.00234507]
     '313': cc = [0.98683305, 0.01021644, -0.00182772]
     '417': cc = [0.996066342, 3.10394890e-03, -5.71903939e-04]
     '419': cc = [0.997016199, 2.40564506e-03, -4.58929918e-04]
     'K':  BEGIN
            wmap=1
            nu = [20.6, 22.8, 24.9]
            w = [0.332906, 0.374325, 0.292768]
            dT = 1.013438
           END
     'Ka': BEGIN
            wmap=1
            nu = [30.4, 33.0, 35.6]
            w = [0.322425, 0.387532, 0.290043]
            dT = 1.028413
           END
     'Q':  BEGIN
            wmap=1
            nu = [37.8, 40.7, 43.8]
            w = [0.353635, 0.342752, 0.303613]
            dT = 1.043500
           END
     'V':  BEGIN
            wmap=1
            nu = [55.7, 60.7, 66.2]
            w = [0.337805, 0.370797, 0.291399]
            dT = 1.098986
           END
     'W':  BEGIN
            wmap=1
            nu = [87.0, 93.5, 100.8]
            w = [0.337633, 0.367513, 0.294854]
            dT = 1.247521
           END
     ELSE: BEGIN
       print,'Invalid frequency specified for fastcc, returning zero.'
       return, 0d
      ENDELSE
   ENDCASE
 ENDELSE
ENDELSE

IF (wmap) THEN BEGIN
 beta=-2.0+alpha
 T0 = 1.0 * (nu[0]/nu[1])^beta
 T1 = 1.0
 T2 = 1.0 * (nu[2]/nu[1])^beta
 dT = 1.0 ; Because conversion from T_CMB to T_RJ is done elsewhere.
 fastCC = 1.0/(dT * (w[0]*T0 + w[1]*T1 + w[2]*T2))

ENDIF ELSE BEGIN
 fastCC = cc[0] + cc[1]*alpha + cc[2]*alpha*alpha
ENDELSE

RETURN, fastCC

END
