#!/usr/bin/env python3
import os
from numpy import *
from tkinter import *
from random import *
from scipy.integrate import odeint
import time

# ............................................. subscripts for labels
sub=['\u2080','\u2081','\u2082','\u2083','\u2084','\u2085',\
  '\u2086','\u2087','\u2088','\u2089']
# .................................................. Global variables
RunAll=True
RunIter=NewBaryc=GetData=ReWrite=False
scale=3.0e12
cw=900
ch=900
bcrad=2
cycle=20
PathLength=200
dt=2.0e-19
q=1.602176e-19        # elementary charge/Coulomb
me=9.10938e-31        # electron mass/kg
mp=1.67262e-27        # proton mass/kg
eps0=8.854187817e-12  # vacuum permittivity (F/m)
ke=8.987551e9         # Coulomb's constant (N m^2/C^2)
r2=1.0e-10            # radius of second-electron orbit / m
r1=r2/3.0
v1=sqrt(ke*2.0*q**2/(me*r1))
v2=sqrt(ke*q**2/(me*r2))
# ..................................................... canvas origin
Ox=cw/2.0
Oy=ch/2.0
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
# ................................................ Read Data function
def ReadData(*arg):
  global GetData
  GetData=True
# .......................................................... Scale Up
def ScaleUp(*arg):
  global scale
  scale*=sqrt(2.0)
  ScaleLab['text']="%10.3e"%(scale)
# ........................................................ Scale Down
def ScaleDown(*arg):
  global scale
  scale/=sqrt(2.0)
  ScaleLab['text']="%10.3e"%(scale)
# .......................... Evaluate center of mass and its velocity
def baryc(part):
  mtot=sum(zz.m for zz in part)
  cx=sum(zz.x*zz.m for zz in part)/mtot
  cy=sum(zz.y*zz.m for zz in part)/mtot
  cvx=sum(zz.vx*zz.m for zz in part)/mtot
  cvy=sum(zz.vy*zz.m for zz in part)/mtot
  return [[cx,cy],[cvx,cvy]]
# ..................................... move origin to center of mass
def SetBaryc():
  global NewBaryc
  global part
  xcm,ycm=baryc(part)[0]
  cvx,cvy=baryc(part)[1]
  for zz in part:
    zz.x-=xcm
    zz.y-=ycm
    zz.vx-=cvx
    zz.vy-=cvy
  NewBaryc=True
# ..................................................... Class particle
class particle:
  def __init__(self,mass,charge,frict,x,y,vx,vy):
    self.m=mass
    self.q=charge
    self.fr=frict
    self.x=x
    self.y=y
    self.pathmin=sqrt(self.x**2+self.y**2)*0.05
    self.vx=vx
    self.vy=vy
    if self.q>0:            # nucleus
      self.col='red'
      self.rad=8
    else:                   # electron
      self.col='blue'
      self.rad=4
    self.image=canvas.create_oval(Ox+int(scale*self.x-self.rad),\
      int(Oy-scale*self.y+self.rad),int(Ox+scale*self.x+self.rad),\
        int(Oy-scale*self.y-self.rad),fill=self.col,outline=self.col)
    self.path=[self.x,self.y]*PathLength
    self.ScaledPath=[0.0,0.0]*PathLength
    self.PathImg=canvas.create_line(self.ScaledPath,fill=self.col)
  # ................................................... move perticle
  def move(self):
    canvas.coords(self.image,Ox+scale*self.x-self.rad,\
      Oy-scale*self.y+self.rad,Ox+scale*self.x+self.rad,\
        Oy-scale*self.y-self.rad)
  def UpdatePath(self):
    if abs(self.x-self.path[-2])+abs(self.y-self.path[-1])>self.pathmin:
      del self.path[:2]
      self.path.append(self.x)
      self.path.append(self.y)
  def DrawPath(self):
    self.ScaledPath[::2]=[Ox+scale*zz for zz in self.path[::2]]
    self.ScaledPath[1::2]=[Oy-scale*zz for zz in self.path[1::2]]
    canvas.coords(self.PathImg,self.ScaledPath)
# ....................................................... root window
root=Tk()
root.title('Classical Helium Atom')
root.bind('<Return>',ReadData)
root.bind('<Control-plus>',ScaleUp)
root.bind('<Control-minus>',ScaleDown)
# ............................................................ canvas
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ........................................................... toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1, sticky=N)
# ............................................................ buttons
nr=0
StartButton=Button(toolbar,text="Start",command=StartStop,width=11)
StartButton.grid(row=nr,column=0,sticky=W)
AdjustButton=Button(toolbar, text="Set Barycenter",\
  command=SetBaryc,width=11)
AdjustButton.grid(row=nr,column=1,sticky=W)
nr+=1
CloseButton=Button(toolbar, text="Exit", command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,columnspan=2,sticky=W)
nr+=1
# ..................................................... Create bodies
part=[]
part.append(particle(4.0*mp,2.0*q,0.0,0.0,0.0,0.0,0.0))
part.append(particle(me,-q,0.0,-r1,0.0,0.0,-v1))
part.append(particle(me,-q,0.0,r2,0.0,0.0,v2))
nP=len(part)
# .............................................. Parameter-value list
values=[ke,dt,cycle,PathLength]
# ....................................................... vect2bodies
def vect2bodies(vect,bodies):
  for i,zz in enumerate(bodies):
    zz.x=vect[4*i]
    zz.y=vect[4*i+1]
    zz.vx=vect[4*i+2]
    zz.vy=vect[4*i+3]
# ............................................... create input vector
def WriteInput(bodies,val,InpV,vect):
  nn=7*len(bodies)
  InpV[:nn:7]=[zz.m for zz in bodies]
  InpV[1:nn:7]=[zz.q for zz in bodies]
  InpV[2:nn:7]=[zz.fr for zz in bodies]
  InpV[3:nn:7]=vect[::4]=[zz.x for zz in bodies]
  InpV[4:nn:7]=vect[1::4]=[zz.y for zz in bodies]
  InpV[5:nn:7]=vect[2::4]=[zz.vx for zz in bodies]
  InpV[6:nn:7]=vect[3::4]=[zz.vy for zz in bodies]
  InpV[nn::]=val
# ................................................. Read Entry values
def ReadInput(InpV,bodies,val,vect):
  nn=7*len(bodies)
  for i,zz in enumerate(bodies):
    zz.m=InpV[i*7]
    zz.q=InpV[i*7+1]
    zz.fr=InpV[i*7+2]
    zz.x=vect[i*4]=InpV[i*7+3]
    zz.y=vect[i*4+1]=InpV[i*7+4]
    zz.vx=vect[i*4+2]=InpV[i*7+5]
    zz.vy=vect[i*4+3]=InpV[i*7+6]
  val[::]=InpV[nn::]
# ...................................................... input vector
InpV=[0]*(7*nP+len(values))
y=[0]*4*nP
WriteInput(part,values,InpV,y)
# ........................................................ Input list
InputList=[]
for i in range(len(part)):
  InputList.append('m'+sub[i])
  InputList.append('q'+sub[i])
  InputList.append('\u03B7'+sub[i])  #     eta
  InputList.append('x'+sub[i])
  InputList.append('y'+sub[i])
  InputList.append('vx'+sub[i])
  InputList.append('vy'+sub[i])
InputList.append('Ke')
InputList.append('dt')
InputList.append('Cycle/ms')
InputList.append('Tail')
# .................................. Labels and Entries for particles
LabInput=[]
EntrOdeInput=[]
for i,zz in enumerate(InputList):
  LabInput.append(Label(toolbar,text=zz,font=("Helvetica",11)))
  LabInput[i].grid(row=nr,column=0)
  EntrOdeInput.append(Entry(toolbar,bd=3,width=12))
  EntrOdeInput[i].grid(row=nr,column=1)
  EntrOdeInput[i].insert(0,"{:.3e}".format(InpV[i]))
  nr+=1
# ........................................................ time label
CycleLab0=Label(toolbar,text="Period:",font=("Helvetica",11))
CycleLab0.grid(row=nr,column=0)
CycleLab=Label(toolbar,text="     ",font=("Helvetica",11))
CycleLab.grid(row=nr,column=1,sticky=W)
nr+=1
# ....................................................... scale label
ScaleLab0=Label(toolbar,text="Scale:",font=("Helvetica",11))
ScaleLab0.grid(row=nr,column=0)
ScaleLab=Label(toolbar,text="%10.3e"%(scale),font=("Helvetica",11))
ScaleLab.grid(row=nr,column=1,sticky=W)
nr+=1
# .......................................................... function
def dfdt(OdeInp,t,pp):
  nn=7*(len(OdeInp)//4)
  mm=pp[:nn:7]                           # masses from InpV
  qq=pp[1:nn:7]                          # charges from InpV
  fr=pp[2:nn:7]                          # drags from InpV
  # ..................................................................
  x=OdeInp[::4]
  y=OdeInp[1::4]
  vx=OdeInp[2::4]
  vy=OdeInp[3::4]
  Fx=list(-array(vx)*array(fr))   # drag contribution to force x
  Fy=list(-array(vy)*array(fr))   # drag contribution to force y
  # ............................ Coulomb contribution to force
  i=1
  while i<nP:
    j=0
    while j<i:
      deltax=x[i]-x[j]
      deltay=y[i]-y[j]
      r2=deltax**2+deltay**2
      alpha=arctan2(deltay,deltax)
      ff=-ke*qq[i]*qq[j]/r2
      fx=ff*cos(alpha)
      fy=ff*sin(alpha)
      Fx[i]-=fx
      Fx[j]+=fx
      Fy[i]-=fy
      Fy[j]+=fy
      j+=1
    i+=1
  # ...................................................................
  derivs=[0]*len(OdeInp)
  derivs[::4]=vx
  derivs[1::4]=vy
  derivs[2::4]=list(array(Fx)/array(mm))
  derivs[3::4]=list(array(Fy)/array(mm))
  # .................................................................
  return derivs
# ........................................... numerical time interval
t=[0.0,dt]
tt0=time.time()
tcount=0
# .............................................. draw coordinate axes
canvas.create_line(0,Oy,cw,Oy,fill="black")
canvas.create_line(Ox,0,Ox,ch,fill="black")
canvas.create_oval(Ox-bcrad,Oy-bcrad,Ox+bcrad,Oy+bcrad,fill="black")
# ................................. Create barycenter image on canvas
bc=canvas.create_oval(Ox-bcrad,Oy-bcrad,Ox+bcrad,Oy+bcrad,fill="black")
# ...................................................................
while RunAll:
  StartIter=time.time()
  # ..................................................... draw bodies
  for zz in part:
    zz.move()
    zz.UpdatePath()
    zz.DrawPath()
  # .................................................. center of mass
  cx,cy=baryc(part)[0]
  cx*=scale
  cy*=scale
  canvas.coords(bc,Ox+cx-bcrad,Oy-cy-bcrad,Ox+cx+bcrad,Oy-cy+bcrad)
  canvas.update()
  # .......................................................... motion
  if RunIter:
    # ..................................................... next step
    psoln = odeint(dfdt,y,t,args=(InpV,))
    y=psoln[1,:]
    vect2bodies(y,part)
  # .................................................................
  else:
    if NewBaryc:
      ReWrite=True
      WriteInput(part,values,InpV,y)
      NewBaryc=False
    elif GetData:
      for i,zz in enumerate(EntrOdeInput):
        try:
          InpV[i]=float(zz.get())
        except ValueError:
          pass
      ReWrite=True
      GetData=False
    if ReWrite:
      ReadInput(InpV,part,values,y)
      for zz,yy in zip(EntrOdeInput,InpV):
        zz.delete(0,'end')
        zz.insert(0,"{:.3e}".format(yy))
      dt=values[1]
      t=[0.0,dt]
      cycle=int(values[2])
      PathLength=int(values[3])
      for zz in part:
        zz.path=[zz.x,zz.y]*PathLength
        zz.ScaledPath=[0.0,0.0]*PathLength
      ReWrite=False
  # ................................................ cycle duration
  tcount+=1
  if tcount==10:
    tcount=0
    ttt=time.time()
    elapsed=ttt-tt0
    CycleLab['text']="%8.3f"%(elapsed*100.0)+" ms"
    tt0=ttt
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.update()
  canvas.after(cycle-ElapsIter)
#----------------------------------------------------------------------
root.destroy()
root.mainloop()
  
