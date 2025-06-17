#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
#
x=np.linspace(0.0,2.0,41)
plt.plot(x,x,x,np.sqrt(x),'ro',x,x**2,'g^')
plt.show()




