#!/usr/bin/env python3
import numpy  as np
#
A=np.array([[3.0,-2.0,-1.0],[2.0,-2.0,4.0],[-1.0,0.5,-1.5]])
b=np.array([2.0,0.0,-1.0])
x=np.linalg.solve(A,b)
print('x =',x)
bb=np.dot(A,x)
print('bb =',bb)

# .....................................................................

#!/usr/bin/env python3
from numpy import exp
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
iter=1
while (b-a)>eps:
  c=(a+b)/2.0
  fc=fun(c)
  if fc==0:
    print("x = ",c)
    exit()
  if fc*fa>0:
    a=c
    fa=fc
  else:
    b=c
    fb=fc
  iter+=1
#
print("x = ",c)
print("accuracy = ",'{:.2e}'.format(b-a))
print("f(",c,") =",fun(c))
print(iter," iterations needed")

