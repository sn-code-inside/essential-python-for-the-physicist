#!/usr/bin/env python3
from vpython import *
scene.title='Precession'
scene.width=800
scene.height=600
scene.background=vector(1,1,1)
# ................................................ Initial conditions
s=2
theta=pi/6
phi=0.0
sy=s*cos(theta)
r=s*sin(theta)
spin=arrow(pos=vector(0,0,0),length=s,axis=vector(0,sy,r),\
  color=vector(1,1,0))
dPhi=radians(0.5)
dPsi=radians(3)
# ....................................................... Precession
while True:
  rate(50)
  spin.rotate(angle=dPsi)
  sz=r*cos(phi)
  sx=r*sin(phi)
  spin.axis=vector(sx,sy,sz)
  phi+=dPhi


