#!/usr/bin/env python3
from tkinter import *
import numpy as np
from scipy.integrate import odeint
import time
# .................................................. Global variables
RunAll=True
RunMotion=False
ButtWidth=20
scale=5.0e7                # px/m
cw=ch=900                  # px
Ox=Oy=cw/2
r_max=Ox*np.sqrt(2)/scale
tau=20                     # frame period (ms)
dt=1.0e-11                 # numerical integration step (s)
t=[0,dt]                   # time interval for odeint()
# ..................................................... Initial State
const=3.47e5
r=1.0e-7           # m     initial cluster radius
v=0.0              # m/s   initial velocity
state=[r,v]        # initial state
# ........................................................ Start/Stop
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  StartButton['text']='Stop' if RunMotion else 'Restart'
  CloseButton['state']=DISABLED if RunMotion else NORMAL
# ........................................................... StopAll
def StopAll():
  global RunAll
  RunAll=False
# ............................................................. circ
def circ(r):
  global Ox,Oy,scale
  rr=scale*r
  return [Ox-rr,Oy-rr,Ox+rr,Oy+rr]
# .............................................................. dfdt
def dfdt(state,t):
  global const
  r,vel=state
  acc=const/r
  derivs=[vel,acc]
  return derivs
# ............................ Create Root Window, Canvas and Toolbar
root=Tk()
root.title('Coulomb Explosion')
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ............................................ Add Buttons to Toolbar
nr=0
StartButton=Button(toolbar,text='Start',command=StartStop,width=11)
StartButton.grid(row=nr,column=0,sticky=W)
nr+=1
CloseButton=Button(toolbar, text='Exit', command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,sticky=W)
nr+=1
# ........................................................ Add Labels
TimeLab=Label(toolbar,text=f't={0:08} ps')
TimeLab.grid(row=nr,column=0,sticky=N)
nr+=1
RadLab=Label(toolbar,text=f'r={100:08} nm')
RadLab.grid(row=nr,column=0,sticky=N)

# ............................................ Create Initial Cluster
cluster=canvas.create_oval(circ(r),fill='blue',outline='blue')
# ........................................... numerical time interval
count=0
tt=0.0
while RunAll:
  StartIter=time.time()
  # ........................................... Update Helium Cluster
  canvas.coords(cluster,circ(state[0]))
  canvas.update()
  # .......................... Update Cluster Radius and Elapsed Time
  if RunMotion:
    psoln = odeint(dfdt,state,t)
    state=psoln[1,:]
    tt+=dt
    # ................................................. Update Labels
    count+=1
    if count%20==0:
      count=0
      TimeLab['text']=f't={tt*1.0e12:11.2f} ps'
      RadLab['text']=f'r={state[0]*1.0e9:11.2f} nm'
    # ...........................................................
    if state[0]>r_max:
      state=[1.0e-7,0.0]
  # .................................................. cycle duration
  elapsed=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-elapsed)
root.destroy()
  
