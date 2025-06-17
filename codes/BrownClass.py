#!/usr/bin/env python3
from numpy import *
from random import *
from tkinter import *
import time
#
Vmax=8.0
cycle=20  #  milliseconds
mesoM=200
microM=10
mesoR=12
microR=5
# .............................................................. class particle
class particle:
  def __init__(self,mass,radius,x,y,vx,vy,color):
    self.m=mass
    self.rad=radius
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    self.color=color
    # ................................................. move particle
  def move(self):
    self.x+=self.vx
    self.y+=self.vy
    # ...................................... bounce on canvas borders
  def bounce(self,canvas):
    width=canvas.winfo_width()
    height=canvas.winfo_height()
    if (self.x+self.rad)>=width:
      self.vx=-abs(self.vx)
      self.x=width-self.rad
    if (self.x-self.rad)<=0:
      self.vx=abs(self.vx)
      self.x=self.rad
    if (self.y+self.rad)>=height:
      self.vy=-abs(self.vy)
      self.y=height-self.rad
    if (self.y-self.rad)<=0:
      self.vy=abs(self.vy)
      self.y=self.rad
      # ........................................... elastic collision
  def ElastColl(self,other):
    deltax=other.x-self.x
    deltay=other.y-self.y
    impactsq=(self.rad+other.rad)**2
    impact=sqrt(impactsq)
    if (deltax**2+deltay**2)<=impactsq:
      alpha=arctan2(deltay,deltax)
      csalpha=cos(alpha)
      snalpha=sin(alpha)
      SelfXi=self.vx*csalpha+self.vy*snalpha
      SelfEta=-self.vx*snalpha+self.vy*csalpha
      OtherXi=other.vx*csalpha+other.vy*snalpha
      OtherEta=-other.vx*snalpha+other.vy*csalpha
      SelfNewXi=((self.m-other.m)*SelfXi+2.0*other.m*OtherXi)/\
        (self.m+other.m)
      OtherNewXi=((other.m-self.m)*OtherXi+2.0*self.m*SelfXi)/\
        (self.m+other.m)
      self.vx=SelfNewXi*csalpha-SelfEta*snalpha
      self.vy=SelfNewXi*snalpha+SelfEta*csalpha
      other.vx=OtherNewXi*csalpha-OtherEta*snalpha
      other.vy=OtherNewXi*snalpha+OtherEta*csalpha
      # ............................................... avoid overlap
      self.x=other.x-impact*csalpha
      self.y=other.y-impact*snalpha
      # ...................................... particles overlapping?
  def overlap(self,other):
    overl=((self.x-other.x)**2+(self.y-other.y)**2)<=\
      (self.rad+other.rad)**2
    return overl
    # ................................................. draw particle
  def draw(self,canvas):
    canvas.create_oval(int(self.x-self.rad),\
      int(canvas.winfo_height()-self.y+self.rad),\
        int(self.x+self.rad),\
          int(canvas.winfo_height()-self.y-self.rad),fill=self.color)
# .................................................................. Functions
def RandomVel(partic,Vmax):
  nMicro=len(partic)
  for i in range(nMicro):
    partic[i].vx=uniform(-Vmax,Vmax)
    partic[i].vy=uniform(-Vmax,Vmax)
# .............................................................................
global GetData,RunAll,RunIter
RunAll=True
GetData=RunIter=False
# .............................................................................
ButtWidth=9
# ............................................................ button functions
def ReadData(*arg):
  global GetData
  GetData=True
#
def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StartButton["text"]="Stop"
  else:
    StartButton["text"]="Restart"
#
def StopAll():
  global RunAll
  RunAll=False
# .............................................................................
root=Tk()
root.title("Brown 1")
root.bind('<Return>',ReadData)
# .............................................................................
cw=600
ch=600
# .............................................................................
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ..................................................................... toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1, sticky=N)
# ..................................................................... buttons
nr=0
StartButton=Button(toolbar,text="Start",command=StartStop,width=ButtWidth)
StartButton.grid(row=nr,column=0,sticky=W)
nr+=1
ReadButton=Button(toolbar, text="Read Data", command=ReadData,width=ButtWidth)
ReadButton.grid(row=nr,column=0,columnspan=2,sticky=W)
nr+=1
CloseButton=Button(toolbar, text="Exit", command=StopAll,width=ButtWidth)
CloseButton.grid(row=nr,column=0,sticky=W)
nr+=1
# ...................................................................... arrays
LabPar=[]
EntryPar=[]
ParList=["Max. Vel.","Cycle/ms"]
nPar=len(ParList)
# ..................................................................... Entries
for i in range (nPar):
  LabPar.append(Label(toolbar,text=str(ParList[i]),font=("Helvetica",12)))
  LabPar[i].grid(row=nr,column=0)
  EntryPar.append(Entry(toolbar,bd=5,width=10))
  EntryPar[i].grid(row=nr,column=1)
  nr+=1
# ........................................................ time label
CycleLab0=Label(toolbar,text="Period:",font=("Helvetica",11))
CycleLab0.grid(row=nr,column=0)
CycleLab=Label(toolbar,text="     ",font=("Helvetica",11))
CycleLab.grid(row=nr,column=1,sticky=W)
nr+=1
# .................................................................. parameters
params=[Vmax,cycle]
for i in range(nPar):
  buff="%.2f" % params[i]
  EntryPar[i].delete(0,'end')
  EntryPar[i].insert(0,buff)
# ......................................................... mesoscopic particle
meso=particle(mesoM,mesoR,cw/2.0,ch/2.0,0.0,0.0,"red")
# ................................ random non-overlapping microscopic particles
nmicro=150
micro=[]
j=0
while j<nmicro:
  newp=particle(microM,microR,uniform(microR,cw-2*microR),\
    uniform(microR,ch-2*microR),uniform(-Vmax,Vmax),\
      uniform(-Vmax,Vmax),"blue")
  if meso.overlap(newp):
    continue
  overl=False
  k=0
  while k<j:
    if newp.overlap(micro[k]):
      overl=True
      break
    k+=1
  if not overl:
    micro.append(newp)
    j+=1
# ............................................................... time interval
tt0=time.time()
tcount=0
# .............................................................. animation loop
while RunAll:
  StartIter=time.time()
  canvas.delete(ALL)
  # .................................................. draw mesoscopic particle
  meso.draw(canvas)
  # ................................................. draw microscopic particles
  j=0
  while j<nmicro:
    micro[j].draw(canvas)
    j+=1
  # ............................................................ move particles
  if RunIter:
    meso.move()
    meso.bounce(canvas)
    # ......................................... microscopic particle positions
    j=0
    while j<nmicro:
      micro[j].move()
      micro[j].bounce(canvas)
      # ................................................ meso-micro collision?
      meso.ElastColl(micro[j])
      # ............................................... micro-micro collision?
      k=0
      while k<j:
        micro[j].ElastColl(micro[k])
        k+=1
      j+=1
  else:
    if GetData:
      OldVel=Vmax
      i=0
      while i<nPar:
        try:
          params[i]=float(EntryPar[i].get())
        except ValueError:
          pass
        i+=1
      Vmax,cycle=params
      cycle=int(cycle)
      for i in range(nPar):
        buff="%.2f" % params[i]
        EntryPar[i].delete(0,'end')
        EntryPar[i].insert(0,buff)
      if OldVel !=  Vmax:
        RandomVel(micro,Vmax)
      GetData=False
  # ................................................ cycle duration
  tcount+=1
  if tcount==10:
    tcount=0
    ttt=time.time()
    elapsed=ttt-tt0
    CycleLab['text']="%8.2f"%(elapsed*100.0)+" ms"
    tt0=ttt
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.update()
  canvas.after(cycle-ElapsIter)
  #----------------------------------------------------------------------------
root.destroy()
root.mainloop()
  