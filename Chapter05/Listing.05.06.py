#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
# .......................................................... function
def dfdt(state,t):
  x,y,vx,vy=state
  r=np.sqrt(x**2+y**2)
  alpha=np.arctan2(y,x)
  a=-K/r
  ax=a*np.cos(alpha)
  ay=a*np.sin(alpha)
  return [vx,vy,ax,ay]
# .................................................. numerical values
x=0.01             #  m
vx=y=0.0
vy=2.934e4         #  m/s
K=3.443e9          #  m2/s2
# ...................................................... input lists
t=np.arange(0.0,5.0e-6,1.0e-8) #1.0e-9
yy=[x,y,vx,vy]
# ...................................... solve differential equations
psoln=odeint(dfdt,yy,t)
# ............................................... plot the trajectory
plt.axis('equal')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.plot(psoln[:,0],psoln[:,1],'k-')
plt.plot(0.0,0.0,'ko')
plt.savefig('WireProt.pdf',format='pdf',dpi=1000)
plt.show()








