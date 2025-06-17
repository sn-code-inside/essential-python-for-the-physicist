#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
# .................................................. Define Functions
def fun1(t,omega,tau,ampl):
  y=ampl*np.cos(omega*t)*np.exp(-t/tau)
  return y
def fun2(t,omega,omega2,ampl):
  y=ampl*np.sin(omega2*t)*np.sin(omega*t)
  return y
# ............................... Numerical values for the parameters
omega=32.0
omega2=np.pi/2.0
tau=1.0
ampl=5.0
ampl2=10.0
# ................................................ Create Plot Arrays
t=np.linspace(0.0,2.0,201)
s1=fun1(t,omega,tau,ampl)
s2=fun2(t,omega,omega2,ampl2)
# ........................................... Figure Width and Height
plt.figure(figsize=(10,4))
# ......................................................... subplot 1
plt.subplot(1,2,1)
plt.plot(t,s1)
plt.plot(t,ampl*np.exp(-t/tau))
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel(r'$A\,\cos(\omega t)\,{\rm e}^{-t/\tau}$',fontsize=24)
plt.xlabel(r'$t$',fontsize=24)
plt.tight_layout()
# ......................................................... subplot 2
plt.subplot(1,2,2)
plt.plot(t,s2)
plt.plot(t,ampl2*np.sin(omega2*t))
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel(r'$B\,\sin(\omega t)\,\sin(\omega_2 t)$',fontsize=24)
plt.xlabel(r'$t$',fontsize=24)
plt.tight_layout()
# ................................................... Save PDF Figure
plt.savefig('MultiPlot0.pdf',format='pdf',dpi=1000)
plt.show()







