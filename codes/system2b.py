#!/usr/bin/env python3
from scipy.optimize import fsolve
import numpy as np
# ..................................... Define Vector-Valued Function
def func(xvect):
  x,y=xvect
  r1=2*x**2-np.sin(x)+x*y-3
  r2=3*x+y**2+np.cos(x*y)-5
  return[r1,r2]
# ............................................ Define Starting Vector
xstart=(1,1)
# ................................... Solve System and Print Solution
sol=fsolve(func,xstart)
print("Solution:",sol)
print("Check:",func(sol))
