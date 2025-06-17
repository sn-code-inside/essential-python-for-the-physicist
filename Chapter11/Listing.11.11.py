#!/usr/bin/env python3
from vpython import *
# ..................................................... create canvas
scene.title='Buttons and Entries'
scene.background=vector(1,1,1)
scene.width=1000
scene.height=600
# ......................................................... variables
bw=8
bh=5
bdepth=1
thick=0.1
rad=0.2
vx=3
vy=8
dt=0.01
g=vector(0,-9.8,0)
# ............................................. interaction variables
RunIter=False
ButtonWidth=20
global MyText
# ..........................................................functions
def incvx():
  ball.velocity.x=ball.velocity.x*1.2
def decvx():
  ball.velocity.x=ball.velocity.x/1.2
def ReadEntry(s):
  global MyText
  MyText=text(pos=vector(0,1,0),text=s.text,height=0.3,\
    color=vector(0.3,0.8,0))
def EraseText():
  global MyText
  MyText.visible=False
def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StopButton.text='Stop'.center(ButtonWidth)
  else:
    StopButton.text='Restart'.center(ButtonWidth)
# .......................................... buttons and input window
AccelButton=button(bind=incvx,text='Faster!')
scene.append_to_caption(' ')
DecelButton=button(bind=decvx,text='Slower!')
scene.append_to_caption('\n')
StopButton=button(bind=StartStop,text='Start'.center(ButtonWidth))
scene.append_to_caption('\n\n')
LabelText=wtext(text='Write here: ')
EntryWindow=winput(bind=ReadEntry,type='string',width=200)
scene.append_to_caption(' ')
EraseButton=button(bind=EraseText,text='Erase')
# .......................................................... add lamp
lamp=local_light(pos=vector(1.2*bw,0,4*bdepth),color=color.white)
# ........................................................ boundaries
LeftWall=box(pos=vector(-bw/2-thick/2,0,0),length=thick,\
  height=bh+2*thick,width=bdepth,color=vector(0.5,0.5,1))
RightWall=box(pos=vector(bw/2+thick/2,0,0),length=thick,\
  height=bh+2*thick,width=bdepth,color=vector(0.5,0.5,1))
floor=box(pos=vector(0,-bh/2-thick/2,0),length=bw,\
  height=thick,width=bdepth,color=vector(0.5,0.5,1))
ceiling=box(pos=vector(0,bh/2+thick/2,0),length=bw,\
  height=thick,width=bdepth,color=vector(0.5,0.5,1))
# .............................................................. ball
ball=sphere(pos=vector(-bw/2+rad,-bh/2+rad,0),radius=rad,\
  make_trail=True,retain=50,color=color.red,\
    velocity=vector(vx,vy,0))
# ......................................................... main loop
while True:
  rate(50)
  if RunIter:
    ball.pos=ball.pos+ball.velocity*dt+0.5*g*dt**2
    ball.velocity=ball.velocity+g*dt
    # ................... is the ball bouncing on the canvas borders?
    if ball.pos.x>=(bw/2-rad):
      ball.velocity.x=-abs(ball.velocity.x)
    elif ball.pos.x<=-(bw/2-rad):
      ball.velocity.x=abs(ball.velocity.x)
    elif ball.pos.y>=bh/2-rad:
      ball.velocity.y=-abs(ball.velocity.y)
    elif ball.pos.y<=-(bh/2-rad):
      ball.velocity.y=abs(ball.velocity.y)
