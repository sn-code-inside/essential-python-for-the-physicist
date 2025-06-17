#!/usr/bin/env python3
from numpy import exp
# ................................................... Define Function
def fun(x):
  return 5.0+4.0*x-exp(x)
# ................... Define Interval Endpoints and Required Accuracy
a=0.0
b=10.0
eps=1.0e-15
# ............................... Evaluiate Function at the Endpoints
fa=fun(a)
fb=fun(b)
# ................................ Check If Bisection Method Can Work
if fa*fb>0:
  print('wrong interval!!!',fa,fb)
  exit()
# .................................... Evaluate Solution by Bisection
iter=1
while (b-a)>eps:
  c=(a+b)/2.0
  fc=fun(c)
  if fc==0:
    print('x = ',c)
    exit()
  if fc*fa>0:
    a=c
    fa=fc
  else:
    b=c
    fb=fc
  iter+=1
# ..................................................... Print Results
print('x = ',c)
print(f'accuracy = {b-a:.2e}')
print(f'f({c:.3f}) = {fun(c):.3e}')
print(iter,' iterations needed')



