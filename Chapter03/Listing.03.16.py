#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
#
xlist=np.arange(-4,4.05,0.1)
ylist=np.tanh(xlist)
plt.plot(xlist,ylist)
plt.show()
