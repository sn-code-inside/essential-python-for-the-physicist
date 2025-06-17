#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
#
def Lang(x):
  if abs(x)>1:
    return 1.0/np.tanh(x)-1.0/x
  else:
    return x/3-x**3/45     #  +x**5*(2/945)
#
xlist=np.arange(-6,6.05,0.2)
ylist=[]
for x in xlist:
  ylist.append(Lang(x))
plt.plot(xlist,ylist)
plt.show()
  

