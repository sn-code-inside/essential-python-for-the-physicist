#!/usr/bin/env python3
#coding: utf8 
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
#
def dydt(y0,t, params):
  theta,omega = y0
  GdivL,=params
  derivs = [omega,-GdivL*np.sin(theta)]
  return derivs
#
theta0=170.0*np.pi/180.0
omega0=0.0
y0=[theta0,omega0]
#
GdivL=4.9
params=[GdivL]
Omega=np.sqrt(GdivL)
period=2.0*np.pi/Omega
#
t=np.linspace(0.0,period,101)
ThetaHar=theta0*np.cos(Omega*t)
#
sol=odeint(dydt,y0,t,args=(params,))
theta=sol[:,0]
plt.plot(t,theta,'k')
plt.plot(t,ThetaHar,'k--')
plt.axhline(linewidth=1, color='k')
plt.rcParams.update({'font.size': 18})
plt.grid()
plt.xlabel(r'$t$/s', fontsize=22)
plt.ylabel(r'$\vartheta$/rad',fontsize=22)
plt.text(2.25,1.8,'Harmonic',fontsize=16,rotation=65)
plt.text(1.10,2.5,'Large Amplitude',fontsize=16,rotation=-50)
plt.tight_layout()
plt.savefig('VeryLargeAmpl.pdf',format='pdf',dpi=1000)
plt.show()
