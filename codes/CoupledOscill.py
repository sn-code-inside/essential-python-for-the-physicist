#!/usr/bin/env python3
import numpy as np
import time
from tkinter import *
from scipy.integrate import odeint
# ......................................................... Constants
RunAll=True
RunMotion=False
cw,ch=800,400
EquilPos=[0.2,0.4,0.6]
Oy=ch/2.0
scale=1000
rad=10
tau=20
omega2=1
# ......................................................... StartStop
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  StartButton['text']='Stop' if RunMotion else 'Restart'
  CloseButton['state']=DISABLED if RunMotion else NORMAL
# ........................................................... StopAll
def StopAll():
  global RunAll
  RunAll=False
# .............................................................. dfdt
def dfdt(state,t):
  x1,x2,x3,v1,v2,v3=state
  a1=-2*omega2*x1+omega2*x2
  a2=omega2*x1-2*omega2*x2+omega2*x3
  a3=omega2*x2-2*omega2*x3
  return [v1,v2,v3,a1,a2,a3]
# .............................................................. circ
def circ(x):
  global Oy,rad,scale
  xx=scale*x
  return [xx-rad,Oy-rad,xx+rad,Oy+rad]
# ............................ Create Root Window, Canvas and Toolbar
root=Tk()
root.title('Coupled Oscillators')
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ............................................ add buttons to toolbar
ButtWidth=10
StartButton=Button(toolbar,text='Start',command=StartStop,width=ButtWidth)
StartButton.grid(row=0,column=0)
CloseButton=Button(toolbar,text='Exit',command=StopAll,width=ButtWidth)
CloseButton.grid(row=1,column=0)
#................................ Initial Values and Integration Step
state=[0.1,0,0,0,0,0]
t=[0.0,0.05]
# .................................................... Animation Loop
while RunAll:
  StartIter=time.time()
  # ................................................... Update Canvas
  canvas.delete(ALL)
  canvas.create_line(0,Oy,cw,Oy,fill='black')
  for i,pos in enumerate(EquilPos):
    canvas.create_oval(circ(pos+state[i]),fill='red')
  canvas.update()
  # ................................................... Update Motion
  if RunMotion:
    psoln=odeint(dfdt,state,t)
    state=psoln[1,:]
  # ......................................... Control Animation Speed
  ElapsTime=int((time.time()-StartIter)*1000)
  canvas.after(tau-ElapsTime)
root.destroy()
