#!/usr/bin/env python3
import numpy as np
from vpython import *
from scipy.integrate import odeint
# ...................................................................
scene.width=1000
scene.height=1000
scene.background=color.black
scene.title='Pluto-Charon System'
scene.lights=[]
distant_light(direction=vec(-1,0,0),color=color.white)
# ............................................ gravitational constant
G=6.67408e-11
# ........................... "real" time interval between two frames
dt=100                # s
# ............................................ Data in Pluto's system
mp=1.3e22    # kg    Pluto
xp=0         # m      
vyp=0        # m/s
mc=1.6e21    # kg    Charon
xc=1.9e7     # m
vyc=200      # m/s
# ......................................... move to barycenter system
mtot=mp+mc
xb=(mp*xp+mc*xc)/mtot
vyb=(mp*vyp+mc*vyc)/mtot
xp-=xb
vyp-=vyb
xc-=xb
vyc-=vyb
baryc=sphere(pos=vec(0,0,0),radius=1e5,color=color.yellow)
# ............................................................. Pluto
pluto=sphere(mass=mp,pos=vec(xp,0,0),radius=1.18e6,color=color.white,\
  make_trail=True,interval=2,retain=50,vel=vec(0,vyp,0))
# ............................................................ Charon
charon=sphere(mass=mc,pos=vec(xc,0,0),radius=6.06e5,color=color.white,\
  make_trail=True, interval=1,retain=100,vel=vec(0,vyc,0))
# ...................................... initial conditions and times
y=[pluto.pos.x,pluto.pos.y,pluto.vel.x,pluto.vel.y,charon.pos.x,\
  charon.pos.y,charon.vel.x,charon.vel.y]
t=[0.0,dt]
# .......................................................... function
def dfdt(yInp,t):
  global G
  x1,y1,vx1,vy1,x2,y2,vx2,vy2=yInp
  distx=x2-x1
  disty=y2-y1
  r2=distx**2+disty**2
  alpha=np.arctan2(disty,distx)
  f=G/r2
  fx=f*np.cos(alpha)
  fy=f*np.sin(alpha)
  ax1=fx*charon.mass
  ay1=fy*charon.mass
  ax2=-fx*pluto.mass
  ay2=-fy*pluto.mass
  return [vx1,vy1,ax1,ay1,vx2,vy2,ax2,ay2]
# ......................................................... main loop
while True:
  rate(400)
  psoln=odeint(dfdt,y,t)
  y=psoln[1,:]
  pluto.pos.x,pluto.pos.y,pluto.vel.x,pluto.vel.y,charon.pos.x,\
    charon.pos.y,charon.vel.x,charon.vel.y=y









