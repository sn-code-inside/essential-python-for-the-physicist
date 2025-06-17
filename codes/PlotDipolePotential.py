#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
# .................................................. charge locations
yplus=1.0
yminus=-1.0
xplus=xminus=0.0
rad=0.1
lim=30
# ...................................................................
plt.axis('off')
plt.gca().set_aspect('equal')
# ....................................................... field lines
i=0
delta=0.05
DeltaPot=2
ystart=yplus+1
while ystart<20:
  xlist=[]
  ylist=[]
  x=0
  y=ystart
  xlist.append(x)
  ylist.append(y)
  while True:
    alpha=np.arctan2((y-yplus),(x-xplus))
    beta=np.arctan2((y-yminus),(x-xminus))
    Eplus=1.0/((x-xplus)**2+(y-yplus)**2)
    Eminus=-1.0/((x-xminus)**2+(y-yminus)**2)
    Ex=Eplus*np.cos(alpha)+Eminus*np.cos(beta)
    Ey=Eplus*np.sin(alpha)+Eminus*np.sin(beta)
    gamma=np.arctan2(Ey,Ex)-np.pi/2
    x=x+delta*np.cos(gamma)
    y=y+delta*np.sin(gamma)
    if x>lim or x<-delta or y>lim or y<0:
      break
    xlist.append(x)
    ylist.append(y)
  plt.plot(xlist,ylist,'k-',linewidth=0.5)
  ylist=-np.array(ylist)
  plt.plot(xlist,ylist,'k-',linewidth=0.5)
  xlist=-np.array(xlist)
  plt.plot(xlist,ylist,'k-',linewidth=0.5)
  ylist=-np.array(ylist)
  plt.plot(xlist,ylist,'k-',linewidth=0.5)
  ystart+=DeltaPot
# ....................................................................
plt.plot((-10,10),(0,0),'k-',linewidth=0.5)
plt.text(-0.9,yplus-0.55,'+',fontsize=14)
plt.text(-1.0,yminus-0.65,r'$-$',fontsize=14)
# ....................................................................
plt.savefig('DipolePotential.pdf',format='pdf',bbox_inches='tight',\
  pad_inches=0)
plt.show()  
