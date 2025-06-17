#!/usr/bin/env python3
import numpy as np
# .......................................... Ask for Data and Convert
answ=input('Type a, b and c separated by spaces: ')
astr,bstr,cstr=answ.split()
a,b,c=float(astr),float(bstr),float(cstr)
# .......................................... Solve Quadratic Equation
delta=b*b-4*a*c
if delta>=0:
	dd=np.sqrt(delta)
else:
	dd=np.sqrt(-delta)*1j
x1=(-b-dd)/(2*a)
x2=(-b+dd)/(2*a)
print('x1 = ',x1)
print('x2 = ',x2)


