#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
# ................................... functions
x=np.linspace(1.0,20.0,20)
y1=x**2
y2=np.sqrt(x)
# ........................................
plt.figure(figsize=(10,8))
# ................................... subplot 1
plt.subplot(2,2,1)
plt.plot(x,y1,'ro')
plt.plot(x,y2,'bo')
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('linear',fontsize=16)
plt.ylabel('linear',fontsize=16)
plt.tight_layout()
plt.ylim(-10,420)
plt.xlim(0,21)
# ................................... subplot 2
plt.subplot(2,2,2)
plt.plot(x,y1,'ro')
plt.plot(x,y2,'bo')
plt.grid(True)
plt.yscale('log')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('linear',fontsize=16)
plt.ylabel(r'$\log$',fontsize=20)
plt.tight_layout()
plt.ylim(0.8,500)
plt.xlim(-0.8,21)
# ................................... subplot 3
plt.subplot(2,2,3)
plt.plot(x,y1,'ro')
plt.plot(x,y2,'bo')
plt.grid(True)
plt.xscale('log')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel(r'$\log$',fontsize=20)
plt.ylabel('linear',fontsize=16)
plt.tight_layout()
plt.ylim(-10.8,420)
plt.xlim(0.8,22)
# ................................... subplot 4
plt.subplot(2,2,4)
plt.plot(x,y1,'ro')
plt.plot(x,y2,'bo')
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel(r'$\log$',fontsize=20)
plt.ylabel(r'$\log$',fontsize=20)
plt.tight_layout()
plt.ylim(0.8,500)
plt.xlim(0.8,25)
#
plt.savefig('LogPlot0.pdf',format='pdf',dpi=1000)
plt.show()
