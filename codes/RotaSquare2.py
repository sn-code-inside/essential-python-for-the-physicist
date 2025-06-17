#!/usr/bin/env python3
import numpy as np
from tkinter import *
# ..................................................................
RunAll=True
# ........................................................ functions
def StopAll():
  global RunAll
  RunAll=False
def accel():
  global dAlpha
  dAlpha*=1.2
def decel():
  global dAlpha
  dAlpha/=1.2
# ............................................... initialize graphics
root=Tk()
root.title("Rotating Square with Buttons")
# ............................................................ canvas
cw=ch=600
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ........................................................... toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ........................................................... buttons
nr=0
AccelButton=Button(toolbar,text="Accelerate",command=accel,width=11)
AccelButton.grid(row=nr,column=0,sticky=W)
nr+=1
DecelButton=Button(toolbar,text="Decelerate",command=decel,width=11)
DecelButton.grid(row=nr,column=0,sticky=W)
nr+=1
CloseButton=Button(toolbar,text="Exit",command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,sticky=W)
nr+=1
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
while RunAll:
  if not RunAll:
    break
  canvas.delete(ALL)
  canvas.create_polygon(corners,fill='red')
  canvas.update()
  for i in range(0,4):
    corners[2*i]=Ox+r*np.cos(alpha+i*delta)
    corners[2*i+1]=Oy-r*np.sin(alpha+i*delta)
    alpha+=dAlpha
    canvas.after(delay)
canvas.destroy()






  
