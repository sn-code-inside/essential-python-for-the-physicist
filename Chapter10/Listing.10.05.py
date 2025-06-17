#!/usr/bin/env python3
from tkinter import *
import numpy as np
from scipy.integrate import odeint
import time
# .................................................. Global variables
RunAll=True
RunMotion=False
ButtWidth=20
scale=5.0e-6         # px/m
cw=ch=900            # px
Ox=Oy=cw/2
TrailLength=400
tau=20               # ms
t=[0,600]            # s
G=6.67408e-11        # m^3/(kg s^2)
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
# ................................................ Canvas Coordinates
def meter2pix(pos):
  global Ox,Oy,scale
  for i,xy in enumerate(pos):
    pos[i]=Ox+scale*xy if i%2==0 else Oy-scale*xy
  return pos
# ................................................ Circle Coordinates
def circ(pos,radius):
  global Ox,Oy,scale
  xx,yy=meter2pix(pos)
  return [xx-radius,yy-radius,xx+radius,yy+radius]
# ................................................... Class AstroBody
class AstroBody:
  def __init__(self,mass,radius,x,y,vx,vy,color):
    self.m=mass
    self.rad=radius
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    self.col=color
    self.image=canvas.create_oval(circ([self.x,self.y],self.rad),\
      fill=self.col,outline=self.col)
    self.trail=meter2pix([self.x,self.y])*TrailLength
    self.TrailImg=canvas.create_line(self.trail,fill=self.col)
   # ....................................................... move body
  def redraw(self):
    canvas.coords(self.image,circ([self.x,self.y],self.rad))
    xx,yy=meter2pix([self.x,self.y])
    if np.linalg.norm([xx-self.trail[-2],yy-self.trail[-1]])>10:
      del self.trail[:2]
      self.trail.extend([xx,yy])
    canvas.coords(self.TrailImg,self.trail)
# ............................ Create Root Window, Canvas and Toolbar
root=Tk()
root.title('Pluto Moons')
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ................................................... Toolbar Buttons
nr=0
StartButton=Button(toolbar,text='Start',command=StartStop,width=11)
StartButton.grid(row=nr,column=0,sticky=N)
nr+=1
CloseButton=Button(toolbar, text='Exit', command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,sticky=N)
# .................................................... create bodies
body=[]
body.append(AstroBody(1.3e22,8.0,-2.137e6,0.0,0.0,-19.4,'red'))#  Pluto
body.append(AstroBody(1.6e21,6.0,1.736e7,0.0,0.0,158,'blue'))#  Charon
body.append(AstroBody(7.5e14,4,4.2656e7,0.0,0.0,151,'blue'))#  Styx
body.append(AstroBody(5.0e16,4,4.8694e7,0.0,0.0,142,'blue'))# Nix
body.append(AstroBody(1.6e16,4,5.7783e7,0.0,0.0,130,'blue'))# Kerberos
body.append(AstroBody(5.0e16,4.0,6.486e7,0.0,0.0,123,'blue'))# Hydra
nB=len(body)
# ......................................... Move to Barycenter System
mtot=sum(bd.m for bd in body)
cx=sum(bd.x*bd.m for bd in body)/mtot
cy=sum(bd.y*bd.m for bd in body)/mtot
cvx=sum(bd.vx*bd.m for bd in body)/mtot
cvy=sum(bd.vy*bd.m for bd in body)/mtot
for bd in body:
  bd.x-=cx
  bd.y-=cy
  bd.vx-=cvx
  bd.vy-=cvy
# ...................................................... x and y Axes
canvas.create_line(0,Oy,cw,Oy,fill='black')
canvas.create_line(Ox,0,Ox,ch,fill='black')
# ............................................. Masses of the Bodies
masses=[bd.m for bd in body]
# ..................................................... Initial State
state=[]
for bd in body:
  state.extend([bd.x,bd.y])
for bd in body:
  state.extend([bd.vx,bd.vy])
# .......................................................... function
def dfdt(state,t,mm):
  nB=len(mm)
  x=state[0:2*nB:2]
  y=state[1:2*nB:2]
  distx=(np.tile(x,(len(x),1))).T-x
  disty=(np.tile(y,(len(y),1))).T-y
  alpha=np.arctan2(disty,distx)
  r2=np.square(distx)+np.square(disty)
  np.fill_diagonal(r2,1.0) #   prevent division by zero at Line 90
  force=np.divide(G,r2)
  np.fill_diagonal(force,0.0)
  fx=force*np.cos(alpha)
  fy=force*np.sin(alpha)
  fx=(fx.T*mm).T
  fy=(fy.T*mm).T
  ax=fx.sum(axis=0)
  ay=fy.sum(axis=0)
  derivs=[0]*len(state)
  derivs[0:2*nB]=state[2*nB:]   # velocities
  derivs[2*nB::2]=ax
  derivs[2*nB+1::2]=ay
  return derivs
# .................................................... Animation Loop
while RunAll:
  StartIter=time.time()
  # ........................................... Draw Bodies on Canvas
  for bd in body:
    bd.redraw()
  canvas.update()
  # ..................................................... Move Bodies
  if RunMotion:
    solution = odeint(dfdt,state,t,args=(masses,))
    state=solution[1,:]
    for i,bd in enumerate(body):
      bd.x,bd.y=state[2*i],state[2*i+1]
      bd.vx,bd.vy=state[2*nB+2*i],state[2*nB+1+2*i]
  # ................................................ cycle duration
  elapsed=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-elapsed)
root.destroy()
  
