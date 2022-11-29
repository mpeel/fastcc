import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from astrocode.astroutils import *
from fastcc import *
from cc_calc_functions import *

def do_polyfit(x,y,z,name,do_log=False,order=2):
	if do_log:
		x = np.log10(x)
		# y = np.log10(y)
		# plt.yscale('log')
		plt.xscale('log')
	plt.pcolormesh(x,y,z)
	plt.colorbar()
	plt.tight_layout()
	plt.savefig(name+'_cc.png')
	plt.clf()
	fit = polyfit2d(x, y, z, kx=order, ky=order, order=3)
	# print(fit)
	fit_params = fit[0].reshape(order+1,order+1)
	# print(fit_params)
	fit_vals = z.copy()
	# print(np.shape(fit_vals))
	# print(len(x))
	for i in range(0,len(x)-1):
		for j in range(0,len(y)-1):
			if order == 2:
				fit_vals[j][i] = fit_params[0][0] + fit_params[0][1]*x[i] + fit_params[0][2]*x[i]*x[i] + fit_params[1][0]*y[j]+fit_params[2][0]*y[j]*y[j]+fit_params[1][1]*x[i]*y[j]
			else:
				fit_vals[j][i] = fit_params[0][0] + fit_params[0][1]*x[i] + fit_params[0][2]*x[i]*x[i] + fit_params[0][3]*x[i]*x[i]*x[i] + fit_params[1][0]*y[j]+fit_params[2][0]*y[j]*y[j]+fit_params[3][0]*y[j]*y[j]*y[j]+fit_params[1][1]*x[i]*y[j]+fit_params[1][2]*x[i]*x[i]*y[j]+fit_params[2][1]*x[i]*y[j]*y[j]
	plt.pcolormesh(x,y,fit_vals)
	if do_log:
		# plt.yscale('log')
		plt.xscale('log')
	plt.colorbar()
	plt.tight_layout()
	plt.savefig(name+'_poly.png')
	plt.clf()
	plt.pcolormesh(x,y,fit_vals-z)
	if do_log:
		# plt.yscale('log')
		plt.xscale('log')
	plt.colorbar()
	plt.tight_layout()
	plt.savefig(name+'_diff.png')
	plt.clf()
	print(name + ": " + str(np.max(np.abs(fit_vals-z))))
	# exit()

def polyfit2d(x, y, z, kx=3, ky=3, order=None):
    '''
    Two dimensional polynomial fitting by least squares.
    Fits the functional form f(x,y) = z.

    Notes
    -----
    Resultant fit can be plotted with:
    np.polynomial.polynomial.polygrid2d(x, y, soln.reshape((kx+1, ky+1)))

    Parameters
    ----------
    x, y: array-like, 1d
        x and y coordinates.
    z: np.ndarray, 2d
        Surface to fit.
    kx, ky: int, default is 3
        Polynomial order in x and y, respectively.
    order: int or None, default is None
        If None, all coefficients up to maxiumum kx, ky, ie. up to and including x^kx*y^ky, are considered.
        If int, coefficients up to a maximum of kx+ky <= order are considered.

    Returns
    -------
    Return paramters from np.linalg.lstsq.

    soln: np.ndarray
        Array of polynomial coefficients.
    residuals: np.ndarray
    rank: int
    s: np.ndarray

    '''

    # grid coords
    x, y = np.meshgrid(x, y)
    # coefficient array, up to x^kx, y^ky
    coeffs = np.ones((kx+1, ky+1))

    # solve array
    a = np.zeros((coeffs.size, x.size))

    # for each coefficient produce array x^i, y^j
    for index, (j, i) in enumerate(np.ndindex(coeffs.shape)):
        # do not include powers greater than order
        if order is not None and i + j > order:
            arr = np.zeros_like(x)
        else:
            arr = coeffs[i, j] * x**i * y**j
        a[index] = arr.ravel()

    # do leastsq fitting and return leastsq result
    return np.linalg.lstsq(a.T, np.ravel(z), rcond=None)

# cc = fits.open('ricardo_cc/c_alpha_dirbe.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_alpha_iras.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_td_beta_dirbe.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['CA'])
# cc.close()

# cc = fits.open('ricardo_cc/c_td_beta_iras.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['CA'])
# cc.close()


# cc = fits.open('ricardo_cc/c_alpha_hfi_bps_pr3.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()
# cc = fits.open('ricardo_cc/c_alpha_hfi_bps_pr2.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_alpha_hfi_pr1.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_td_beta_hfi_bps_pr3.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['CA'])
# print(np.shape(cc[1].data['CA']))
# # print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# data = cc[1].data['CA']
# # print(np.shape(cc[1].data['CA'][0][1][0]))
# # print(cc[1].data['CA'][0][1][0])
# # print(np.shape(cc[1].data['TD'][0]))
# do_polyfit(cc[1].data['TD'][0],cc[1].data['BETA'][0],cc[1].data['CA'][0][1][0],'p100')
# # plt.savefig('test.png')


# cc = fits.open('ricardo_cc/c_td_beta_iras.fits')
# cc = fits.open('ricardo_cc/c_td_beta_dirbe.fits')
# print(cc.info())
# print(cc[1].header)
# # print(cc[1].data['CA'])
# # print(np.shape(cc[1].data['CA']))
# # print(cc[1].data['BANDS'])
# # print(cc[1].data['PF'])
# # data = cc[1].data['CA']
# # print(np.shape(cc[1].data['CA'][0][1][0]))
# print(cc[1].data['CA'][0][0])
# print(np.shape(cc[1].data['TD'][0]))
# print(np.shape(cc[1].data['BETA'][0]))
# print(cc[1].data['TD'][0])#[:-56])
# print(cc[1].data['BETA'][0])
# # exit()
# for i in range(0,10):
# 	do_polyfit(cc[1].data['TD'][0],cc[1].data['BETA'][0],cc[1].data['CA'][0][i],'dirbe_nolog_'+str(i),do_log=False,order=3)
# 	do_polyfit(cc[1].data['TD'][0],cc[1].data['BETA'][0],cc[1].data['CA'][0][i],'dirbe_log_'+str(i),do_log=True,order=3)
# 	do_polyfit(cc[1].data['TD'][0],cc[1].data['BETA'][0],cc[1].data['CA'][0][i],'dirbe_'+str(i),do_log=False,order=2)
# fit = polyfit2d(cc[1].data['TD'][0], cc[1].data['BETA'][0], cc[1].data['CA'][0][1][0], kx=1, ky=1, order=None)
# fit_params = fit[0]
# print(fit_params)
# exit()
# fit_vals = cc[1].data['CA'][0][1][0].copy()
# for i in len(cc[1].data['TD'][0]):
# 	for j in len(cc[1].data['BETA'][0]):
# 		fit_vals[i][j] = 1.0
# cc.close()
# cc = fits.open('ricardo_cc/c_td_beta_hfi_bps_pr2.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_td_beta_hfi_pr1.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

# cc = fits.open('ricardo_cc/c_alpha_wmap_bps.fits')
# print(cc.info())
# print(cc[1].header)
# print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()

cc = fits.open('ricardo_cc/c_alpha_lfi_pr1.fits')
# cc = fits.open('ricardo_cc/c_alpha_lfi_pr3.fits')
# print(cc.info())
# print(cc[1].header)
print(cc[1].data['BANDS'])
print(cc[1].data['PF'])
cc.close()

# cc = fits.open('ricardo_cc/c_alpha_mfi_p6.fits')
# print(cc.info())
# print(cc[1].header)
# # print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()
# cc = fits.open('ricardo_cc/c_alpha_mfi_p6_pol.fits')
# print(cc.info())
# print(cc[1].header)
# # print(cc[1].data['BANDS'])
# print(cc[1].data['PF'])
# cc.close()
