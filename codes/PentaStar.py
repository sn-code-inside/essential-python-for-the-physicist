#!/usr/bin/env python3
from tkinter import Canvas,Tk
import numpy as np
#
cw=ch=400
Ox=Oy=cw/2
# ..................................... create root window and canvas
root=Tk()
root.title('Star')
canvas=Canvas(root,width=cw,height=cw,background='blue')
canvas.grid(row=0,column=0)
# ................................................. Pentagon Vertices
alpha=np.pi/2
dAlpha=2*np.pi/5
r=cw/2
poly=[]
for i in range(5):
  poly.extend([Ox-r*np.cos(alpha),Oy-r*np.sin(alpha)])
  alpha+=dAlpha
# .................................................... Star Perimeter
star=[]
for i in range (5):
  j=(i*4)%10
  star.extend(poly[j:j+2])
# ......................................................... Draw Star
canvas.create_polygon(star,fill='yellow')
rr=r*0.38
canvas.create_oval(Ox-rr,Oy-rr,Ox+rr,Oy+rr,fill='yellow',outline='yellow')
canvas.update()
# ...................................................................
root.mainloop()
  
