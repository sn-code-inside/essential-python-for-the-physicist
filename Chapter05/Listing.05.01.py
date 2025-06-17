#!/usr/bin/env python3
#coding: utf8 
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
#  ........................... Function that computes the derivatives
def dfdt(y0,t, params):
  theta,omega = y0
  GdivL,=params
  derivs = [omega,-GdivL*np.sin(theta)]
  return derivs
# ............................................... Initial Conditions
theta0=np.pi/2.0
omega0=0.0
y0=[theta0,omega0]
# ........................................................ Parameters
GdivL=4.9
params=[GdivL]
Omega=np.sqrt(GdivL)
period=2.0*np.pi/Omega
# ..................................................... List of Times
t=np.linspace(0.0,period,101)
ThetaHar=theta0*np.cos(Omega*t)
# ................................................. Solution and Plot
sol=odeint(dfdt,y0,t,args=(params,))
theta=sol[:,0]
plt.plot(t,theta,'k')
plt.plot(t,ThetaHar,'k--')
plt.axhline(linewidth=1, color='k')
plt.rcParams.update({'font.size': 18})
plt.grid()
plt.xlabel(r'$t$/s', fontsize=22)
plt.ylabel(r'$\vartheta$/rad',fontsize=22)
plt.text(2.10,0.5,'Harmonic',fontsize=16,rotation=65)
plt.text(2.23,-0.4,'Large Amplitude',fontsize=16,rotation=65)
plt.tight_layout()
plt.savefig('LargAmpl00.pdf',format='pdf',dpi=1000)
plt.show()
