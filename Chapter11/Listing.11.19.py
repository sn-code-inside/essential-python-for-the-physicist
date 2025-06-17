#!/usr/bin/env python3
from vpython import *
from scipy.integrate import odeint
scene.width=800
scene.height=200
scene.background=color.white
# ...................................................................
RunIter=False
# .............................................. function StartStop()
def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StopButton.text='Standby'.center(20)
  else:
    StopButton.text='Restart'.center(20)
# ............................................................ button
StopButton=button(bind=StartStop,text='Start'.center(20))
# ...................................................................
rad=30
SpringRad=15
omega2=1
# ...................................................................
Delta=200
O1=-Delta
O2=0
O3=Delta
x1=100
x2=x3=0
v1=v2=v3=0
wall1=box(pos=vec(-2*Delta,0,0),size=vec(1,200,100),color=vec(0.7,0.7,1))
wall2=box(pos=vec(2*Delta,0,0),size=vec(1,200,100),color=vec(0.7,0.7,1))
ball1=sphere(pos=vec(O1+x1,0,0),radius=rad,color=color.red)
ball2=sphere(pos=vec(O2,0,0),radius=rad,color=color.red)
ball3=sphere(pos=vec(O3,0,0),radius=rad,color=color.red)
spring1=helix(pos=vec(-400,0,0),length=Delta+x1-rad,\
  radius=SpringRad,coils=15)
spring2=helix(pos=vec(O1+x1+rad,0,0),length=Delta-x1-2*rad,\
  radius=SpringRad,coils=15)
spring3=helix(pos=vec(O2+x2+rad,0,0),length=Delta-x2-2*rad,\
  radius=SpringRad,coils=15)
spring4=helix(pos=vec(O3+x3+rad,0,0),length=Delta-x3-2*rad,\
  radius=SpringRad,coils=15)
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
while True:
  rate(50)
  ball1.pos.x=O1+x1
  ball2.pos.x=O2+x2
  ball3.pos.x=O3+x3
  spring1.length=Delta+x1-rad
  spring2.pos.x=O1+x1+rad
  spring2.length=Delta+x2-x1-2*rad
  spring3.pos.x=O2+x2+rad
  spring3.length=Delta+x3-x2-2*rad
  spring4.pos.x=O3+x3+rad
  spring4.length=Delta-x3-rad
  if RunIter:
    psoln=odeint(f,y,t)
    y=psoln[1,:]
    x1,v1,x2,v2,x3,v3=y
