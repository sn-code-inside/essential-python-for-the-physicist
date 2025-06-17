#!/usr/bin/env python3
import numpy as np
import time
from tkinter import *
from scipy.integrate import odeint
# ...................................................................
RunAll=True
RunMotion=False
cw=800
ch=400
O1=200
O2=400
O3=600
Oy=ch/2.0
rad=10
tau=20
omega2=1
tau=20
# .............................................. function StartStop()
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  StartButton['text']='Stop' if RunMotion else 'Restart'
  CloseButton['state']=DISABLED if RunMotion else NORMAL
# ................................................ function StopAll()
def StopAll():
  global RunAll
  RunAll=False
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
# .......................................................... function
def f(y,t):
  x1,v1,x2,v2,x3,v3=y
  a1=-2*omega2*x1+omega2*x2
  a2=omega2*x1-2*omega2*x2+omega2*x3
  a3=omega2*x2-2*omega2*x3
  return [v1,a1,v2,a2,v3,a3]
#..................................................... initial values
x1=100
v1=x2=v2=x3=v3=0
y=[x1,v1,x2,v2,x3,v3]
t=[0.0,0.05]
# .............................................................. loop
while RunAll:
  StartIter=time.time()
  canvas.delete(ALL)
  canvas.create_line(0,Oy,cw,Oy,fill='black')
  canvas.create_oval(O1+x1-rad,Oy-rad,O1+x1+rad,Oy+rad,fill='red')
  canvas.create_oval(O2+x2-rad,Oy-rad,O2+x2+rad,Oy+rad,fill='red')
  canvas.create_oval(O3+x3-rad,Oy-rad,O3+x3+rad,Oy+rad,fill='red')
  canvas.update()
  if RunMotion:
    psoln = odeint(f,y,t)
    y=psoln[1,:]
    x1,v1,x2,v2,x3,v3=y
  ElapsTime=int((time.time()-StartIter)*1000)
  canvas.after(tau-ElapsTime)
root.destroy()
