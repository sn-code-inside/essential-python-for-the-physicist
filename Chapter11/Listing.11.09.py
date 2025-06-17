#!/usr/bin/env python3
from vpython import *
# ..................................................... create canvas
scene.title='Framed ball'
scene.background=vector(1,1,1)
scene.width=1000
scene.height=600
# ......................................................... variables
rw=8
rh=5
rdepth=1
thick=0.1
rad=0.2
vx=3
vy=8
dt=0.01
g=vector(0,-9.8,0)
# .......................................................... add lamp
lamp=local_light(pos=vector(1.2*rw,0,4*rdepth),color=color.white)
# ........................................................ boundaries
LeftWall=box(pos=vector(-rw/2-thick/2,0,0),length=thick,\
  height=rh+2*thick,width=rdepth,color=vector(0.5,0.5,1))
RightWall=box(pos=vector(rw/2+thick/2,0,0),length=thick,\
  height=rh+2*thick,width=rdepth,color=vector(0.5,0.5,1))
floor=box(pos=vector(0,-rh/2-thick/2,0),length=rw,\
  height=thick,width=rdepth,color=vector(0.5,0.5,1))
ceiling=box(pos=vector(0,rh/2+thick/2,0),length=rw,\
  height=thick,width=rdepth,color=vector(0.5,0.5,1))
# .............................................................. ball
ball=sphere(pos=vector(-rw/2+rad,-rh/2+rad,0),radius=rad,\
  make_trail=True,retain=50,color=color.red,\
    velocity=vector(vx,vy,0))
# ......................................................... main loop
while True:
  rate(50)
  ball.pos=ball.pos+ball.velocity*dt+0.5*g*dt**2
  ball.velocity=ball.velocity+g*dt
  # ..................... is the ball bouncing on the canvas borders?
  if ball.pos.x>=(rw/2-rad):
    ball.velocity.x=-abs(ball.velocity.x)
  elif ball.pos.x<=-(rw/2-rad):
    ball.velocity.x=abs(ball.velocity.x)
  elif ball.pos.y>=rh/2-rad:
    ball.velocity.y=-abs(ball.velocity.y)
  elif ball.pos.y<=-(rh/2-rad):
    ball.velocity.y=abs(ball.velocity.y)
