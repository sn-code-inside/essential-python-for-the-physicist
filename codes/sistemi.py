# .......................................... SystemSolve2
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

# ........................................... SystemSolve

#!/usr/bin/env python3
from scipy.optimize import fsolve
from numpy import exp

def func(xvect,*args):
  x,y=xvect
  a,b=params
  r1=x+y**2-a
  r2=exp(x)+x*y-b
  return[r1,r2]
a=4
b=3
params=[a,b]
xstart=(1,1)
sol=fsolve(func,xstart,args=(params,))
print(sol)

# ..................................... SystemSolveParams

#!/usr/bin/env python3
from scipy.optimize import fsolve
from numpy import exp
#
def func(xvect,params):
  x1,x2=xvect
  a11,a12,a21,a22,a23,c1,c2=params
  r1=a11*x1+a12*x2**2-c1
  r2=a21*exp(x1)+a22*x1*x2+a23*pow(x2,3)-c2
  return[r1,r2]
a11=4
a12=2
a21=1
a22=3
a23=-5
c1=4
c2=-3
parlist=[a11,a12,a21,a22,a23,c1,c2]
xstart=(1,1)
sol=fsolve(func,xstart,parlist)
print(sol)

