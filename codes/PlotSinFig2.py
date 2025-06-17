#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
#
x=np.linspace(0,2*np.pi,50)
y = np.sin(x)
plt.plot(x, y)
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel(r'$\sin(x)$',fontsize=24)
plt.xlabel(r'$x/{\rm rad}$',fontsize=24)
plt.tight_layout()
plt.savefig('SineGrid.pdf',format='pdf',\
  dpi=1000)
plt.show()




