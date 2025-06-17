#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
# .................................................. charge locations
yplus=1.0
yminus=-1.0
xplus=xminus=0.0
rad=0.1
lim=30
nLin=60
plt.axis('off')
plt.gca().set_aspect('equal')
# ....................................................... field lines
i=0
delta=0.05
while i<nLin:
  xlist=[]
  ylist=[]
  alpha0=i*2*np.pi/float(nLin)
  x=xplus+rad*np.cos(alpha0)
  y=yplus+rad*np.sin(alpha0)
  xlist.append(x)
  ylist.append(y)
  while True:
    alpha=np.arctan2((y-yplus),(x-xplus))
    beta=np.arctan2((y-yminus),(x-xminus))
    Eplus=1.0/((x-xplus)**2+(y-yplus)**2)
    Eminus=-1.0/((x-xminus)**2+(y-yminus)**2)
    Ex=Eplus*np.cos(alpha)+Eminus*np.cos(beta)
    Ey=Eplus*np.sin(alpha)+Eminus*np.sin(beta)
    gamma=np.arctan2(Ey,Ex)
    x=x+delta*np.cos(gamma)
    y=y+delta*np.sin(gamma)
    if x>lim or x<-lim or y>lim or y<0:
      break
    xlist.append(x)
    ylist.append(y)
  plt.plot(xlist,ylist,'k-',linewidth=0.5)
  ylist=-np.array(ylist)
  plt.plot(xlist,ylist,'k-',linewidth=0.5)
  i+=1
# ....................................................................
plt.savefig('DipoleField.pdf',format='pdf')
plt.show()  
