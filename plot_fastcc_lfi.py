# Quick script to plot the LFI colour correction curve
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

font = {'family' : 'normal',
        'size'   : 12}

matplotlib.rc('font', **font)

P30 = [1.00513, 0.00301399, -0.00300699, 28.4]
P44 = [0.994769, 0.00596703, -0.00173626, 44.1]
P70 = [0.989711, 0.0106943, -0.00328671, 70.4]

alphas = np.arange(-3.0,4.0,0.1)
plt.plot(alphas,P30[0]+P30[1]*alphas+P30[2]*alphas*alphas,label='28.4 GHz')
plt.plot(alphas,P44[0]+P44[1]*alphas+P44[2]*alphas*alphas,label='44.1 GHz')
plt.plot(alphas,P70[0]+P70[1]*alphas+P70[2]*alphas*alphas,label='70.4 GHz')
l = plt.legend(prop={'size':12})
l.set_zorder(20)
plt.xlabel('Spectral index',)
plt.ylabel('Colour correction')
plt.savefig('plots_2022_07_26/planck_lfi_cc.pdf')
plt.clf()
plt.close()
