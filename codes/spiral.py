#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
plt.axis('equal')
x=[]
y=[]
for phi in np.arange(0,8*np.pi,0.1):
  r=10*phi
  x.append(r*np.cos(phi))
  y.append(r*np.sin(phi))
plt.plot(x,y)
plt.show()
