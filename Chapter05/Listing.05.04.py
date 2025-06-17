#!/usr/bin/env python3
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
# ............................................... Compute Derivatives
def dydt(y0,t,params):
  theta,omega=y0
  GdivL,alpha=params
  derivs = [omega,-alpha*omega-GdivL*np.sin(theta)]
  return derivs
# ........................................................ Parameters
alpha=0.2
GdivL=4.9
params=[GdivL,alpha]
# ................................................ Initial Conditions
theta0=np.pi/2.0
omega0=0.0
y0=[theta0,omega0]
# .......................................... Solve Equations and Plot
t=np.arange(0.0,12.01,0.1)
sol=odeint(dydt,y0,t,args=(params,))
theta=sol[:,0]
plt.figure(figsize=(10,4))
plt.plot(t,theta)
plt.grid()
plt.xlabel(r'$t$/s', fontsize=22)
plt.ylabel(r'$\vartheta$/rad',fontsize=22)
plt.tight_layout()
plt.savefig('PlotDrag.pdf',format='pdf',dpi=1000)
plt.show()
