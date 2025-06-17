#!/usr/bin/env python3
from vpython import *
import numpy as np
from scipy.integrate import odeint
scene.width=scene.height=800
scene.background=color.black
scene.title='Coulomb explosion'
# ................................................ Start/Stop function
def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StopButton.text='Standby'.center(20)
  else:
    StopButton.text='Expand'.center(20)
# ........................................... time reversal function
def Reset():
  global r,r0,tt,v,v0,y
  r=r0
  v=v0
  tt=0.0
  y=[r,v]
# ................................................. buttons and label
StopButton=button(bind=StartStop,text='Expand'.center(20))
ResetButton=button(bind=Reset,text='Reset'.center(20))
RadiusLabel=wtext(text='{:08} nm'.format(100))
TimeLabel=wtext(text='{:11.2f} ps'.format(0))
# .................................................. Global variables
RunIter=False
dt=1.0e-11           # s
# .................................................. numerical values
const=3.47e5
r=r0=1.0e-7        # m     initial cluster radius
v=v0=0.0           # m/s   initial velocity
y=[r,v]            # initial values
t=[0,dt]
# ........................................................... spheres
cluster=sphere(pos=vec(0,0,0),radius=r,color=color.white)
corner1=sphere(pos=vec(-1.0e-5,-1.0e-5,0),radius=1.e-8)
corner2=sphere(pos=vec(1.0e-5,1.0e-5,0),radius=1.e-8)
scene.autoscale=False
# .............................................................. dfdt
def dfdt(yInp,t):
  r,vel=yInp
  acc=const/r
  derivs=[vel,acc]
  return derivs
# ......................................................... main loop
count=0
tt=0.0
while True:
  rate(50)
  # .................................................... draw cluster
  cluster.radius=r
  count+=1
  if count%20==0:
    RadiusLabel.text='{:11.2f} nm'.format(r*1.0e9)
    TimeLabel.text='{:11.2f} ps'.format(tt*1.0e12)
  # ..................................................... Run/Standby
  if RunIter:
    psoln = odeint(dfdt,y,t)
    y=psoln[1,:]
    r,v=y
    tt+=dt
  
