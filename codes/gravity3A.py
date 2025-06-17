#!/usr/bin/env python3
from tkinter import *
import numpy as np
from scipy.integrate import odeint
import time
# .................................................. Global variables
RunAll=True
RunIter=False
ButtWidth=20
scale=5.0e-6         # px/m
cw=ch=900
cycle=20             # ms
dt=1200              # s
G=6.67408e-11
# ............................................................ Origin
Ox=cw/2
Oy=ch/2
# ............................................... Start/Stop function
def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StartButton["text"]="Stop"
  else:
    StartButton["text"]="Restart"
# ..................................................... Exit function
def StopAll():
  global RunAll
  RunAll=False
# ..................................................... Class CelBody
class AstroBody:
  def __init__(self,mass,radius,x,y,vx,vy,color):
    self.m=mass
    self.rad=radius
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    self.col=color
    self.image=canvas.create_oval(Ox+int(scale*self.x-self.rad),\
      int(Oy-scale*self.y+self.rad),int(Ox+scale*self.x+self.rad),\
        int(Oy-scale*self.y-self.rad),fill=self.col,outline=self.col)
   # ....................................................... move body
  def redraw(self):
    canvas.coords(self.image,Ox+scale*self.x-self.rad,\
      Oy-scale*self.y+self.rad,Ox+scale*self.x+self.rad,\
        Oy-scale*self.y-self.rad)
# ....................................................... root window
root=Tk()
root.title('Gravity 3')
# ............................................................ canvas
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ........................................................... toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ............................................................ buttons
nr=0
StartButton=Button(toolbar,text="Start",command=StartStop,width=11)
StartButton.grid(row=nr,column=0,sticky=N)
nr+=1
CloseButton=Button(toolbar, text="Exit", command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,sticky=N)
# .................................................... create bodies
bd=[]
bd.append(AstroBody(1.3e22,8.0,-2.137e6,0.0,0.0,-19.4,'red'))#  Pluto
bd.append(AstroBody(1.6e21,6.0,1.736e7,0.0,0.0,158,'blue'))#  Charon
bd.append(AstroBody(5.0e16,4,6.486e7,0.0,0.0,122.6,'blue'))# Hydra
nB=len(bd)
# ........................................ coordinates and barycenter
canvas.create_line(0,Oy,cw,Oy,fill="black")
canvas.create_line(Ox,0,Ox,ch,fill="black")
# ............................................................ masses
masses=[]
for zz in bd:
  masses.append(zz.m)
# .................................................... initial values
y=[]
for zz in bd:
  y.append(zz.x)
  y.append(zz.y)
  y.append(zz.vx)
  y.append(zz.vy)
# ........................................................ value list
t=[0.0,dt]
# .......................................................... function
def dfdt(yInp,t,mm):
  nB=len(mm)
  x=yInp[0::4]
  y=yInp[1::4]
  distx=(np.tile(x,(len(x),1))).T-x
  disty=(np.tile(y,(len(y),1))).T-y
  alpha=np.arctan2(disty,distx)
  r2=np.square(distx)+np.square(disty)
  np.fill_diagonal(r2,1.0)
  ff=np.divide(G,r2)
  np.fill_diagonal(ff,0.0)
  fx=ff*np.cos(alpha)
  fy=ff*np.sin(alpha)
  fx=(fx.T*mm).T
  fy=(fy.T*mm).T
  ax=fx.sum(axis=0)
  ay=fy.sum(axis=0)
  derivs=[0]*len(yInp)
  derivs[::4]=yInp[2::4]     # vx
  derivs[1::4]=yInp[3::4]    # vy
  derivs[2::4]=ax 
  derivs[3::4]=ay
  return derivs
# ........................................... numerical time interval
while RunAll:
  StartIter=time.time()
  # ..................................................... draw bodies
  for zz in bd:
    zz.redraw()
    canvas.update()
  # .......................................................... motion
  if RunIter:
    # ..................................................... next step
    psoln = odeint(dfdt,y,t,args=(masses,))
    y=psoln[1,:]
    for i,zz in enumerate(bd):
      zz.x=y[4*i]
      zz.y=y[4*i+1]
      zz.vx=y[4*i+2]
      zz.vy=y[4*i+3]
  # ................................................ cycle duration
  ElapsTime=int((time.time()-StartIter)*1000.0)
  canvas.after(cycle-ElapsTime)
root.destroy()
  
