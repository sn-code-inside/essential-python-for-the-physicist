#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
# .................................................. Numerical Values
x0=1.0
y0=2.0
x1=3.0
y1=5.0
length=7.0
# ........................................................... CateFun
def CateFun(x,ell,dx,dy):
  r=np.sqrt(ell**2-dy**2)/dx
  return r-np.sinh(x)/x
# .......................................................... catenary
def catenary(x0,y0,x1,y1,ell):
  if x0>x1:
    x0,x1=x1,x0
    y0,y1=y1,y0
  dx=x1-x0
  dy=y1-y0
  dist=np.sqrt(dx**2+dy**2)
  if dist>=ell:
    print('Catenary not possible!')
    exit()
  xav=(x0+x1)/2.0
  yav=(y0+y1)/2.0
  A0=0.001
  A=fsolve(CateFun,A0,args=(ell,dx,dy))[0]
  aa=abs(0.5*dx/A)
  bb=xav-aa*np.arctanh(dy/ell)
  cc=yav-0.5*ell/np.tanh(A)
  return [aa,bb,cc]
# ..................................................................
a,b,c=catenary(x0,y0,x1,y1,length)
dx=x1-x0
xx=[x0]
yy=[y0]
for i in range(1,20):
  xi=x0+dx*i/20.0
  xx.append(xi)
  yy.append(a*np.cosh((xi-b)/a)+c)
xx.append(x1)
yy.append(y1)
plt.gca().set_aspect('equal')
plt.plot(xx,yy)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
plt.savefig('catenary01.pdf',format='pdf',bbox_inches='tight')
plt.show()





