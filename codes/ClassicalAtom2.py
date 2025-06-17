#!/usr/bin/env python3
from tkinter import *
from scipy.integrate import odeint
import numpy as np
import time
# ............................................. subscripts for labels
sub=['\u2080','\u2081','\u2082','\u2083','\u2084','\u2085',\
  '\u2086','\u2087','\u2088','\u2089']
# .................................................. Global variables
RunAll=True
RunIter=GetData=False
# ............................... Class particle (nucleus, electrons)
class particle:
  def __init__(self,mass,charge,frict,x,y,vx,vy):
    self.m=mass
    self.q=charge
    self.fr=frict
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    if self.q>0:            # nucleus
      self.col='red'
      self.rad=8
    else:                   # electron
      self.col='blue'
      self.rad=4
    self.image=canvas.create_oval(Ox+scale*self.x-self.rad,\
      Oy-scale*self.y+self.rad,Ox+scale*self.x+self.rad,\
        Oy-scale*self.y-self.rad,fill=self.col,outline=self.col)
    self.trail=np.array([self.x,self.y]*TrailLength)
    self.ScaledTrail=[0.0,0.0]*TrailLength
    self.TrailImg=canvas.create_line(self.ScaledTrail,fill=self.col)
  # ......................................... move particle and trail
  def move(self):
    # ................................................. move particle
    canvas.coords(self.image,Ox+scale*self.x-self.rad,\
      Oy-scale*self.y+self.rad,Ox+scale*self.x+self.rad,\
        Oy-scale*self.y-self.rad)
    # .................................................... move trail
    dist2=(self.x-self.trail[0])**2+(self.y-self.trail[1])**2
    if (scale2*dist2)>100:
      self.trail=np.roll(self.trail,2)
      self.trail[0]=self.x
      self.trail[1]=self.y
    self.ScaledTrail[::2]=[Ox+scale*tr for tr in self.trail[::2]]
    self.ScaledTrail[1::2]=[Oy-scale*tr for tr in self.trail[1::2]]
    canvas.coords(self.TrailImg,self.ScaledTrail)
# ............................................... Start/Stop function
def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StartButton['text']='Stop'
    CloseButton['state']=DISABLED
    for ep in EntryPar:
      ep['state']=DISABLED
  else:
    StartButton['text']='Restart'
    CloseButton['state']=NORMAL
    for ep in EntryPar:
      ep['state']=NORMAL
# ..................................................... Exit function
def StopAll():
  global RunAll
  RunAll=False
# ................................................ Read Data function
def ReadData(*arg):
  global GetData
  if not RunIter:
    GetData=True
# ........................................................ Scale Down
def ScaleDown(*arg):
  global scale,scale2
  scale/=np.sqrt(2.0)
  scale2/=2.0
  ScaleLab['text']='{:10.3e}'.format(scale)
# .......................................................... Scale Up
def ScaleUp(*arg):
  global scale,scale2
  scale*=np.sqrt(2.0)
  scale2*=2.0
  ScaleLab['text']='{:10.3e}'.format(scale)
# ..................................... move origin to center of mass
def SetBaryc():
  #  ...................... evaluate barycenter position and velocity
  mtot=sum(pp.m for pp in part)
  cx=sum(pp.x*pp.m for pp in part)/mtot
  cy=sum(pp.y*pp.m for pp in part)/mtot
  cvx=sum(pp.vx*pp.m for pp in part)/mtot
  cvy=sum(pp.vy*pp.m for pp in part)/mtot
  # .......... particles positions and velocities in barycenter frame
  for pp in part:
    pp.x-=cx
    pp.y-=cy
    pp.vx-=cvx
    pp.vy-=cvy
    pp.trail[::2]-=cx
    pp.trail[1::2]-=cy
  StartVal[::4]-=cx
  StartVal[1::4]-=cy
  StartVal[2::4]-=cvx
  StartVal[3::4]-=cvy
  # ............................ parameter values in barycenter frame
  params[5:nPartPar:7]-=cvx
  params[6:nPartPar:7]-=cvy
  # ................................................. rewrite entries
  for ep,pp in zip(EntryPar,params):
    ep['state']=NORMAL
    ep.delete(0,'end')
    ep.insert(0,'{:.3e}'.format(pp))
    if RunIter:
      ep['state']=DISABLED
# ................................................... Physical values
q=1.602176e-19        # elementary charge/Coulomb
me=9.10938e-31        # electron mass/kg
mp=1.67262e-27        # proton mass/kg
ke=8.987551e9         # Coulomb's constant (N m^2/C^2)
r2=1.0e-10            # radius of second-electron orbit / m
r1=r2/3.0
v1=np.sqrt(ke*2.0*q**2/(me*r1)) # m/s
v2=np.sqrt(ke*q**2/(me*r2))     # m/s
dt=2.0e-19            # s
# .................................. Drawing and animation parameters
cycle=20              # ms
scale=3.0e12          # px/m
scale2=scale*scale    # px^2/m^2
cw=900                # px
ch=900                # px
Ox=cw/2.0
Oy=ch/2.0
bcrad=2               # px
TrailLength=400
# ....................................................... root window
root=Tk()
root.title('Classical Helium Atom')
root.bind('<Return>',ReadData)
root.bind('<Control-plus>',ScaleUp)
root.bind('<Control-minus>',ScaleDown)
# ............................................................ canvas
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# ........................................................... toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1, sticky=N)
# ............................................................ buttons
nr=0
StartButton=Button(toolbar,text='Start',command=StartStop,width=11)
StartButton.grid(row=nr,column=0,sticky=W)
BarycButton=Button(toolbar, text='Set Barycenter',\
  command=SetBaryc,width=11)
BarycButton.grid(row=nr,column=1,sticky=W)
nr+=1
CloseButton=Button(toolbar, text='Exit', command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,columnspan=2,sticky=W)
nr+=1
# .............................................. draw coordinate axes
canvas.create_line(0,Oy,cw,Oy,fill='black')
canvas.create_line(Ox,0,Ox,ch,fill='black')
# ................................................. Create particles
part=[]
part.append(particle(4.0*mp,2.0*q,0.0,0.0,0.0,0.0,0.0))    # nucleus
part.append(particle(me,-q,0.0,-r1,0.0,0.0,-v1))        # electron 1
part.append(particle(me,-q,0.0,r2,0.0,0.0,v2))          # electron 2
nPart=len(part)
nPartPar=7*nPart
# .............................................. Parameter-value list
values=[ke,dt,cycle,TrailLength]
# ...................................................... input vector
params=np.array([0.0]*(7*nPart+len(values)))
StartVal=np.array([0.0]*4*nPart)
# .................................................. write parameters
params[:nPartPar:7]=[pp.m for pp in part]
params[1:nPartPar:7]=[pp.q for pp in part]
params[2:nPartPar:7]=[pp.fr for pp in part]
params[3:nPartPar:7]=StartVal[::4]=[pp.x for pp in part]
params[4:nPartPar:7]=StartVal[1::4]=[pp.y for pp in part]
params[5:nPartPar:7]=StartVal[2::4]=[pp.vx for pp in part]
params[6:nPartPar:7]=StartVal[3::4]=[pp.vy for pp in part]
params[nPartPar::]=values
# ................................................... parameter names
ParStr=[]
VarName=['m','q','\u03B7','x','y','vx','vy']
ParName=['Ke','dt','Cycle/ms','Tail']
for i in range(nPart):
  for nm in VarName:
    ParStr.append(nm+sub[i])
for nm in ParName:
  ParStr.append(nm)
# ................................. Labels and Entries for parameters
LabPar=[]
EntryPar=[]
for i,ps in enumerate(ParStr):
  LabPar.append(Label(toolbar,text=ps,font=('Helvetica',11)))
  LabPar[i].grid(row=nr,column=0)
  EntryPar.append(Entry(toolbar,bd=3,width=12))
  EntryPar[i].grid(row=nr,column=1)
  EntryPar[i].insert(0,'{:.3e}'.format(params[i]))
  nr+=1
# ........................................................ time label
CycleLab0=Label(toolbar,text='Period:',font=('Helvetica',11))
CycleLab0.grid(row=nr,column=0)
CycleLab=Label(toolbar,text='     ',font=('Helvetica',11))
CycleLab.grid(row=nr,column=1,sticky=W)
nr+=1
# ....................................................... scale label
ScaleLab0=Label(toolbar,text='Scale:',font=('Helvetica',11))
ScaleLab0.grid(row=nr,column=0)
ScaleLab=Label(toolbar,text='%10.3e'%(scale),font=('Helvetica',11))
ScaleLab.grid(row=nr,column=1,sticky=W)
nr+=1
# .......................................................... function
def dfdt(OdeInp,t,pp):
  mm=np.array(pp[:nPartPar:7])                   # masses from params
  qq=pp[1:nPartPar:7]                           # charges from params
  fr=np.array(pp[2:nPartPar:7])             # drag forces from params
  # ................... initial conditions for differential equations
  x=OdeInp[::4]
  y=OdeInp[1::4]
  vx=np.array(OdeInp[2::4])
  vy=np.array(OdeInp[3::4])
  # ................................... Coulomb contribution to force
  distx=x-(np.tile(x,(len(x),1))).T
  disty=y-(np.tile(y,(len(y),1))).T
  alpha=np.arctan2(disty,distx)
  r2=np.square(distx)+np.square(disty)
  np.fill_diagonal(r2,1.0)
  q2=-ke*(np.tile(qq,(len(qq),1)).T*qq)
  ff=np.divide(q2,r2)
  np.fill_diagonal(ff,0.0)
  fx=ff*np.cos(alpha)
  fy=ff*np.sin(alpha)
  # ........................... Accelerations, including linear drags
  ax=(fx.sum(axis=1)-(vx*fr))/mm
  ay=(fy.sum(axis=1)-(vy*fr))/mm
  # ............................................... Build output list
  derivs=[0]*len(OdeInp)
  derivs[::4]=vx
  derivs[1::4]=vy
  derivs[2::4]=ax
  derivs[3::4]=ay
  # ...........................................................
  return derivs
# ........................................... numerical time interval
t=[0.0,dt]
tt0=time.time()
tcount=0
# ......................................................... main loop
while RunAll:
  StartIter=time.time()
  # .................................................. draw particles
  for pp in part:
    pp.move()
  canvas.update()
  # .......................................................... motion
  if RunIter:
    # ..................................................... next step
    psoln = odeint(dfdt,StartVal,t,args=(params,))
    StartVal=psoln[1,:]
    for i,pp in enumerate(part):
      pp.x=StartVal[4*i]
      pp.y=StartVal[4*i+1]
      pp.vx=StartVal[4*i+2]
      pp.vy=StartVal[4*i+3]
  # .................................................................
  elif GetData:
    for i,ep in enumerate(EntryPar):
      try:
        params[i]=float(ep.get())
      except ValueError:
        pass
    for i,pp in enumerate(part):
      pp.m=params[i*7]
      pp.q=params[i*7+1]
      pp.fr=params[i*7+2]
      pp.x=StartVal[i*4]=params[i*7+3]
      pp.y=StartVal[i*4+1]=params[i*7+4]
      pp.vx=StartVal[i*4+2]=params[i*7+5]
      pp.vy=StartVal[i*4+3]=params[i*7+6]
    values[::]=params[nPartPar::]
    for ep,yy in zip(EntryPar,params):
      ep.delete(0,'end')
      ep.insert(0,'{:.3e}'.format(yy))
    dt=values[1]
    t=[0.0,dt]
    cycle=int(values[2])
    TrailLength=int(values[3])
    for pp in part:
      pp.trail=np.array([pp.x,pp.y]*TrailLength)
      pp.ScaledTrail=[0.0,0.0]*TrailLength
    GetData=False
  # ................................................ cycle duration
  tcount+=1
  if tcount>=10:
    tcount=0
    ttt=time.time()
    elapsed=ttt-tt0
    CycleLab['text']='%8.3f'%(elapsed*100.0)+' ms'
    tt0=ttt
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(cycle-ElapsIter)
#----------------------------------------------------------------------
root.destroy()
  
