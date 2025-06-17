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
scale=1.0
# ..................................................... Class particle
class particle:
  def __init__(self,mass,charge,frict,x,y,vx,vy):
    self.m=mass
    self.q=charge
    self.fr=frict
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    if self.q>0:
      self.col='red'
    else:
      self.col='blue'
    self.wakex=[self.x]
    self.wakey=[self.y]
    self.collide=0
    self.rad=6
  # ..................................................... move body
  def move(self):
    self.x+=self.vx
    self.y+=self.vy
  # ......................................................... blast
  def blast(self,canvas,orig):
    global scale
    if self.collide<=0:
      return
    xx=scale*self.x
    yy=scale*self.y
    canvas.create_oval(orig[0]+int(xx-100),int(orig[1]-yy+100),\
      int(orig[0]+xx+100),int(orig[1]-yy-100),\
        outline='yellow',fill='yellow')
    self.collide-=1
  # ............................................ draw body and wake
  def draw(self,canvas,orig,nWake):
    global scale
    xx=scale*self.x
    yy=scale*self.y
    rr=scale*self.rad
    if rr<4.0:
      rr=4.0
    canvas.create_oval(orig[0]+int(xx-rr),\
      int(orig[1]-yy+rr),int(orig[0]+xx+rr),\
        int(orig[1]-yy-rr),outline=self.col,fill=self.col)
    k=1
    while k<len(self.wakex):
      canvas.create_line(orig[0]+scale*self.wakex[k-1],\
        orig[1]-scale*self.wakey[k-1],orig[0]+scale*self.wakex[k],\
          orig[1]-scale*self.wakey[k],fill=self.col)
      k+=1
    if abs(self.wakex[-1]-self.x)>4 or abs(self.wakey[-1]-self.y)>4:
      self.wakex.append(self.x)
      self.wakey.append(self.y)
    while len(self.wakex)>nWake:
      pip=self.wakex.pop(0)
      pip=self.wakey.pop(0)
# .................................................... create bodies
part=[]
part.append(particle(2000.0,150.0,0.0,0.0,0.0,0.0,0.0))
part.append(particle(10.0,-50.0,0.0,40.0,0.0,0.0,160.0))
part.append(particle(10.0,-50.0,0.0,150.0,0.0,0.0,-75.0))
part.append(particle(10.0,-50.0,0.0,300.0,0.0,0.0,70.0))
nP=len(part)
# ..................................... masses, charges and frictions
masses=[]
charges=[]
frictions=[]
i=0
while i<nP:
  masses.append(part[i].m)
  charges.append(part[i].q)
  frictions.append(part[i].fr)
  i+=1
# ............................................ finite time difference
dt=0.03
# ............................................ gravitational constant
KK=2000.0
# ................................................. cycle duration/ms
cycle=20
# ....................................................... tail length
nWake=200
# ................................................. barycenter radius
bcrad=2
# ........................................................ value list
values=[KK,dt,cycle,nWake]
t=[0.0,dt]
# ................................................... parameter array
params=[values,masses,charges,frictions]
# ........................................... evaluate center of mass
def baryc(part):
  nP=len(part)
  cx=cy=cvx=cvy=mtot=0
  i=0
  while i<nP:
    cx+=part[i].m*part[i].x
    cy+=part[i].m*part[i].y
    cvx+=part[i].m*part[i].vx
    cvy+=part[i].m*part[i].vy
    mtot+=part[i].m
    i+=1
  cx/=mtot
  cy/=mtot
  cvx/=mtot
  cvy/=mtot
  return [[cx,cy],[cvx,cvy]]
# ..................................... move origin to center of mass
def SetBaryc():
  global NewBaryc
  global part
  global nWake
  nP=len(part)
  xcm,ycm=baryc(part)[0]
  cvx,cvy=baryc(part)[1]
  i=0
  while i<nP:
    part[i].x-=xcm
    part[i].y-=ycm
    part[i].vx-=cvx
    part[i].vy-=cvy
    i+=1
  NewBaryc=True
# ......................................................... bodies2vect
#   x1,y1,x2,y2, ...,vx1,vy1,vx2,vy2, ...=vect
def bodies2vect(bodies,vect,nP):
  twonP=nP*2
  i=0
  while i<nP:
    vect[2*i]=bodies[i].x
    vect[2*i+1]=bodies[i].y
    vect[twonP+2*i]=bodies[i].vx
    vect[twonP+2*i+1]=bodies[i].vy
    i+=1
# ......................................................... vect2bodies
def vect2bodies(vect,bodies,nP):
  twonP=2*nP
  i=0
  while i<nP:
    bodies[i].x=vect[2*i]
    bodies[i].y=vect[2*i+1]
    bodies[i].vx=vect[twonP+2*i]
    bodies[i].vy=vect[twonP+2*i+1]
    i+=1
# ............................................... create input vector
def WriteInput(bodies,val,InpV):
  nP=len(bodies)
  nV=len(values)
  del InpV[:]
  i=0
  while i<nP:
    InpV.append(bodies[i].m)
    InpV.append(bodies[i].q)
    InpV.append(bodies[i].fr)
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
def ReadInput(InpV,bodies,masses,charges,frictions,val,vect):
  nP=len(bodies)
  nV=len(val)
  twonP=2*nP
  i=0
  while i<nP:
    bodies[i].m=masses[i]=InpV[7*i]
    bodies[i].q=charges[i]=InpV[7*i+1]
    bodies[i].fr=frictions[i]=InpV[7*i+2]
    bodies[i].x=vect[2*i]=InpV[7*i+3]
    bodies[i].y=vect[2*i+1]=InpV[7*i+4]
    bodies[i].vx=vect[twonP+2*i]=InpV[7*i+5]
    bodies[i].vy=vect[twonP+2*i+1]=InpV[7*i+6]
    i+=1
  j=0
  i=7*nP
  while j<nV:
    val[j]=InpV[i]
    i+=1
    j+=1
# ................................................ Elastics collision
def ElastColl(part1,part2):
  deltax=part2.x-part1.x
  deltay=part2.y-part1.y
  impactsq=(part1.rad+part2.rad)**2
  # .................................................... out of range
  if (deltax**2+deltay**2)>impactsq:
    return False
  else:
    if part1.collide==0:
      part1.collide=4
      part2.collide=4
      alpha=arctan2(deltay,deltax)
      csalpha=cos(alpha)
      snalpha=sin(alpha)
      Xi1=part1.vx*csalpha+part1.vy*snalpha
      Eta1=-part1.vx*snalpha+part1.vy*csalpha
      Xi2=part2.vx*csalpha+part2.vy*snalpha
      Eta2=-part2.vx*snalpha+part2.vy*csalpha
      NewXi1=((part1.m-part2.m)*Xi1+2.0*part2.m*Xi2)\
        /(part1.m+part2.m)
      NewXi2=((part2.m-part1.m)*Xi2+2.0*part1.m*Xi1)\
        /(part1.m+part2.m)
      part1.vx=NewXi1*csalpha-Eta1*snalpha
      part1.vy=NewXi1*snalpha+Eta1*csalpha
      part2.vx=NewXi2*csalpha-Eta2*snalpha
      part2.vy=NewXi2*snalpha+Eta2*csalpha
      return True
    else:
      return False
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
  scale*=2.0
  ScaleLab['text']="%8.3f"%(scale)
# ........................................................ Scale Down
def ScaleDown(*arg):
  global scale
  scale/=2.0
  ScaleLab['text']="%8.3f"%(scale)
# ....................................................... root window
root=Tk()
root.title('MultiElectron')
root.bind('<Return>',ReadData)
root.bind('<Control-plus>',ScaleUp)
root.bind('<Control-minus>',ScaleDown)
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
"""
ReadButton=Button(toolbar, text="Read Data", command=ReadData,width=11)
ReadButton.grid(row=nr,column=0,columnspan=2,sticky=W)
nr+=1
"""
CloseButton=Button(toolbar, text="Exit", command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,columnspan=2,sticky=W)
nr+=1
# ............................................................ Origin
Ox=cw/2
Oy=ch/2
orig=[Ox,Oy]
# ...................................................... input vector
InpV=[]
WriteInput(part,values,InpV)
nInp=len(InpV)
# ..................................................... odeint vector
y=[0]*4*nP
bodies2vect(part,y,nP)
# ........................................................ Input list
InputList=[]
i=0
while i<nP:
  InputList.append('m'+sub[i])
  InputList.append('q'+sub[i])
  InputList.append('\u03B7'+sub[i])  #     eta
  InputList.append('x'+sub[i])
  InputList.append('y'+sub[i])
  InputList.append('vx'+sub[i])
  InputList.append('vy'+sub[i])
  i+=1
InputList.append('K')
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
  LabInput[i].grid(row=nr%31,column=2*(nr//31))
  EntryInput.append(Entry(toolbar,bd=5,width=8))
  EntryInput[i].grid(row=nr%31,column=1+2*(nr//31))
  EntryInput[i].insert(0,"{:.3f}".format(InpV[i]))
  i+=1
  nr+=1
# ........................................................ time label
CycleLab0=Label(toolbar,text="Period:",font=("Helvetica",11))
CycleLab0.grid(row=nr%31,column=2*(nr//31))
CycleLab=Label(toolbar,text="     ",font=("Helvetica",11))
CycleLab.grid(row=nr%31,column=1+2*(nr//31),sticky=W)
nr+=1
# ....................................................... scale label
ScaleLab0=Label(toolbar,text="Scale:",font=("Helvetica",11))
ScaleLab0.grid(row=nr%31,column=2*(nr//31))
ScaleLab=Label(toolbar,text="%8.3f"%(scale),font=("Helvetica",11))
ScaleLab.grid(row=nr%31,column=1+2*(nr//31),sticky=W)
nr+=1
# .................................................................... function
def fun(yInp,t,params):
  KK,dt,cycle,nWake=params[0]             # unpack parameters
  mm=params[1]                            # unpack masses
  qq=params[2]                            # unpack charges
  fric=params[3]                          # unpack frictions
  nP=len(mm)
  twonP=2*nP
  twoN=2*nP
  fourN=4*nP
  ax=[0]*nP
  ay=[0]*nP
  i=1
  while i<nP:
    j=0
    while j<i:
      deltax=yInp[2*i]-yInp[2*j]
      deltay=yInp[2*i+1]-yInp[2*j+1]
      r2=deltax**2+deltay**2
      alpha=arctan2(deltay,deltax)
      ff=-KK*qq[i]*qq[j]/r2
      fx=ff*cos(alpha)
      fy=ff*sin(alpha)
      ax[i]-=fx/mm[i]
      ax[j]+=fx/mm[j]
      ay[i]-=fy/mm[i]
      ay[j]+=fy/mm[j]
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
  while i<nP:
    derivs.append(ax[i]-fric[i]*yInp[twonP+2*i])
    derivs.append(ay[i]-fric[i]*yInp[twonP+2*i+1])
    i+=1
  return derivs
# ........................................... numerical time interval
t=[0.0,0.03]
tt0=time.time()
tcount=0
while RunAll:
  StartIter=time.time()
  # ............................................. Draw Cartesian axes
  canvas.delete(ALL)
  # ............................................. draw blasts, if any
  i=0
  while i<nP:
    part[i].blast(canvas,orig)
    i+=1
  # ................................................ draw coordinates
  canvas.create_line(0,Oy,cw,Oy,fill="black")
  canvas.create_line(Ox,0,Ox,ch,fill="black")
  canvas.create_oval(Ox-bcrad,Oy-bcrad,Ox+bcrad,Oy+bcrad,fill="black")
  # ..................................................... draw bodies
  i=0
  while i<nP:
    part[i].draw(canvas,orig,nWake)
    i+=1
  # .................................................. center of mass
  cx,cy=baryc(part)[0]
  cx*=scale
  cy*=scale
  canvas.create_oval(Ox+cx-bcrad,Oy-cy-bcrad,Ox+cx+bcrad,Oy-cy+bcrad,\
    fill="black")
  # .......................................................... motion
  if RunIter:
    # ..................................................... next step
    psoln = odeint(fun,y,t,args=(params,))
    y=psoln[1,:]
    vect2bodies(y,part,nP)
    # ............................................. check if colliding
    i=1
    j=0
    coll=False
    while i<nP:
      while j<i:
        coll=(coll or ElastColl(part[i],part[j]))
        j+=1
      j=0
      i+=1
    if coll:
      bodies2vect(part,y,nP)
  # .................................................................
  else:
    if NewBaryc:
      ReWrite=True
      WriteInput(part,values,InpV)
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
      ReadInput(InpV,part,masses,charges,frictions,values,y)
      i=0
      while i<nInp:
        EntryInput[i].delete(0,'end')
        EntryInput[i].insert(0,"{:.3f}".format(InpV[i]))
        i+=1
      t=[0.0,values[1]]
      cycle=int(values[2])
      nWake=int(values[3])
      i=0
      while i<nP:
        del part[i].wakex[:]
        del part[i].wakey[:]
        part[i].wakex=[part[i].x]*nWake
        part[i].wakey=[part[i].y]*nWake
        i+=1
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
  