#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
#
x = np.arange(0,6.4,0.1);
y = np.sin(x)
plt.plot(x, y)
plt.grid(True)
plt.ylabel('$\sin(x)$',fontsize=24)
plt.xlabel('$x/{\\rm rad}$',fontsize=24)
plt.show()




