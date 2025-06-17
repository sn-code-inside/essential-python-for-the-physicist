#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# .................................... Create Figure and Set y Limits
fig,ax=plt.subplots(figsize=(10,6))
ax.set(ylim=(-1,1))
# ................................................... Define Function
def func(x):
  return np.sin(8*x)*np.exp(-0.1*x)
# .................................. Create Initial x Values and Line
x=np.arange(0,10,0.01)
line,=ax.plot(x,func(x))
# ................................................ Animation Function
def animate(i):
  xx=x+i/100
  line.set_xdata(xx)
  line.set_ydata(func(xx))
  ax.set(xlim=(xx[0],xx[999]))
  return line,
# .................................................... Show Animation
ani=animation.FuncAnimation(fig,animate,interval=20) 
plt.show()




