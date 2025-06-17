#!/usr/bin/env python3
from tkinter import Tk,Canvas,E,LAST,N
import numpy as np
#
cw=400
ch=400
Ox=cw/2
Oy=ch/2
# ..................................... create root window and canvas
root=Tk()
root.title('Color Hexagon')
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ...........................................................
colors=['red','lightgreen','blue','cyan','magenta','yellow']
# ........................................................... triang1
alpha=0.0
dAlpha=np.pi/3.0
r=200.0
i=0
while i<6:
  tr=[Ox,Oy]
  j=0
  while True:
    tr.append(Ox+r*np.cos(alpha))
    tr.append(Oy-r*np.sin(alpha))
    if j==0:
      alpha+=dAlpha
      j+=1
    else:
      break
  canvas.create_polygon(tr,fill=colors[i],outline='black')
  i+=1
# ...................................................................
root.mainloop()
  
