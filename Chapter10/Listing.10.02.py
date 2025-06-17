#!/usr/bin/env python3
from tkinter import *
import numpy as np
import time
# .................................................. Global variables
RunAll=True
GetData=RunMotion=False
ButtWidth=9
# ......................................... ............ Canvas sizes
cw=800
ch=600
# ...................................................... Start values
tau=20  #  milliseconds
m1=200
r1=40
x1=r1
y1=r1
vx1=5.0
vy1=5.0
m2=150
r2=30
x2=cw-r2
y2=r2
vx2=-5.0
vy2=5.0
# ........................................................ Class Ball
class Ball:
  def __init__(self,mass,radius,x,y,vx,vy,color):
    self.m=mass
    self.rad=radius
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    self.col=color
    self.image=canvas.create_oval(self.x-self.rad,ch-(self.y+\
      self.rad),self.x+self.rad,ch-(self.y-self.rad),\
        fill=self.col,outline=self.col)
  # ....................................................... Move Ball
  def move(self):
    self.x+=self.vx
    self.y+=self.vy
    canvas.coords(self.image,self.x-self.rad,ch-(self.y+self.rad),\
      self.x+self.rad,ch-(self.y-self.rad))
  # ........................................ Bounce on Canvas Borders
  def bounce(self):
    if (self.x+self.rad)>=cw:
      self.vx=-abs(self.vx)
      self.x=2.0*(cw-self.rad)-self.x
    elif (self.x-self.rad)<=0:
      self.vx=abs(self.vx)
      self.x=2.0*self.rad-self.x
    if (self.y+self.rad)>=ch:
      self.vy=-abs(self.vy)
      self.y=2.0*(ch-self.rad)-self.y
    elif (self.y-self.rad)<=0:
      self.vy=abs(self.vy)
      self.y=2.0*self.rad-self.y
  # ............................................... Elastic Collision
  def ElastColl(self,other):
    dx=other.x-self.x
    dy=other.y-self.y
    distsq=dx**2+dy**2
    R12sq=(self.rad+other.rad)**2
    if distsq>R12sq:
      return
    tc=0.0
    # ...................................... Adjust Overlapping Balls
    if distsq<R12sq:
      dvx=other.vx-self.vx
      dvy=other.vy-self.vy
      aa=dvx**2+dvy**2
      bbhalf=dx*dvx+dy*dvy
      cc=dx**2+dy**2-R12sq
      # ......................... Time Elapsed since 'Real' Collision
      tc=(-bbhalf-np.sqrt(bbhalf**2-aa*cc))/aa
      # .......................... Time Reversal to Collision Instant
      other.x+=tc*other.vx
      other.y+=tc*other.vy
      self.x+=tc*self.vx
      self.y+=tc*self.vy
      # .............................. Distances at Collision Instant
      dx=other.x-self.x
      dy=other.y-self.y
    # ..................................... Collision Reference Frame
    alpha=np.arctan2(dy,dx)
    csalpha=np.cos(alpha)
    snalpha=np.sin(alpha)
    SelfVelXi=self.vx*csalpha+self.vy*snalpha
    SelfVelEta=-self.vx*snalpha+self.vy*csalpha
    OtherVelXi=other.vx*csalpha+other.vy*snalpha
    OtherVelEta=-other.vx*snalpha+other.vy*csalpha
    SelfNewVelXi=((self.m-other.m)*SelfVelXi+2.0*other.m*OtherVelXi)/\
      (self.m+other.m)
    OtherNewXi=((other.m-self.m)*OtherVelXi+2.0*self.m*SelfVelXi)/\
      (self.m+other.m)
    self.vx=SelfNewVelXi*csalpha-SelfVelEta*snalpha
    self.vy=SelfNewVelXi*snalpha+SelfVelEta*csalpha
    other.vx=OtherNewXi*csalpha-OtherVelEta*snalpha
    other.vy=OtherNewXi*snalpha+OtherVelEta*csalpha
    # ...........................................................
    other.x-=tc*other.vx
    other.y-=tc*other.vy
    self.x-=tc*self.vx
    self.y-=tc*self.vy
# ........................................................ StartStop
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  StartButton['text']='Stop' if RunMotion else 'Restart'
  for wg in [CloseButton]+VarEntry:
    wg['state']=DISABLED if RunMotion else NORMAL
# ...........................................................StopAll
def StopAll():
  global RunAll
  RunAll=False
# .......................................................... ReadData
def ReadData(*arg):
  global GetData
  GetData=True
# ................................................ Create Root Window
root=Tk()
root.title('Class Collide')
root.bind('<Return>',ReadData)
# ...................................................................
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# .................................................... Create Toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
toolbar.option_add('*Font','Helvetica 11')
# ........................................................... Buttons
nr=0
StartButton=Button(toolbar,text='Start',command=StartStop,
                   width=ButtWidth)
StartButton.grid(row=nr,column=0,sticky=W)
nr+=1
CloseButton=Button(toolbar, text='Exit', command=StopAll,
                   width=ButtWidth)
CloseButton.grid(row=nr,column=0,sticky=W)
nr+=1
# ................................................... Parameter Array
params=[m1,r1,vx1,vy1,m2,r2,vx2,vy2,tau]
VarEntry=[]
VarLab=['m\u2081','r\u2081','vx\u2081','vy\u2081','m\u2082',\
  'r\u2082','vx\u2082','vy\u2082','\u03C4']
for i,vl in enumerate(VarLab):
  Label(toolbar,text=str(vl)).grid(row=nr,column=0)
  VarEntry.append(Entry(toolbar,bd=5,width=10))
  VarEntry[i].grid(row=nr,column=1)
  VarEntry[i].insert(0,f'{params[i]:.3f}')
  nr+=1
# ...................................................... Period Label
Label(toolbar,text='Period:').grid(row=nr,column=0)
PeriodLab=Label(toolbar,text='     ')
PeriodLab.grid(row=nr,column=1,sticky=W)
nr+=1
# ............................................ Create Colliding Balls
ball1=Ball(m1,r1,x1,y1,vx1,vy1,'red')
ball2=Ball(m2,r2,x2,y2,vx2,vy2,'blue')
# ....................................................... Time Origin
tt0=time.time()
tcount=0
# .................................................... Animation loop
while RunAll:
  StartIter=time.time()
  # ...................................................... Move balls
  if RunMotion:
    ball1.move()
    ball1.bounce()
    ball2.move()
    ball2.bounce()
    ball1.ElastColl(ball2)
  elif GetData:
    for i,ve in enumerate(VarEntry):
      try:
        params[i]=float(ve.get())
      except ValueError:
        pass
      ve.delete(0,'end')
      ve.insert(0,f'{params[i]:.2f}')
    ball1.m,ball1.rad,ball1.vx,ball1.vy,\
      ball2.m,ball2.rad,ball2.vx,ball2.vy,tau=params
    tau=int(tau)
    ball1.x=ball1.rad-ball1.vx
    ball1.y=ball1.rad-ball1.vy
    ball2.x=cw-ball2.rad-ball2.vx
    ball2.y=ball2.rad-ball2.vy
    ball1.move()
    ball2.move()
    GetData=False
  # ................................................ Cycle duration
  tcount+=1
  if tcount>=10:
    tcount=0
    ttt=time.time()
    elapsed=ttt-tt0
    PeriodLab['text']=f'{elapsed*100:8.2f}'+' ms'
    tt0=ttt
  canvas.update()
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-ElapsIter)
  #------------------------------------------------------------------
root.destroy()
  
