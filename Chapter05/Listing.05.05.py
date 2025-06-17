#!/usr/bin/env python3
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
# ................................................ Initial Conditions
const=3.47e5
r=1.0e-7
v=0.0
state=[r,v]
t=np.arange(0.0,5.01e-9,1.0e-10)
# ....................................................... Derivatives
def dfdt(state,t):
  r,vel=state
  acc=const/r
  derivs=[vel,acc]
  return derivs
# .......................................... Solve Equations and Plot
sol=odeint(dfdt,state,t)
rr=sol[:,0]
plt.figure(figsize=(10,10))
plt.plot(t,rr)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.grid()
plt.xlabel(r'$t$/ns', fontsize=40)
plt.ylabel(r'$r$/m',fontsize=40)
plt.tight_layout()
plt.savefig('Explosion.pdf',format='pdf',dpi=1000)
plt.show()
