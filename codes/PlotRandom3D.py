#!/usr/bin/env python3
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
# ........................................ define 3D figure
ax = plt.axes(projection='3d')
# .................. 3D-coordinates of the scattered points
xpoints = 10*(0.5-np.random.random(100))
ypoints = 10*(0.5-np.random.random(100))
zpoints = 10*(0.5-np.random.random(100))
# ............................ draw the 3D scattered points
ax.scatter3D(xpoints,ypoints,zpoints,c=ypoints,\
  cmap='Greys')
# ..................................... generate pdf figure
plt.savefig('Random3D.pdf',format='pdf',dpi=1000,\
  bbox_inches='tight',pad_inches=0)
# ............................ show the plot on the monitor
plt.show()
