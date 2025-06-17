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
RunIter=False
NewBaryc=False
GetData=False
ReWrite=False
# ..................................................... Class CelBody
class CelBody:
  def __init__(self,mass,radius,x,y,vx,vy,color):
    self.m=mass
    self.rad=radius
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    self.col=color
    self.wakex=[]
    self.wakey=[]
    self.WakeCount=0
  # ..................................................... move body
  def move(self):
    self.x+=self.vx
    self.y+=self.vy
  # ............................................ draw body and wake
  def draw(self,canvas,orig,nWake):
    canvas.create_oval(orig[0]+int(self.x-self.rad),\
      int(orig[1]-self.y+self.rad),int(orig[0]+self.x+self.rad),\
        int(orig[1]-self.y-self.rad),fill=self.col)
    k=1
    while k<len(self.wakex):
      canvas.create_line(orig[0]+self.wakex[k-1],\
        orig[1]-self.wakey[k-1],orig[0]+self.wakex[k],\
          orig[1]-self.wakey[k],fill=self.col)
      k+=1
    if self.WakeCount%2==0:
      self.wakex.append(self.x)
      self.wakey.append(self.y)
    self.WakeCount+=1
    while len(self.wakex)>nWake:
      pip=self.wakex.pop(0)
      pip=self.wakey.pop(0)
# .................................................... create bodies
bd=[]
bd.append(CelBody(200.0,10.0,0.0,0.0,0.0,0.0,'red'))
bd.append(CelBody(10.0,6.0,300.0,0.0,0.0,40.0,'blue'))
bd.append(CelBody(5.0,4.0,0.0,200.0,50.0,0.0,'green'))
nB=len(bd)
# ............................................................ masses
masses=[]
i=0
while i<nB:
  masses.append(bd[i].m)
  i+=1
# ............................................ finite time difference
dt=0.1
# ............................................ gravitational constant
KG=5000.0
# ................................................. cycle duration/ms
cycle=20
# ....................................................... tail length
nWake=200
# ................................................. barycenter radius
bcrad=2
# ........................................................ value list
values=[KG,dt,cycle,nWake]
t=[0.0,dt]
# ................................................... parameter array
params=[values,masses]
# ........................................... evaluate center of mass
def baryc(bd):
  nB=len(bd)
  cx=cy=cvx=cvy=mtot=0
  i=0
  while i<nB:
    cx+=bd[i].m*bd[i].x
    cy+=bd[i].m*bd[i].y
    cvx+=bd[i].m*bd[i].vx
    cvy+=bd[i].m*bd[i].vy
    mtot+=bd[i].m
    i+=1
  cx/=mtot
  cy/=mtot
  cvx/=mtot
  cvy/=mtot
  return [[cx,cy],[cvx,cvy]]
# ..................................... move origin to center of mass
def SetBaryc():
  global NewBaryc
  global bd
  nB=len(bd)
  xcm,ycm=baryc(bd)[0]
  cvx,cvy=baryc(bd)[1]
  i=0
  while i<nB:
    bd[i].x-=xcm
    bd[i].y-=ycm
    bd[i].vx-=cvx
    bd[i].vy-=cvy
    i+=1
  NewBaryc=True
# ......................................................... bodies2vect
#   x1,y1,x2,y2, ...,vx1,vy1,vx2,vy2, ...=vect
def bodies2vect(bodies,vect,nB):
  del vect[:]
  twonB=2*nB
  fournB=4*nB
  i=0
  while i<fournB:
    vect.append(0)
    i+=1
  i=0
  while i<nB:
    vect[2*i]=bodies[i].x
    vect[2*i+1]=bodies[i].y
    vect[twonB+2*i]=bodies[i].vx
    vect[twonB+2*i+1]=bodies[i].vy
    i+=1
# ......................................................... vect2bodies
def vect2bodies(vect,bodies,nB):
  twonB=2*nB
  i=0
  while i<nB:
    bodies[i].x=vect[2*i]
    bodies[i].y=vect[2*i+1]
    bodies[i].vx=vect[twonB+2*i]
    bodies[i].vy=vect[twonB+2*i+1]
    i+=1
# ............................................... create input vector
def WriteInput(bodies,val,InpV):
  nB=len(bodies)
  nV=len(values)
  del InpV[:]
  i=0
  while i<nB:
    InpV.append(bodies[i].m)
    InpV.append(bodies[i].x)
    InpV.append(bodies[i].y)
    InpV.append(bodies[i].vx)
    InpV.append(bodies[i].vy)
    i+=1
  i=0
  while i<nV:
    InpV.append(val[i])
    i+=1
# ....................................................................
def ReadInput(InpV,bodies,masses,val,vect):
  nB=len(bodies)
  nV=len(val)
  twonB=2*nB
  i=0
  while i<nB:
    bodies[i].m=masses[i]=InpV[5*i]
    bodies[i].x=vect[2*i]=InpV[5*i+1]
    bodies[i].y=vect[2*i+1]=InpV[5*i+2]
    bodies[i].vx=vect[twonB+2*i]=InpV[5*i+3]
    bodies[i].vy=vect[twonB+2*i+1]=InpV[5*i+4]
    i+=1
  j=0
  i=5*nB
  while j<nV:
    val[j]=InpV[i]
    i+=1
    j+=1
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
# ....................................................... root window
root=Tk()
root.title("Gravity 3")
root.bind('<Return>',ReadData)
# ............................................................ canvas
cw=800
ch=800
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ........................................................... toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1, sticky=N)
# ............................................................ buttons
nr=0
StartButton=Button(toolbar,text="Start",command=StartStop,width=11)
StartButton.grid(row=nr,column=0,sticky=W)
nr+=1
AdjustButton=Button(toolbar, text="Set Barycenter",\
  command=SetBaryc,width=11)
AdjustButton.grid(row=nr,column=0,columnspan=2,sticky=W)
nr+=1
ReadButton=Button(toolbar, text="Read Data", command=ReadData,width=11)
ReadButton.grid(row=nr,column=0,columnspan=2,sticky=W)
nr+=1
CloseButton=Button(toolbar, text="Exit", command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,sticky=W)
nr+=1
# ............................................................ Origin
Ox=cw/2
Oy=ch/2
orig=[Ox,Oy]
# ...................................................... input vector
InpV=[]
WriteInput(bd,values,InpV)
nInp=len(InpV)
# ..................................................... odeint vector
y=[]
bodies2vect(bd,y,nB)
# ........................................................ Input list
InputList=[]
i=0
while i<nB:
  InputList.append('m'+sub[i])
  InputList.append('x'+sub[i])
  InputList.append('y'+sub[i])
  InputList.append('vx'+sub[i])
  InputList.append('vy'+sub[i])
  i+=1
InputList.append('G')
InputList.append('dt')
InputList.append('Cycle/ms')
InputList.append('Tail')
# ................................................ Labels and Entries
LabInput=[]
EntryInput=[]
i=0
while i<nInp:
  LabInput.append(Label(toolbar,text=InputList[i],\
    font=("Helvetica",12)))
  LabInput[i].grid(row=nr,column=0)
  EntryInput.append(Entry(toolbar,bd=5,width=8))
  EntryInput[i].grid(row=nr,column=1)
  EntryInput[i].insert(0,"{:.2f}".format(InpV[i]))
  i+=1
  nr+=1
# ........................................................ time label
CycleLab0=Label(toolbar,text="Period:",font=("Helvetica",11))
CycleLab0.grid(row=nr,column=0)
CycleLab=Label(toolbar,text="     ",font=("Helvetica",11))
CycleLab.grid(row=nr,column=1,sticky=W)
nr+=1
# .................................................................... function
def fun(yInp,t,params):
  KG,dt,cycle,nWake=params[0]             # unpack parameters
  mm=params[1]                            # unpack masses
  nB=len(mm)
  twoN=2*nB
  fourN=4*nB
  ax=[0]*nB
  ay=[0]*nB
  i=1
  while i<nB:
    j=0
    while j<i:
      deltax=yInp[2*i]-yInp[2*j]
      deltay=yInp[2*i+1]-yInp[2*j+1]
      r2=deltax**2+deltay**2
      alpha=arctan2(deltay,deltax)
      ff=KG/r2
      fx=ff*cos(alpha)
      fy=ff*sin(alpha)
      ax[i]-=fx*mm[j]
      ax[j]+=fx*mm[i]
      ay[i]-=fy*mm[j]
      ay[j]+=fy*mm[i]
      j+=1
    i+=1
  derivs=[]
  # ............................................... insert velocities
  i=twoN
  while i<fourN:
    derivs.append(yInp[i])
    i+=1
  # ............................................ insert accelerations
  i=0
  while i<nB:
    derivs.append(ax[i])
    derivs.append(ay[i])
    i+=1
  return derivs
# ........................................... numerical time interval
t=[0.0,0.1]
tt0=time.time()
tcount=0
while RunAll:
  StartIter=time.time()
  # ............................................. Draw Cartesian axes
  canvas.delete(ALL)
  canvas.create_line(0,Oy,cw,Oy,fill="black")
  canvas.create_line(Ox,0,Ox,ch,fill="black")
  canvas.create_oval(Ox-bcrad,Oy-bcrad,Ox+bcrad,Oy+bcrad,fill="black")
  # ..................................................... draw bodies
  i=0
  while i<nB:
    bd[i].draw(canvas,orig,nWake)
    i+=1
  # .................................................. center of mass
  cx,cy=baryc(bd)[0]
  canvas.create_oval(Ox+cx-bcrad,Oy-cy-bcrad,Ox+cx+bcrad,Oy-cy+bcrad,\
    fill="black")
  # .......................................................... motion
  if RunIter:
    # ..................................................... next step
    psoln = odeint(fun,y,t,args=(params,))
    y=psoln[1,:]
    vect2bodies(y,bd,nB)
  # .................................................................
  else:
    if NewBaryc:
      ReWrite=True
      WriteInput(bd,values,InpV)
      NewBaryc=False
    elif GetData:
      i=0
      while i<nInp:
        try:
          InpV[i]=float(EntryInput[i].get())
        except ValueError:
          pass
        i+=1
      ReWrite=True
      GetData=False
    if ReWrite:
      ReadInput(InpV,bd,masses,values,y)
      i=0
      while i<nInp:
        EntryInput[i].delete(0,'end')
        EntryInput[i].insert(0,"{:.2f}".format(InpV[i]))
        i+=1
      t=[0.0,values[1]]
      cycle=int(values[2])
      nWake=int(values[3])
      ReWrite=False
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
#----------------------------------------------------------------------
root.destroy()
root.mainloop()
  