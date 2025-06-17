#!/usr/bin/env python3
from tkinter import *
from matplotlib.colors import is_color_like
import numpy as np
import random as rn
import time
# .................................................. Global Variables
RunAll=True
GetData=GetPr=GetQt=RunMotion=False
ButtWidth=11
Grabbed=-1
SelB=-1
nBalls=0
mass=200
rad=20
MaxSpeed=5
tau=20  #  milliseconds
col='blue'
# ......................................... ............ Canvas Sizes
cw=800
ch=600
# ...................................................... Start Values
ball=[]
QtLab=['Mass','Radius','x','y','vx','vy']
QtKey=['m','r','x','y','vx','vy']
QtForm=['{:.3f}','{:d}','{:.3f}','{:.3f}','{:.3f}','{:.3f}']
QtRead=[float,int,float,float,float,float]
PrLab=['\u03C4/ms','Mass','Radius','Max. Speed']
PrList=[tau,mass,rad,MaxSpeed]
PrForm=['{:d}','{:.3f}','{:d}','{:.3f}']
PrRead=[int,float,int,float]
nQt=len(QtKey)
# ........................................................ Class Ball
class Ball:
  def __init__(self,mass,radius,x,y,vx,vy,color):
    self.m=mass
    self.r=radius
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    self.col=color
    self.image=canvas.create_oval(self.x-self.r,ch-(self.y+self.r),\
      self.x+self.r,ch-(self.y-self.r),fill=self.col,outline='black')
  # ....................................................... Move Ball
  def move(self):
    self.x+=self.vx
    self.y+=self.vy
  # ..................................................... Redraw Ball
  def redraw(self):
    canvas.coords(self.image,self.x-self.r,ch-(self.y+self.r),\
      self.x+self.r,ch-(self.y-self.r))
  # ........................................ Bounce on Canvas Borders
  def bounce(self):
    if (self.x+self.r)>=cw:
      self.vx=-abs(self.vx)
      self.x=2.0*(cw-self.r)-self.x
    elif (self.x-self.r)<=0:
      self.vx=abs(self.vx)
      self.x=2.0*self.r-self.x
    if (self.y+self.r)>=ch:
      self.vy=-abs(self.vy)
      self.y=2.0*(ch-self.r)-self.y
    elif (self.y-self.r)<=0:
      self.vy=abs(self.vy)
      self.y=2.0*self.r-self.y
  # ............................................... Elastic Collision
  def ElastColl(self,other):
    dx=other.x-self.x
    dy=other.y-self.y
    distsq=dx**2+dy**2
    R12sq=(self.r+other.r)**2
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
# .................................................. Button Functions
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  if RunMotion:
    butts[0]['text']='Stop'
    for xx in butts[1::]+QtEntry+PrEntry+[ColorEntry,DefColorEntry]:
      xx['state']=DISABLED
  else:
    butts[0]['text']='Restart'
    for xx in butts[1::]+QtEntry+PrEntry+[ColorEntry,DefColorEntry]:
      xx['state']=NORMAL
# ...................................................................
def StopAll():
  global RunAll
  RunAll=False
# ......................................................... Grab Ball
def GrabBall(event):
  global Grabbed
  if not RunMotion:
    Grabbed=-1
    xx,yy=event.x,ch-event.y
    for i,bb in enumerate(ball):
      if((bb.x-xx)**2+(bb.y-yy)**2)<bb.r**2:
        Grabbed=i
        break
# ...................................................... Release Ball
def ReleaseBall(event):
  global Grabbed
  Grabbed=-1
# ......................................................... Drag Ball
def DragBall(event):
  global Grabbed
  if Grabbed>=0:
    r=ball[Grabbed].r
    xx,yy=event.x,ch-event.y
    ball[Grabbed].x=np.clip(xx,r,cw-r)
    ball[Grabbed].y=np.clip(yy,r,ch-r)
# ...................................................... Add New Ball
def AddBall():
  global nBalls,SelB
  overl=True
  while overl:
    x=rn.randint(rad,cw-rad)
    y=rn.randint(rad,ch-rad)
    overl=any(((x-b.x)**2+(y-b.y)**2)<(rad+b.r)**2 for b in ball)
  vx=rn.uniform(-MaxSpeed,MaxSpeed)
  vy=rn.uniform(-MaxSpeed,MaxSpeed)
  ball.append(Ball(mass,rad,x,y,vx,vy,col))
  ColLab.config(bg=col)
  SelB=nBalls
  nBalls+=1
  SelectBall(0)
# ....................................................... Remove Ball
def DelBall(event):
  global nBalls,SelB
  if RunMotion:
    return
  iDel=-1
  xx,yy=event.x,ch-event.y
  for i,bb in enumerate(ball):
    if((bb.x-xx)**2+(bb.y-yy)**2)<bb.r**2:
      iDel=i
      break
  if iDel==-1:
    return
  canvas.delete(ball[iDel].image)
  ball.pop(iDel)
  nBalls-=1
  if nBalls==0:
    SelBallLab.config(text='No Balls',fg='black')
  if SelB>=nBalls:
    SelB-=1
    SelectBall(0)
# ....................................... Read Color of Selected Ball
def ReadColor(*args):
  if SelB>=0:
    color=ColorEntry.get()
    if is_color_like(color):
      ColLab.config(bg=color)
      ball[SelB].col=color
      SelBallLab.config(fg=color)
      canvas.itemconfig(ball[SelB].image,fill=color,outline='black')
# ................................................ Read Default Color
def ReadDefaultColor(*args):
  global col
  NewCol=DefColorEntry.get()
  if is_color_like(NewCol):
    col=NewCol
    DefColLab.config(bg=col)
# ....................................................... Select Ball
def SelectBall(delta):
  global SelB
  if nBalls==0:
    return
  SelB=(SelB+delta)%nBalls
  SelBallLab.config(text='Ball '+str(SelB),fg=ball[SelB].col)
  for i,vv in enumerate(list(ball[SelB].__dict__.values())[:nQt]):
    QtEntry[i].delete(0,'end')
    QtEntry[i].insert(0,QtForm[i].format(vv))
  ColLab.config(bg=ball[SelB].col)
  ColorEntry.delete(0,'end')
  ColorEntry.insert(0,'{:s}'.format(ball[SelB].col))
# ...................................................... Read Entries
def ReadQt(WhichEntry):
  global GetQt,SelEn
  SelEn=WhichEntry
  GetQt=True
# ..................................................................
def ReadPr(WhichPr):
  global GetPr,SelPr
  SelPr=WhichPr
  GetPr=True
# ................................................ Create Root Window
root=Tk()
root.title('Multicollision')
# ...................................................................
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# ........................................... Bind Mouse to Functions
canvas.bind('<Button-1>',GrabBall)
canvas.bind('<B1-Motion>',DragBall)
canvas.bind('<ButtonRelease-1>',ReleaseBall)
canvas.bind('<ButtonRelease-3>',DelBall)
# .................................................... Create Toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
toolbar.option_add('*Font','Helvetica 11')
# .................................................... Create Buttons
nr=0
butts=[]
ButtLab=['Start','Add Ball','Exit']
ButtFun=[StartStop,AddBall,StopAll]
for i,(ll,ff) in enumerate(zip(ButtLab,ButtFun)):
  butts.append(Button(toolbar,text=ll,command=ff,width=ButtWidth))
  butts[i].grid(row=nr,column=0,sticky=W)
  nr+=1
# ............................................... Selected Ball Label
Label(toolbar,text='Selected Ball:').grid(row=nr,column=0)
SelBallLab=Label(toolbar,text='No Balls',width=15,bg='#ffffff')
SelBallLab.grid(row=nr,column=1)
SelBallLab.bind('<Button-1>',lambda event,num=-1:SelectBall(num))
SelBallLab.bind('<Button-5>',lambda event,num=-1:SelectBall(num))
SelBallLab.bind('<Button-3>',lambda event,num=1:SelectBall(num))
SelBallLab.bind('<Button-4>',lambda event,num=1:SelectBall(num))
nr+=1
# ................................... Entries for Physical Quantities
QtEntry=[]
for i,kk in enumerate(QtLab):
  Label(toolbar,text=QtLab[i]).grid(row=nr,column=0)
  QtEntry.append(Entry(toolbar,bd=3,width=16))
  QtEntry[i].grid(row=nr,column=1)
  QtEntry[i].insert(0,'        ')
  QtEntry[i].bind('<Return>',lambda event,num=i:ReadQt(num))
  nr+=1
# ....................................................... Color Entry
ColLab=Label(toolbar,text='    ',bd=5,width=9,bg=col)
ColLab.grid(row=nr,column=0)
ColorEntry=Entry(toolbar,bd=3,width=16)
ColorEntry.grid(row=nr,column=1)
ColorEntry.insert(0,'{:s}'.format(col))
ColorEntry.bind('<Return>',ReadColor)
nr+=1
# ............................................ Entries for Parameters
Label(toolbar,text='Default Parameters').grid(row=nr,column=0,\
  columnspan=2,pady=10)
nr+=1
PrEntry=[]
for i,pl in enumerate(PrLab):
  Label(toolbar,text=pl).grid(row=nr,column=0)
  PrEntry.append(Entry(toolbar,bd=3,width=12))
  PrEntry[i].grid(row=nr,column=1)
  PrEntry[i].insert(0,PrForm[i].format(PrList[i]))
  PrEntry[i].bind('<Return>',lambda event,num=i:ReadPr(num))
  nr+=1
# ............................................... Default Color Entry
DefColLab=Label(toolbar,text='    ',bd=5,width=9,bg=col)
DefColLab.grid(row=nr,column=0)
DefColorEntry=Entry(toolbar,bd=3,width=12)
DefColorEntry.grid(row=nr,column=1)
DefColorEntry.insert(0,'{:s}'.format(col))
DefColorEntry.bind('<Return>',ReadDefaultColor)
nr+=1
# ....................................................... Cycle Label
csLabs=['Period:','Frames/s']
CYCLE,SPEED=range(2)
csDisp=[]
for i,ll in enumerate(csLabs):
  Label(toolbar,text=ll).grid(row=nr,column=0)
  csDisp.append(Label(toolbar,text='         '))
  csDisp[i].grid(row=nr,column=1,sticky=W)
  nr+=1
# ....................................................... Time Origin
tt0=time.time()
tcount=0
# .................................................... Animation Loop
while RunAll:
  StartIter=time.time()
  # ............................... Redraw Balls in Current Positions
  for bb in ball:
    bb.redraw()
  canvas.update()
  # ...................................................... Move Balls
  if RunMotion:
    for i,b1 in enumerate(ball):
      b1.move()
      b1.bounce()
      for b2 in ball[:i]:
        b2.ElastColl(b1)
  elif GetPr: # ..................................... Read Parameters
    try:
      PrList[SelPr]=PrRead[SelPr](PrEntry[SelPr].get())
    except ValueError:
      pass
    else:
      PrEntry[SelPr].delete(0,'end')
      PrEntry[SelPr].insert(0,PrForm[SelPr].format(PrList[SelPr]))
      tau,mass,rad,MaxSpeed=PrList
    GetPr=False
  elif GetQt and SelB>=0: # ..................... Read Ball Variables
    try:
      ball[SelB].__dict__[str(QtKey[SelEn])]=vv=\
        QtRead[SelEn](QtEntry[SelEn].get())
    except ValueError:
      pass
    else:
      QtEntry[SelEn].delete(0,'end')
      QtEntry[SelEn].insert(0,QtForm[SelEn].format(vv))
    GetQt=False    
  # ................................................ Cycle Duration
  tcount+=1
  if tcount>=10:
    tcount=0
    ttt=time.time()
    elapsed=ttt-tt0
    csDisp[CYCLE]['text']='{:8.2f}'.format(elapsed*100.0)+' ms'
    csDisp[SPEED]['text']='{:8.2f}'.format(10.0/elapsed)+' fps'
    tt0=ttt
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-ElapsIter)
  #------------------------------------------------------------------
root.destroy()
  
