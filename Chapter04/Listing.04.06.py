#!/usr/bin/env python3
from scipy.optimize import fsolve
import numpy as np
# ..................................... Define Vector-Valued Function
def func(xvect):
  x1,x2=xvect
  r1=4*x1+2*x2**2-4
  r2=np.exp(x1)+3*x1*x2-5*x2**3+3
  return[r1,r2]
# ............................................ Define Starting Vector
xstart=[1,1]
# ................ Solve System of Equations, Print Results and Check
sol=fsolve(func,xstart)
print('Solution:',sol)
print('Check:',func(sol))
