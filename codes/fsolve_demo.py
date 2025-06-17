#!/usr/bin/env python3
from numpy import exp
from scipy.optimize import fsolve
# ................................................... Define Function
def fun(x):
  return 5.0+4.0*x-exp(x)
# ............................................ Choose a Staring Point
xstart=3.0
# ................................... Solve Equation and Print Result
x=fsolve(fun,xstart)
print(x)



