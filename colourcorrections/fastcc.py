#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# Apply colour corrections to Planck LFI and WMAP data
# freq should be one of 30, 44, 70, K, Ka, Q, V or W, as a string.
 # Actual frequencies are 28.4, 44.1 or 70.4 for LFI; 22.80 33.00 40.60 60.80 93.50 for WMAP
 # detector (optional) should be between '18' and '28' inclusive for LFI, as a string; they should of the style 'K11', 'K12', 'K1' for WMAP. Only works for power laws.
# set 'debug' to see debug messages
# Use 'option' to select which set of colour corrections you want to use:
#  'option=1' is the WMAP9 and Planck 2013 numbers
#  'option=2' is the WMAP 2015 and Planck 2015 numbers
#  'option=3' is the WMAP 2015 and Planck 2018 numbers (DEFAULT)
#  If you don't want to use the latest version, you MUST set option to preserve the same behaviour from future versions.
# Set alpha=<val> to use a power law, or td=<val> and bd=<val> to use a modified black body
# Set debug=True if you want some extra debug messages to appear
# Set returnfreq=True if you want the code to return [freq, correction], otherwise it will just return correction
#
# Version history:
# Mike Peel   01-Feb-2013   v1.0 Initial version
# Mike Peel   04-Feb-2013   v1.1 Correct convention
# Locke Spencer 05-Feb-2013:  v1.2 Changed name to LFI_fastCC from planckcc (it only works for LFI)
#                             Changed nested IF..ELSE groups to case statements
#                             Changed invalid detector/frequency output to zero and removed internal stop in the code.
# Mike Peel   24-Jul-2014   v2.0 Added WMAP (based on values from Paddy Leahy), renamed to fastcc. Note that function calls from v1 won't work with v2 without modification.
# Mike Peel   13-Aug-2014   v2.1 Updated WMAP colour corrections, taking into account frequency drift during the mission (values from Paddy Leahy).
# Mike Peel   06-Nov-2014   v2.2 Added 'dev' parameter (updated LFI and WMAP numbers from Paddy Leahy, including LFI bandpass shifts); without this parameter the published values for LFI and WMAP will be returned.
# Mike Peel   12-Mar-2015   v2.3 Update 70GHz values to fits to corrected colour corrections from Paddy Leahy
# Mike Peel   23-Mar-2015   v2.4 Update WMAP colour corrections to corrected values from Paddy Leahy.
# Mike Peel   22-Jan-2016   v2.5 Convert from IDL to Python
# Mike Peel   17-Jul-2019   v2.6 Swap 'dev' for 'latest' parameter, add QUIJOTE MFI for testing
# Mike Peel   17-Jul-2019   v2.6a Revised QUIJOTE numbers
# Mike Peel   18-Jul-2019   v2.7 Adding CBASS
# Mike Peel   06-Oct-2020   v2.8 New QUIJOTE numbers
# Mike Peel   16-Nov-2020   v2.9 BREAKING CHANGE, 'latest' is now 'option'. Adding HFI power laws.
# Mike Peel   15-Jan-2021   v3.0 BREAKING CHANGE, frequency/detector labels now have prefixes. Upgrading to return frequencies and to prepare for colour corrections for thermal dust models for Planck HFI (not added in this version). Updated numbers for MFI, HFI, C-BASS.
# Mike Peel   10-Feb-2021   v3.1 Adding DIRBE and IRAS
# Mike Peel   26-Feb-2021   v3.2 Updating QUIJOTE, HFI, DIRBE, IRAS, adding HFI modified black body
# Mike Peel   01-Mar-2021   v3.3 Updating QUIJOTE 17 and 19GHz

def fastcc(freq, alpha=False, td=False, bd=False, detector=False, debug=False, option=3, returnfreq=False):
	# Define dictionaries containing the coefficients for different detectors and frequencies
	# WMAP9 + Planck 2013 + QUIJOTE MFI original
	frequencies_v1 = {
		'Q11': [0.99421638, 0.00712698, -0.00234507, 11.1],
		'Q13': [0.98683305, 0.01021644, -0.00182772, 12.9],
		'Q17': [1.00166741, 4.87517031e-04, -6.63221982e-04, 16.7],
		'Q19': [0.997955472, 1.66235456e-03, -4.36898290e-04, 18.7],
		'P30': [0.98520, 0.0131778, -0.00302, 28.4],
		'P44': [0.99059, 0.0079600, -0.00169, 44.1],
		'P70': [0.98149, 0.0152737, -0.00325, 70.4],
		'P100': [0.9957806,  -0.0079764,  -0.00431805, 100.0],
		'P143': [1.0115104,   0.00670483, -0.00465519, 143.0],
		'P217': [0.9843917,  -0.01793987, -0.00345606, 217.0],
		'P353': [0.9834889,  -0.01869916, -0.0031923, 353.0],
		'P545': [0.9852726,  -0.01683206, -0.00393032, 545.0],
		'P857': [1.0015814,  -0.00154559, -0.00421434, 857.0],
		'WK' : {'nu': [20.6, 22.8, 24.9], 'w': [0.332906, 0.374325, 0.292768], 'dT': 1.013438},
		'WKa': {'nu': [30.4, 33.0, 35.6], 'w': [0.322425, 0.387532, 0.290043], 'dT': 1.028413},
		'WQ' : {'nu': [37.8, 40.7, 43.8], 'w': [0.353635, 0.342752, 0.303613], 'dT': 1.043500},
		'WV' : {'nu': [55.7, 60.7, 66.2], 'w': [0.337805, 0.370797, 0.291399], 'dT': 1.098986},
		'WW' : {'nu': [87.0, 93.5, 100.8], 'w': [0.337633, 0.367513, 0.294854], 'dT': 1.247521},
		'DB10': [1.0056317,   -0.0052173,   -0.0119257, 1249],
		'DB9':  [1.0347912,    0.0245728,   -0.0095350, 2141],
		'DB8':  [0.9593942,   -0.0469581,   -0.0075185, 2997],
		'DB7':  [0.9079217,   -0.0942761,   -0.0068850, 4995],
		'DB6':  [0.8160551,   -0.1717965,    0.0103011, 11988],
		'DB5':  [0.9816717,   -0.0327394,   -0.0178211, 24975],
		'DB4':  [0.9947178,   -0.0060948,   -0.0008378, 61163],
		'DB3':  [1.0030533,   -0.0001524,   -0.0032236, 85629],
		'DB2':  [1.0064020,    0.0050962,   -0.0012763, 136227],
		'DB1':  [1.0073260,    0.0044317,   -0.0028791, 239760],
		'I100': [0.9899184805240909, -0.01970072476335274, -0.007706943391147654, 2997],
		'I60': [0.9510100573154361, -0.06111819772388552, -0.016457316462171055, 4995],
		'I25': [0.9123700815757735, -0.08972760549528734, -0.0056369170040417305, 11988],
		'I12': [0.9083422603187424, -0.09300485963152248, -0.008759896726856715, 24975]
	}
	detectors_v1 = {
		'Q111': [0.99278484, 0.00709364, -0.00182065, 11.2],
		'Q113': [0.99583466, 0.00512841, -0.00151745, 12.8],
		'Q217': [1.00166741, 4.87517031e-04, -6.63221982e-04, 16.7],
		'Q219': [0.997955472, 1.66235456e-03, -4.36898290e-04, 18.7],
		'Q311': [0.99421638, 0.00712698, -0.00234507, 11.1],
		'Q313': [0.98683305, 0.01021644, -0.00182772, 12.9],
		'Q417': [0.996066342, 3.10394890e-03, -5.71903939e-04, 17.0],
		'Q419': [0.997016199, 2.40564506e-03, -4.58929918e-04, 19.0],
		'P18': [0.98836, 0.0123556, -0.00394, 70.4],
		'P19': [0.93933, 0.0375844, -0.00225, 70.4],
		'P20': [0.95663, 0.0285644, -0.00273, 70.4],
		'P21': [0.97140, 0.0209690, -0.00318, 70.4],
		'P22': [1.02220,-0.0077263, -0.00327, 70.4],
		'P23': [1.00098, 0.0029940, -0.00240, 70.4],
		'P24': [0.99571, 0.0053247, -0.00175, 44.1],
		'P25': [0.98988, 0.0082248, -0.00161, 44.1],
		'P26': [0.98557, 0.0107023, -0.00175, 44.1],
		'P27': [0.98513, 0.0129780, -0.00288, 28.4],
		'P28': [0.98516, 0.0134605, -0.00318, 28.4]
	}
	mbb_v1 =  {
		'P100': [9.78302300e-01, -8.62236600e-04,  1.36959025e-05, -2.59891562e-02, -3.56237032e-03, 100.0],
		'P143': [1.02247059e+00, -9.17630852e-04,  1.45960412e-05, -1.14919655e-02, -4.26908862e-03, 143.0],
		'P217': [9.74371731e-01, -2.16696435e-03,  3.47218520e-05, -3.21109220e-02, -2.52205669e-03, 217.0],
		'P353': [1.00078213e+00, -3.71209905e-03,  5.97756043e-05, -3.04965433e-02, -2.43337080e-03, 353.0],
		'P545': [1.05366600e+00, -6.55682059e-03,  1.05510808e-04, -2.98897382e-02, -2.86604161e-03, 545.0],
		'P857': [1.09370363e+00, -6.18117163e-03,  9.40234822e-05, -9.27975681e-03, -3.77657381e-03, 857.0]
	}

	# WMAP9 modified by Paddy Leahy, Planck 2015, MFI 2019 pre-release, CBASS-N pre-release
	frequencies_v2 = {
		'CBASSNI': [1.000103213196618, -0.0007238230723748647, -0.0013363809246677324, 4.76],
		'CBASSNP': [0.998561438218094, -0.0059052869678747595, -0.001680320871507042, 4.76],
		'Q11': [0.9820571573496972, 0.011947716397192746, -0.0015316600265756597, 11.1],
		'Q13': [1.002376171424373, 0.00087053237460555, -0.0010541678118863593, 12.9],
		'Q11p': [0.9843034690253142, 0.011094990021336104, -0.0016791051042741416, 11.1],
		'Q13p': [0.9958959030027292, 0.0051175051270606255, -0.0014905894344412235, 12.9],
		'Q17': [1.0125436391913436, -0.0047626476557725075, -0.0007290181381636897, 16.8],
		'Q19': [1.0097515098746093, -0.0029060962669316278, -0.000945980118358522, 18.8],
		'Q17p': [1.0269452929735823, -0.011160166272101483, -0.0011604058894213811, 16.8],
		'Q19p': [1.005366057632537, 1.531136601255456e-05, -0.0012837681732906182, 18.8],
		'P30': [1.00513, 0.00301399, -0.00300699, 28.4],
		'P44': [0.994769, 0.00596703, -0.00173626, 44.1],
		'P70': [0.989711, 0.0106943, -0.00328671, 70.4],
		'P100': [0.99806035, -0.00576334, -0.00433317, 100.0],
		'P143': [1.0113103,   0.00652353, -0.00465055, 143.0],
		'P217': [0.98461574, -0.01773364, -0.00346536, 217.0],
		'P353': [0.98313624, -0.01902254, -0.00317299, 353.0],
		'P545': [0.98094696, -0.02082102, -0.00375779, 545.0],
		'P857': [0.994686,   -0.00797382, -0.00402693, 857.0],
		'WK' : [0.972902, 0.0190469, -0.00276464, 22.8],
		'WKa': [0.983787, 0.0117567, -0.00183716, 33.0],
		'WQ' : [0.996854, 0.00496893, -0.00181359, 40.6],
		'WV' : [0.980322, 0.0143631, -0.00223596, 60.8],
		'WW' : [0.984848, 0.0112743, -0.00164595, 93.5],
		'DB10': [1.0056317,   -0.0052173,   -0.0119257, 1249],
		'DB9':  [1.0347912,    0.0245728,   -0.0095350, 2141],
		'DB8':  [0.9593942,   -0.0469581,   -0.0075185, 2997],
		'DB7':  [0.9079217,   -0.0942761,   -0.0068850, 4995],
		'DB6':  [0.8160551,   -0.1717965,    0.0103011, 11988],
		'DB5':  [0.9816717,   -0.0327394,   -0.0178211, 24975],
		'DB4':  [0.9947178,   -0.0060948,   -0.0008378, 61163],
		'DB3':  [1.0030533,   -0.0001524,   -0.0032236, 85629],
		'DB2':  [1.0064020,    0.0050962,   -0.0012763, 136227],
		'DB1':  [1.0073260,    0.0044317,   -0.0028791, 239760],
		'I100': [0.9899184805240909, -0.01970072476335274, -0.007706943391147654, 2997],
		'I60': [0.9510100573154361, -0.06111819772388552, -0.016457316462171055, 4995],
		'I25': [0.9123700815757735, -0.08972760549528734, -0.0056369170040417305, 11988],
		'I12': [0.9083422603187424, -0.09300485963152248, -0.008759896726856715, 24975]
	}
	detectors_v2 = {
		'P18': [0.977484, 0.0185055, -0.00391209, 70.4],
		'P19': [0.965314, 0.0234026, -0.00256943, 70.4],
		'P20': [0.968436, 0.0220869, -0.00285115, 70.4],
		'P21': [0.982854, 0.0142877, -0.00317682, 70.4],
		'P22': [1.049, -0.0237173, -0.00288312, 70.4],
		'P23': [0.990172, 0.0091968, -0.00238961, 70.4],
		'P1823': [0.983195, 0.0141778, -0.00317682, 70.4],
		'P1922': [1.00978, -0.000698302, -0.00328272, 70.4],
		'P2021': [0.97712, 0.0175904, -0.00308092, 70.4],
		'P24': [0.999958, 0.00309391, -0.00177223, 44.1],
		'P25': [0.994381, 0.00591109, -0.00162038, 44.1],
		'P26': [0.990046, 0.00854446, -0.00177223, 44.1],
		'P2526': [0.992115, 0.00717982, -0.00167233, 44.1],
		'P27': [1.00503, 0.00276424, -0.00282717, 28.4],
		'P28': [1.00491, 0.00334266, -0.00313287, 28.4],
		'WK11': [0.939366, 0.0346715, -0.00214346, 22.8],
		'WK12': [1.00894, 0.000982418, -0.00276923, 22.8],
		'WK1': [0.972902, 0.0190469, -0.00276464, 22.8],
		'WKa11': [0.974784, 0.0159578, -0.00161958, 33.0],
		'WKa12': [0.992978, 0.00737502, -0.00200839, 33.0],
		'WKa1': [0.983787, 0.0117567, -0.00183716, 33.0],
		'WQ11': [0.990948, 0.00846474, -0.00204555, 40.6],
		'WQ12': [0.998159, 0.00404356, -0.00167233, 40.6],
		'WQ1': [0.994548, 0.00627672, -0.00186693, 40.6],
		'WQ21': [0.981607, 0.0126181, -0.00166893, 40.6],
		'WQ22': [1.01705, -0.00573297, -0.0016989, 40.6],
		'WQ2': [0.998986, 0.00378172, -0.00176723, 40.6],
		'WV11': [0.939474, 0.0354285, -0.00155105, 60.8],
		'WV12': [0.994737, 0.006396, -0.00217822, 60.8],
		'WV1': [0.966309, 0.0217416, -0.00209331, 60.8],
		'WV21': [1.00662, -0.000113686, -0.00217942, 60.8],
		'WV22': [0.977227, 0.0160255, -0.00220999, 60.8],
		'WV2': [0.991701, 0.0082012, -0.00226214, 60.8],
		'WW11': [0.988343, 0.00956424, -0.00211948, 93.5],
		'WW12': [0.9838, 0.0120015, -0.00173207, 93.5],
		'WW1': [0.986087, 0.0107974, -0.00193167, 93.5],
		'WW21': [0.978714, 0.0149705, -0.00148032, 93.5],
		'WW22': [0.992004, 0.00655744, -0.00146334, 93.5],
		'WW2': [0.985324, 0.0108262, -0.00149331, 93.5],
		'WW31': [0.977457, 0.0155997, -0.00131688, 93.5],
		'WW32': [0.993636, 0.0054001, -0.00134126, 93.5],
		'WW3': [0.985473, 0.0105855, -0.00135485, 93.5],
		'WW41': [0.991452, 0.0072962, -0.00181239, 93.5],
		'WW42': [0.973071, 0.0185705, -0.00153746, 93.5],
		'WW4': [0.982185, 0.0130277, -0.00170889, 93.5],
		'Q111': [0.9925526276311687, 0.007161407883127753, -0.0017891332783659003, 11.2],
		'Q113': [0.9949649181723395, 0.005394042720463821, -0.0014382949498306515, 12.8],
		'Q111p': [0.9925526276311687, 0.007161407883127753, -0.0017891332783659003, 11.2],
		'Q113p': [0.9949649181723395, 0.005394042720463821, -0.0014382949498306515, 12.8],
		'Q217': [1.0129709167366905, -0.005101169068593444, -0.000683203301567257, 16.7],
		'Q219': [1.0175292512259428, -0.007544762181222079, -0.0006248503973819523, 18.7],
		'Q217p': [1.0165157773037472, -0.006419637626097819, -0.000927550610591879, 16.7],
		'Q219p': [1.0136255722145442, -0.004544629474433171, -0.0010878048910708117, 18.7],
		'Q311': [0.9820571573496972, 0.011947716397192746, -0.0015316600265756597, 11.1],
		'Q313': [1.002376171424373, 0.00087053237460555, -0.0010541678118863593, 12.9],
		'Q311p': [0.9843034690253142, 0.011094990021336104, -0.0016791051042741416, 11.1],
		'Q313p': [0.9958959030027292, 0.0051175051270606255, -0.0014905894344412235, 12.9],
		'Q417': [0.9888926591458963, 0.006986281593109233, -0.0007107060258669477, 17.0],
		'Q419': [0.9886433438856964, 0.007541246196285672, -0.0009156379893644272, 19.0],
		'Q417p': [1.0029823815141663, 0.0008640490621996672, -0.0012140291472187072, 17.0],
		'Q419p': [0.9843617866675408, 0.010330165097893152, -0.0012211561793953436, 19.0]
	}
	mbb_v2 =  {
		'P100': [9.8406219e-01, -8.1796874e-04,  1.2984993e-05, -2.3725530e-02, -3.6248658e-03, 100.0],
		'P143': [1.0219676e+00, -9.1921160e-04,  1.4604784e-05, -1.1657137e-02, -4.2607225e-03, 143.0],
		'P217': [9.7481853e-01, -2.1586758e-03,  3.4575922e-05, -3.1927716e-02, -2.5357329e-03, 217.0],
		'P353': [1.0002152e+00, -3.7297627e-03,  6.0069218e-05, -3.0771509e-02, -2.4096791e-03, 353.0],
		'P545': [1.0512086e+00, -7.0331488e-03,  1.1341097e-04, -3.3633444e-02, -2.6284012e-03, 545.0],
		'P857': [1.1041638e+00, -7.7668922e-03,  1.2043497e-04, -1.5862772e-02, -3.4758949e-03, 857.0]
	}

	# WMAP9 modified by Paddy Leahy, Planck LFI 2015, MFI 2019 pre-release, CBASS-N pre-release, HFI 2018
	frequencies_v3 = {
		'CBASSNI': [1.000103213196618, -0.0007238230723748647, -0.0013363809246677324, 4.76],
		'CBASSNP': [0.998561438218094, -0.0059052869678747595, -0.001680320871507042, 4.76],
		'Q11': [0.9820571573496972, 0.011947716397192746, -0.0015316600265756597, 11.1],
		'Q13': [1.002376171424373, 0.00087053237460555, -0.0010541678118863593, 12.9],
		'Q11p': [0.9843034690253142, 0.011094990021336104, -0.0016791051042741416, 11.1],
		'Q13p': [0.9958959030027292, 0.0051175051270606255, -0.0014905894344412235, 12.9],
		'Q17': [1.0125436391913436, -0.0047626476557725075, -0.0007290181381636897, 16.8],
		'Q19': [1.0097515098746093, -0.0029060962669316278, -0.000945980118358522, 18.8],
		'Q17p': [1.0269452929735823, -0.011160166272101483, -0.0011604058894213811, 16.8],
		'Q19p': [1.005366057632537, 1.531136601255456e-05, -0.0012837681732906182, 18.8],
		'P30': [1.00513, 0.00301399, -0.00300699, 28.4],
		'P44': [0.994769, 0.00596703, -0.00173626, 44.1],
		'P70': [0.989711, 0.0106943, -0.00328671, 70.4],
		'P100': [0.99868757, -0.00512203, -0.00428818, 100.0],
		'P143': [1.0125835,   0.00767883, -0.00468418, 143.0],
		'P217': [0.98670965, -0.01582359, -0.00362294, 217.0],
		'P353': [0.98479307, -0.0174746,  -0.00318638, 353.0],
		'P545': [0.98083174, -0.0209257,  -0.00374975, 545.0],
		'P857': [0.9957921,  -0.00693394, -0.00402974, 857.0],
		'WK' : [0.972902, 0.0190469, -0.00276464, 22.8],
		'WKa': [0.983787, 0.0117567, -0.00183716, 33.0],
		'WQ' : [0.996854, 0.00496893, -0.00181359, 40.6],
		'WV' : [0.980322, 0.0143631, -0.00223596, 60.8],
		'WW' : [0.984848, 0.0112743, -0.00164595, 93.5],
		'DB10': [1.0056317e+00, -6.4834543e-03, -1.1925717e-02,  2.3065088e-04, 1249],
		'DB9':  [1.0347912e+00,  2.5405537e-02, -9.5349792e-03, -1.5169126e-04, 2141],
		'DB8':  [9.5939422e-01, -4.8364848e-02, -7.5184624e-03,  2.5625768e-04, 2997],
		'DB7':  [9.0792167e-01, -9.9896029e-02, -6.8849851e-03,  1.0237540e-03, 4995],
		'DB6':  [8.1605506e-01, -1.7407244e-01,  1.0301138e-02,  4.1460118e-04, 11988],
		'DB5':  [9.8167169e-01, -3.6703132e-02, -1.7821072e-02,  7.2205620e-04, 24975],
		'DB4':  [9.9471784e-01, -6.1251973e-03, -8.3776598e-04,  5.5378068e-06, 61163],
		'DB3':  [1.0030533e+00, -1.7146974e-04, -3.2236280e-03,  3.4781212e-06, 85629],
		'DB2':  [1.0064020e+00,  5.1325657e-03, -1.2763232e-03, -6.6162706e-06, 136227],
		'DB1':  [1.0073260e+00,  4.4526956e-03, -2.8791293e-03, -3.8249291e-06, 239760],
		'I100': [9.8682648e-01, -2.0946426e-02, -7.6484028e-03,  1.4026849e-04, 2997],
		'I60': [9.5354623e-01, -6.4501286e-02, -1.7309224e-02,  8.4418210e-04, 4995],
		'I25': [9.1217232e-01, -9.4449066e-02, -5.8258590e-03,  8.7096798e-04, 11988],
		'I12': [9.0728289e-01, -1.0321426e-01, -9.2115393e-03,  1.4914416e-03, 24975]
  	}
	# These haven't changed
	detectors_v3 = detectors_v2
	mbb_v3 = {
		'P100': [9.8575562e-01, -7.9658168e-04,  1.2639553e-05, -2.2861226e-02, -3.6062312e-03, 100.0],
		'P143': [1.0249784e+00, -8.9829491e-04,  1.4292214e-05, -1.0535011e-02, -4.3411409e-03, 143.0],
		'P217': [9.7928268e-01, -2.1219356e-03,  3.3978060e-05, -3.0585570e-02, -2.6902291e-03, 217.0],
		'P353': [1.0023545e+00, -3.5956064e-03,  5.7863985e-05, -2.9128991e-02, -2.4766673e-03, 353.0],
		'P545': [1.0511112e+00, -7.0444597e-03,  1.1361618e-04, -3.3710260e-02, -2.6224528e-03, 545.0],
		'P857': [1.1017295e+00, -7.4657206e-03,  1.1545943e-04, -1.4661285e-02, -3.5227763e-03, 857.0]
	}
	retfreq = 0.0
	# Pull out the desired coefficients from the above arrays
	if (detector != False):
		if (debug == True):
			print('Using detector ' + str(detector))
		if td:
			print('Not coded for black-body spectra and detectors, returning zero.')
			if returnfreq:
				return [0,0]
			else:
				return 0
		else:
			if (option == 3):
				cc = detectors_v3.get(detector, 0)
			elif (option == 2):
				cc = detectors_v2.get(detector, 0)
			else:
				cc = detectors_v1.get(detector, 0)

		if (cc == 0):
			print('Invalid detector specified for fastcc ('+str(detector)+'), returning zero.')
			if returnfreq:
				return [0,0]
			else:
				return 0

	else:
		if (debug == True):
			print('Using frequency ' + str(freq))

		if td:
			if (option == 3):
				cc = mbb_v3.get(freq, 0)
			elif (option == 2):
				cc = mbb_v2.get(freq, 0)
			else:
				cc = mbbb_v1.get(freq, 0)
		else:
			if (option == 3):
				cc = frequencies_v3.get(freq, 0)
			elif (option == 2):
				cc = frequencies_v2.get(freq, 0)
			else:
				cc = frequencies_v1.get(freq, 0)

		if (cc == 0):
			print('Invalid frequency specified for fastcc ('+str(freq)+'), returning zero.')
			if returnfreq:
				return [0,0]
			else:
				return 0

	if (type(cc) is dict):
		# We have WMAP values
		beta=-2.0+alpha
		T0 = 1.0 * (cc['nu'][0]/cc['nu'][1]) ** beta
		T1 = 1.0
		T2 = 1.0 * (cc['nu'][2]/cc['nu'][1]) ** beta
		dT = 1.0 # Because conversion from T_CMB to T_RJ is done elsewhere.
		fastCC = 1.0 / (cc['dT'] * (cc['w'][0]*T0 + cc['w'][1]*T1 + cc['w'][2]*T2))
		retfreq = cc['nu'][1]
	else:
		if len(cc) == 6:
			fastCC = cc[0] + cc[1]*td + cc[2]*(td**2) + cc[3] * bd + cc[4]*(bd**2)
			retfreq = cc[5]
		elif len(cc) == 5:
			fastCC = cc[0] + cc[1]*alpha + cc[2]*(alpha**2) + cc[3]*(alpha**2)
			retfreq = cc[4]
		else:
			fastCC = cc[0] + cc[1]*alpha + cc[2]*(alpha**2)
			retfreq = cc[3]

	if returnfreq:
		return [retfreq,fastCC]
	else:
		return fastCC
