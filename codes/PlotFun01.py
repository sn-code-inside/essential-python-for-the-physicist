#!/usr/bin/env python3
#
from numpy import *
import matplotlib.pyplot as plt
#
def fun(x):
  return 5.0+4.0*x-exp(x)
#
x=arange(-6.0,4.0,0.1)
plt.grid(True)
plt.plot([-6.0,4.0],[0.0,0.0],color='black')
plt.plot(x,fun(x))
plt.savefig('RootFind01.eps', format='eps', dpi=1000)
plt.show()




