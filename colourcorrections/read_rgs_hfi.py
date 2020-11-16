import scipy.io as sio
from scipy.io import readsav

c_alpha_hfi_pr1 = readsav('c_alpha_hfi_pr1.sav')
c_alpha_hfi_pr2 = readsav('c_alpha_hfi_pr2.sav')
c_alpha_hfi_pr3 = readsav('c_alpha_hfi_pr3.sav')

# print(c_alpha_hfi_pr1)
# print(c_alpha_hfi_pr1.keys())
# print(c_alpha_hfi_pr2.keys())
# print(c_alpha_hfi_pr3.keys())

print(c_alpha_hfi_pr1.pf)
print(c_alpha_hfi_pr2.pf)
print(c_alpha_hfi_pr3.pf)
