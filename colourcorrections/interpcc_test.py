from interpcc import *
import time

file = 'ricardo_cc/c_td_10-40_beta_hfi_bps_pr3.fits'
time0 = time.time()
pcc100 = interpcc_setup(file,'P100',method=3)
time1 = time.time()
print(f"\nInterpolation time (Planck, 100GHz): {np.around(time1-time0,2)} sec\n")

print('P100 (Td=15,Bd=1.5): ' + str(interpcc(pcc100,td=15.0,bd=1.5)))
print('P100 (Td=16,Bd=1.5): ' + str(interpcc(pcc100,td=16.0,bd=1.5)))
print('P100 (Td=17,Bd=1.5): ' + str(interpcc(pcc100,td=17.0,bd=1.5)))
print('P100 (Td=18,Bd=1.5): ' + str(interpcc(pcc100,td=18.0,bd=1.5)))
print('P100 (Td=19,Bd=1.5): ' + str(interpcc(pcc100,td=19.0,bd=1.5)))
print('P100 (Td=20,Bd=1.5): ' + str(interpcc(pcc100,td=20.0,bd=1.5)))

file = 'ricardo_cc/c_td_beta_iras.fits'
irascc1 = interpcc_setup(file,'I100')
print('I100 (Td=15,Bd=1.5): ' + str(interpcc(irascc1,td=15.0,bd=1.5)))
print('I100 (Td=20,Bd=1.5): ' + str(interpcc(irascc1,td=20.0,bd=1.5)))
print('I100 (Td=25,Bd=1.5): ' + str(interpcc(irascc1,td=25.0,bd=1.5)))
print('I100 (Td=30,Bd=1.5): ' + str(interpcc(irascc1,td=30.0,bd=1.5)))
print('I100 (Td=35,Bd=1.5): ' + str(interpcc(irascc1,td=35.0,bd=1.5)))
irascc2 = interpcc_setup(file,'I60')
print('I60 (Td=15,Bd=1.5): ' + str(interpcc(irascc2,td=15.0,bd=1.5)))
print('I60 (Td=20,Bd=1.5): ' + str(interpcc(irascc2,td=20.0,bd=1.5)))
print('I60 (Td=25,Bd=1.5): ' + str(interpcc(irascc2,td=25.0,bd=1.5)))
print('I60 (Td=30,Bd=1.5): ' + str(interpcc(irascc2,td=30.0,bd=1.5)))
print('I60 (Td=35,Bd=1.5): ' + str(interpcc(irascc2,td=35.0,bd=1.5)))
irascc3 = interpcc_setup(file,'I25')
print('I25 (Td=15,Bd=1.5): ' + str(interpcc(irascc3,td=15.0,bd=1.5)))
print('I25 (Td=20,Bd=1.5): ' + str(interpcc(irascc3,td=20.0,bd=1.5)))
print('I25 (Td=25,Bd=1.5): ' + str(interpcc(irascc3,td=25.0,bd=1.5)))
print('I25 (Td=30,Bd=1.5): ' + str(interpcc(irascc3,td=30.0,bd=1.5)))
print('I25 (Td=35,Bd=1.5): ' + str(interpcc(irascc3,td=35.0,bd=1.5)))
irascc4 = interpcc_setup(file,'I12')
print('I12 (Td=15,Bd=1.5): ' + str(interpcc(irascc4,td=15.0,bd=1.5)))
print('I12 (Td=20,Bd=1.5): ' + str(interpcc(irascc4,td=20.0,bd=1.5)))
print('I12 (Td=25,Bd=1.5): ' + str(interpcc(irascc4,td=25.0,bd=1.5)))
print('I12 (Td=30,Bd=1.5): ' + str(interpcc(irascc4,td=30.0,bd=1.5)))
print('I12 (Td=35,Bd=1.5): ' + str(interpcc(irascc4,td=35.0,bd=1.5)))

# path = "/Users/clopez/proyectosIAC/cosmology/foregrounds/dirbe/colour_corrections/"
# file =path+'c_td_beta_dirbe.fits'

file ='ricardo_cc/c_td_beta_dirbe.fits'

print("Using '10', '9', '8'")
dirbecc10 = interpcc_setup(file,'10')
dirbecc9 = interpcc_setup(file,'9')
dirbecc8 = interpcc_setup(file,'8')

print('Band10 (Td=15,Bd=1.5): ' + str(interpcc(dirbecc10,td=15.0,bd=1.5)))
print('Band9  (Td=15,Bd=1.5): ' + str(interpcc(dirbecc9,td=15.0,bd=1.5)))
print('Band8  (Td=15,Bd=1.5): ' + str(interpcc(dirbecc8,td=15.0,bd=1.5)))

#

print("Using 'DB10', 'DB9', 'DB8'")
dirbecc10 = interpcc_setup(file,'DB10')
dirbecc9 = interpcc_setup(file,'DB9')
dirbecc8 = interpcc_setup(file,'DB8')

print('Band10 (Td=15,Bd=1.5): ' + str(interpcc(dirbecc10,td=15.0,bd=1.5)))
print('Band9  (Td=15,Bd=1.5): ' + str(interpcc(dirbecc9,td=15.0,bd=1.5)))
print('Band8  (Td=15,Bd=1.5): ' + str(interpcc(dirbecc8,td=15.0,bd=1.5)))

