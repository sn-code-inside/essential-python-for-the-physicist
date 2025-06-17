#!/usr/bin/env python3
from numpy import exp
from scipy.optimize import bisect
# ................................................... Define Function
def fun(x):
  return 5.0+4.0*x-exp(x)
# ................................... Interval Endpoints and Accuracy
a=0.0
b=10.0
eps=1.0e-15
# ....................................Solve Equation and Print Result
x=bisect(fun,a,b,xtol=eps)
print(x)



