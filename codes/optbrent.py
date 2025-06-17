#!/usr/bin/env python3
from numpy import exp
from scipy.optimize import brentq
#
def fun(x):
  return 5.0+4.0*x-exp(x)
#
a=0.0
b=10.0
eps=1.0e-15
#
fa=fun(a)
fb=fun(b)
#
if fa*fb>0:
  print("wrong interval!!!",fa,fb)
  exit()
#
x=brentq(fun,a,b,xtol=eps)
print(x)



