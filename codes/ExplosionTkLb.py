#!/usr/bin/env python3
from tkinter import *
import numpy as np
from scipy.integrate import odeint
import time
# .................................................. Global variables
RunAll=True
RunIter=False
ButtWidth=20
scale=5.0e7          # px/m
cw=ch=900            # px
cycle=20             # ms
dt=1.0e-11           # s
Ox=Oy=cw/2
# ............................................................ Origin
Ox=cw/2
Oy=ch/2
# ............................................... Start/Stop function
def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StartButton['text']='Stop'
  else:
    StartButton['text']='Restart'
# ..................................................... Exit function
def StopAll():
  global RunAll
  RunAll=False
# ....................................................... root window
root=Tk()
root.title('Coulomb Explosion')
# ............................................................ canvas
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# ........................................................... toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ............................................................ buttons
nr=0
StartButton=Button(toolbar,text='Start',command=StartStop,width=11)
StartButton.grid(row=nr,column=0,sticky=W)
nr+=1
CloseButton=Button(toolbar, text='Exit', command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,sticky=W)
nr+=1
# ............................................................ labels
TimeLab=Label(toolbar,text='{:08} ps'.format(0))
TimeLab.grid(row=nr,column=0,sticky=N)
nr+=1
RadLab=Label(toolbar,text='{:08} nm'.format(100))
RadLab.grid(row=nr,column=0,sticky=N)
# .......................................
const=3.47e5
r=1.0e-7           # m     initial cluster radius
v=0.0              # m/s   initial velocity
y=[r,v]            # initial values
t=[0,dt]
rr=r*scale         # px initial radius on canvas
# .............................................................. dfdt
def dfdt(yInp,t):
  r,vel=yInp
  acc=const/r
  derivs=[vel,acc]
  return derivs
# ........................................... numerical time interval
count=0
tt=0.0
while RunAll:
  StartIter=time.time()
  # ..................................................... draw bodies
  canvas.delete(ALL)
  canvas.create_oval(Ox-rr,Oy-rr,Ox+rr,Oy+rr,fill='blue',outline='blue')
  canvas.update()
  # .......................................................... motion
  if RunIter:
    # ..................................................... next step
    psoln = odeint(dfdt,y,t)
    y=psoln[1,:]
    r,v=y
    rr=r*scale
    tt+=dt
  # .......................................................... labels
  count+=1
  if count%20==0:
    count=0
    TimeLab['text']='{:11.2f} ps'.format(tt*1.e12)
    RadLab['text']='{:11.2f} nm'.format(r*1.0e9)
  # .................................................. cycle duration
  elapsed=int((time.time()-StartIter)*1000.0)
  canvas.after(cycle-elapsed)
root.destroy()
  
