#  ......................................optbisect.py
#!/usr/bin/env python3
from numpy import exp
from scipy.optimize import bisect
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
x=bisect(fun,a,b,xtol=eps)
print(x)

# ............................................ optbrent.py

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

# ............................................. fsolve_demo.py

#!/usr/bin/env python3
from numpy import exp
from scipy.optimize import fsolve
#
def fun(x):
  return 5.0+4.0*x-exp(x)
#
xstart=1.0
#
x=fsolve(fun,xstart)
print(x)

