#!/usr/bin/env python3
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
# ........................................ define 3D figure
ax = plt.axes(projection='3d')
# ............................. vertices of the 3D polyline
zz = np.linspace(-2*np.pi,2*np.pi,81)
xx = np.sin(zz)
yy = np.cos(zz)
# .................................... draw the 3D polyline
ax.plot3D(xx,yy,zz,'red')
# .................. 3D-coordinates of the scattered points
xpoints = xx+0.2*(0.5-np.random.random(81))
ypoints = yy+0.2*(0.5-np.random.random(81))
zpoints = zz+0.2*(0.5-np.random.random(81))
# ............................ draw the 3D scattered points
ax.scatter3D(xpoints,ypoints,zpoints,c=ypoints,\
  cmap='rainbow')
# ..................................... generate pdf figure
plt.savefig('Scatter3D.pdf',format='pdf',dpi=1000,\
  bbox_inches='tight',pad_inches=0)
# ............................ show the plot on the monitor
plt.show()
