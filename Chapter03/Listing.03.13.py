#!/usr/bin/env python3
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
# .................................................. define 3D figure
ax=plt.axes(projection='3d')
# ................................................... define function
def fun(x,y):
  return np.sin(x)*np.cos(y)
# ....................................................... define grid
x=np.linspace(-np.pi,np.pi,50)
y=np.linspace(-np.pi,np.pi,50)
xx,yy=np.meshgrid(x,y)
# .........................................................
zz=fun(xx,yy)
# ...................................................... plot surface
ax.plot_surface(xx,yy,zz,rstride=1,cstride=1,\
  cmap='hot',edgecolor='none');
# ........................................................ label axes
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z');
# ................................................... save pdf figure
plt.savefig('surface3D.pdf',format='pdf',dpi=1000)
# ........................................... display plot on monitor
plt.show()
