#!/usr/bin/env python3
import numpy as np
from tkinter import *
# ............................................... initialize graphics
root=Tk()
root.title("Rotating Square")
# ............................................................ canvas
cw=ch=600
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# .............................................................. data
Ox=ch/2
Oy=cw/2
r=200
alpha=0
delta=np.pi/2.0
dAlpha=np.radians(0.5)
corners=8*[0.5]
delay=10
# ......................................................... main loop
while True:
  canvas.delete(ALL)
  canvas.create_polygon(corners,fill='red')
  canvas.update()
  for i in range(0,4):
    corners[2*i]=Ox+r*np.cos(alpha+i*delta)
    corners[2*i+1]=Oy-r*np.sin(alpha+i*delta)
    alpha+=dAlpha
    canvas.after(delay)







  
