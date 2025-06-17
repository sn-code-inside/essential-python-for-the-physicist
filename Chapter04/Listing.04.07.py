#!/usr/bin/env python3
from scipy.optimize import fsolve
import numpy as np
# ..................................... Define Vector-Valued Function
def func(xvect,param):
  x1,x2=xvect
  a11,a12,a21,a22,a23,c1,c2=param
  r1=a11*x1+a12*x2**2-c1
  r2=a21*np.exp(x1)+a22*x1*x2+a23*x2**3-c2
  return[r1,r2]
# ........................... Define Parameters Appearing in Function
a11=4
a12=2
a21=1
a22=3
a23=-5
c1=4
c2=-3
parlist=[a11,a12,a21,a22,a23,c1,c2]
# ............................................ Define Starting Vector
xstart=(1,1)
# ........................ Solve System of Equations and Print Result
sol=fsolve(func,xstart,args=(parlist,))
print(sol)

