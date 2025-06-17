#!/usr/bin/env python3
from scipy.optimize import fsolve
from numpy import exp
#
def func(xvect):
  x1,x2=xvect
  r1=4*x1+2*x2**2-4
  r2=exp(x1)+3*x1*x2-5*pow(x2,3)+3
  return[r1,r2]
xstart=(1,1)
sol=fsolve(func,xstart)
print("Solution:",sol)
#
print("Check:",func(sol))
