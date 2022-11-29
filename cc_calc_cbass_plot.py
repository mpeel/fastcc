import matplotlib.pyplot as plt
import numpy as np
outdir = 'plots_2022_11_08/'

alphas = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
alphas = np.asarray(alphas)
old_I = [1.0001032131966172, -0.0007238230723749948, -0.00133638092466769, 4.76]
old_P = [0.9985614382180937, -0.005905286967874863, -0.001680320871506988, 4.76]

new_I = [1.0017152397219213, 0.004681376835425419, -0.0011099406898534073, 4.76]
new_P = [1.00067251064749, 0.0010118648563905157, -0.0014314759990750453, 4.76]

test_I = [1.0003317241376664, 3.5727991808456454e-05, -0.0013071225208285435, 4.76]
test_P = [0.9988609218460283, -0.00493454594155687, -0.0016504828405324431, 4.76]

plt.plot(alphas,old_I[0]+old_I[1]*alphas+old_I[2]*alphas**2,'--',c='r',label='I_eq1')
plt.plot(alphas,old_P[0]+old_P[1]*alphas+old_P[2]*alphas**2,'--',c='b',label='P_eq1')
plt.plot(alphas,new_I[0]+new_I[1]*alphas+new_I[2]*alphas**2,'-',c='r',label='I_eq2')
plt.plot(alphas,new_P[0]+new_P[1]*alphas+new_P[2]*alphas**2,'-',c='b',label='P_eq2')
plt.plot(alphas,test_I[0]+test_I[1]*alphas+test_I[2]*alphas**2,linestyle='dotted',c='r',label='I_eq3')
plt.plot(alphas,test_P[0]+test_P[1]*alphas+test_P[2]*alphas**2,linestyle='dotted',c='b',label='P_eq3')
l = plt.legend(prop={'size':11})
l.set_zorder(20)
plt.savefig(outdir+'cbass_comparison.png')
