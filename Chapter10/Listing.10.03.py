#!/usr/bin/env python3
from tkinter import *
from scipy.integrate import odeint
import numpy as np
import time
# ............................................................. Lists
QtKey=['name','m','q','fr','x','y','vx','vy']
QtLab=['Name','Mass','Charge','\u03B7','x','y','vx','vy']
nQt=len(QtKey)
PrLab=['dt','\u03C4/ms','Trail length']
PrForm=['{:.3e}','{:d}','{:d}']
# .................................................. Global Variables
RunAll=True
GetPr=GetQt=RunMotion=False
# ................................................... Physical values
q=1.602176e-19        # elementary charge/Coulomb
me=9.10938e-31        # electron mass/kg
mp=1.67262e-27        # proton mass/kg
ke=8.98755179e9       # Coulomb's constant (N m**2/C**2)
r2=1.0e-10            # radius of second-electron orbit / m
r1=r2/3.0
v1=np.sqrt(ke*2.0*q**2/(me*r1)) # m/s
v2=np.sqrt(ke*q**2/(me*r2))     # m/s
dt=2.0e-19            # s
# .................................. Drawing and Animation Parameters
tau=10                # ms
scale=3.0e12          # px/m
cw=ch=900             # px
Ox,Oy=cw/2.0,ch/2.0
bcrad=2               # px
TrailLength=400
SelP=SelPr=SelQt=0
# ......................................................... Parameters
param=[dt,tau,TrailLength]
# ..................................................... Class Particle
class particle:
  def __init__(self,name,mass,charge,frict,x,y,vx,vy):
    self.name=name
    self.m=mass
    self.q=charge
    self.fr=frict
    self.x=x
    self.y=y
    self.vx=vx
    self.vy=vy
    if self.q>0:            # nucleus
      self.col='blue'
      self.rad=8
    else:                   # electron
      self.col='red'
      self.rad=4
    self.image=canvas.create_oval(circ([self.x,self.y],self.rad),\
      fill=self.col,outline=self.col)
    self.trail=meter2pix([self.x,self.y])*TrailLength
    self.TrailImg=canvas.create_line(self.trail,fill=self.col)
  # ................................................... Move Particle
  def redraw(self):
    canvas.coords(self.image,circ([self.x,self.y],self.rad))
    xx,yy=meter2pix([self.x,self.y])
    if np.linalg.norm([xx-self.trail[-2],yy-self.trail[-1]])>10:
      del self.trail[:2]
      self.trail.extend([xx,yy])
    canvas.coords(self.TrailImg,self.trail)
# ............................................... Start/Stop Function
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  butt[0]['text']='Stop' if RunMotion else 'Restart'
  for wg in butt[1:]+QtEntry+PrEntry:
    wg['state']=DISABLED if RunMotion else NORMAL
  SelectPart(0)
# ..................................................... Exit Function
def StopAll():
  global RunAll
  RunAll=False
# ........................................... Read Particol Variables
def ReadQt(WhichEntry):
  global GetQt,SelQt
  SelQt=WhichEntry
  GetQt=True  
# ................................................... Read Parameters
def ReadPr(WhichEntry):
  global GetPr,SelPr
  SelPr=WhichEntry
  GetPr=True
# ................................................ Canvas Coordinates
def meter2pix(pos):
  global Ox,Oy,scale
  for i,xy in enumerate(pos):
    pos[i]=Ox+scale*xy if i%2==0 else Oy-scale*xy
  return pos
# .............................................. Physical Coordinates
def pix2meter(pos):
  global Ox,Oy,scale
  for i,xy in enumerate(pos):
    pos[i]=(xy-Ox)/scale if i%2==0 else (Oy-xy)/scale
  return pos
# ................................................ Circle Coordinates
def circ(pos,radius):
  global Ox,Oy,scale
  xx,yy=meter2pix(pos)
  return [xx-radius,yy-radius,xx+radius,yy+radius]
# ................................................... Select Particle
def SelectPart(delta):
  global SelP
  SelP=(SelP+delta)%nP
  SelLab.config(text=part[SelP].name,fg=part[SelP].col)
  for i,vv in enumerate(list(part[SelP].__dict__.values())[1:nQt]):
    QtEntry[i].delete(0,'end')
    QtEntry[i].insert(0,f'{vv:.3e}')
# ........................................................ Scale Down
def ScaleUpDown(ud):
  global part,scale
  for p in part:
    p.trail=pix2meter(p.trail)
  scale*=np.sqrt(2)**ud
  ScaleLab['text']=f'{scale:10.3e}'
  for p in part:
    p.trail=meter2pix(p.trail)
# .......................... Evaluate Center of Mass and its Velocity
def baryc(part):
  mtot=sum(p.m for p in part)
  cx=sum(p.x*p.m for p in part)/mtot
  cy=sum(p.y*p.m for p in part)/mtot
  cvx=sum(p.vx*p.m for p in part)/mtot
  cvy=sum(p.vy*p.m for p in part)/mtot
  return [cx,cy,cvx,cvy]
# ..................................... Move Origin to Center of Mass
def SetBaryc():
  global state
  xcm,ycm,cvx,cvy=baryc(part)
  for i,p in enumerate(part):
    p.x-=xcm
    p.y-=ycm
    p.vx-=cvx
    p.vy-=cvy
    state[2*i:2*i+2]=[p.x,p.y]
    state[2*nP+2*i:2*nP+2*i+2]=[p.vx,p.vy]
  SelectPart(0)
# ...................................................... Reinitialize
def reinit():
  global part,r1,r2,state,v1,v2
  part[0].x=part[0].y=part[0].vx=part[0].vy=0.0
  part[1].x=-r1
  part[1].vy=-v1
  part[1].y=part[1].vx=0.0
  part[2].x=r2
  part[2].vy=v2
  part[2].y=part[2].vx=0.0
  for i,p in enumerate(part):
    state[2*i:2*i+2]=[p.x,p.y]
    state[2*nP+2*i:2*nP+2*i+2]=[p.vx,p.vy]
    p.trail=meter2pix([p.x,p.y])*TrailLength
  SelectPart(0)
# .............................................................. dfdt
def dfdt(state,t):
  x=state[:2*nP:2]
  y=state[1:2*nP:2]
  vx=state[2*nP::2]
  vy=state[2*nP+1::2]
  distx=x-(np.tile(x,(len(x),1))).T
  disty=y-(np.tile(y,(len(y),1))).T
  alpha=np.arctan2(disty,distx)
  r2=np.square(distx)+np.square(disty)
  np.fill_diagonal(r2,1.0)
  q2=-ke*(np.tile(charge,(len(charge),1)).T*charge)
  ff=np.divide(q2,r2)
  np.fill_diagonal(ff,0.0)
  fx=ff*np.cos(alpha)
  fy=ff*np.sin(alpha)
  DerivState=np.roll(state,2*nP)
  DerivState[2*nP::2]=(fx.sum(axis=1)-(vx*frict))/mass
  DerivState[2*nP+1::2]=(fy.sum(axis=1)-(vy*frict))/mass
  return DerivState
# ....................................................... Root Window
root=Tk()
root.title('Classical Helium Atom (odeint)')
root.bind('<Control-plus>',lambda event,num=1:ScaleUpDown(num))
root.bind('<Control-minus>',lambda event,num=-1:ScaleUpDown(num))
# ............................................................ canvas
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# ........................................................... Toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
toolbar.option_add('*Font','Helvetica 11')
# ............................................................ Buttons
nr=0
butt=[]
ButtLab=['Start','Set Barycenter','Reinitialize','Exit']
ButtComm=[StartStop,SetBaryc,reinit,StopAll]
for i,(ll,cc) in enumerate(zip(ButtLab,ButtComm)):
  butt.append(Button(toolbar,text=ll,command=cc,width=11))
  butt[i].grid(row=nr,column=0,sticky=W)
  nr+=1
# .................................................. Create Particles
part=[]
part.append(particle('Nucleus',4.0*mp,2.0*q,0.0,0.0,0.0,0.0,0.0))
part.append(particle('Electron 1',me,-q,0.0,-r1,0.0,0.0,-v1))
part.append(particle('Electron 2',me,-q,0.0,r2,0.0,0.0,v2))
nP=len(part)
# ....................... Initial State, Charges, Masses and Friction
state=np.array([0.0]*4*nP)
charge=np.array([0.0]*nP)
mass=np.array([0.0]*nP)
frict=np.array([0.0]*nP)
for i,p in enumerate(part):
  state[2*i:2*i+2]=[p.x,p.y]
  state[2*nP+2*i:2*nP+2*i+2]=[p.vx,p.vy]
  charge[i]=p.q
  mass[i]=p.m
  frict[i]=p.fr
# ........................................... Selected Particle Label
Label(toolbar,text='Selected Particle:',pady=20).grid(row=nr,column=0)
SelLab=Label(toolbar,text=part[0].name,width=15,bg='#ffffff')
SelLab.grid(row=nr,column=1)
SelLab.bind('<Button-5>',lambda event,num=-1:SelectPart(num))
SelLab.bind('<Button-1>',lambda event,num=-1:SelectPart(num))
SelLab.bind('<Button-4>',lambda event,num=1:SelectPart(num))
SelLab.bind('<Button-3>',lambda event,num=1:SelectPart(num))
nr+=1
# .............. Entries for Physical Quantities of Selected Particle
QtEntry=[]
for i,kk in enumerate(QtKey[1:]):
  Label(toolbar,text=QtLab[i+1]).grid(row=nr,column=0)
  QtEntry.append(Entry(toolbar,bd=3,width=16))
  QtEntry[i].grid(row=nr,column=1)
  QtEntry[i].insert(0,f'{part[0].__dict__[str(kk)]:.3e}')
  QtEntry[i].bind('<Return>',lambda event,num=i:ReadQt(num))
  nr+=1
# ......................................................... Separator
Label(toolbar,text='  ').grid(row=nr,column=0)
nr+=1
# ............................................ Entries for Parameters
PrEntry=[]
for i,pl in enumerate(PrLab):
  Label(toolbar,text=pl).grid(row=nr,column=0)
  PrEntry.append(Entry(toolbar,bd=3,width=16))
  PrEntry[i].grid(row=nr,column=1)
  PrEntry[i].insert(0,PrForm[i].format(param[i]))
  PrEntry[i].bind('<Return>',lambda event,num=i:ReadPr(num))
  nr+=1
# ....................................................... Cycle Label
Label(toolbar,text='Period:',).grid(row=nr,column=0)
CycleLab=Label(toolbar,text='     ')
CycleLab.grid(row=nr,column=1,sticky=W)
nr+=1
# ....................................................... Scale Label
Label(toolbar,text='Scale:').grid(row=nr,column=0)
ScaleLab=Label(toolbar,text=f'{scale:10.3e}')
ScaleLab.grid(row=nr,column=1,sticky=W)
nr+=1
# .............................................. Draw Coordinate Axes
canvas.create_line(0,Oy,cw,Oy,fill='black')
canvas.create_line(Ox,0,Ox,ch,fill='black')
# ................................. Create Barycenter Image on Canvas
bc=canvas.create_oval(circ([0,0],bcrad),fill='black')
# ................................................... Initialize Time
tt0=time.time()
tcount=0
t=[0,dt]
# .................................................... Animation Loop
while RunAll:
  StartIter=time.time()
  # .................................................. Draw Particles
  for p in part:
    p.redraw()
  # ................................................. Draw Barycenter
  cx,cy=baryc(part)[:2]
  canvas.coords(bc,circ([cx,cy],bcrad))
  canvas.update()
  # .......................................................... motion
  if RunMotion:
    # ................................................... Call odeint
    psoln=odeint(dfdt,state,t)
    state=psoln[1,:]
    for i,p in enumerate(part):
      p.x,p.y=state[2*i:2*i+2]
      p.vx,p.vy=state[2*nP+2*i:2*nP+2*i+2]
  elif GetPr: # ................................... Read Parameters
    try:
      vv=float(PrEntry[SelPr].get())
    except ValueError:
      pass
    else:
      if SelPr==1 or SelPr==2:
        vv=int(vv)
      param[SelPr]=vv
      PrEntry[SelPr].delete(0,'end')
      PrEntry[SelPr].insert(0,PrForm[SelPr].format(vv))
      # ...................................... If TrailLength Changed
      dTrail=param[2]-TrailLength
      if dTrail<0:
        for p in part:
          del p.trail[:2*abs(dTrail)]
      elif dTrail>0:
        for p in part:
          NewPoints=meter2pix([p.trail[0],p.trail[1]])*dTrail
          p.trail=NewPoints+p.trail
      # .............................................................
      dt,tau,TrailLength=param
      t=[0,dt]
    GetPr=False
  elif GetQt:  # ............................ Read Particle Variables
    try:
      part[SelP].__dict__[str(QtKey[SelQt+1])]=vv=\
        float(QtEntry[SelQt].get())
    except ValueError:
      pass
    else:
      QtEntry[SelQt].delete(0,'end')
      QtEntry[SelQt].insert(0,f'{vv:.3e}')
      state[2*SelP:2*SelP+2]=[part[SelP].x,part[SelP].y]
      state[2*nP+2*SelP:2*nP+2*SelP+2]=[part[SelP].vx,part[SelP].vy]
      charge[SelP]=part[SelP].q
      mass[SelP]=part[SelP].m
      frict[SelP]=part[SelP].fr
    GetQt=False
  # ................................................ Cycle Duration
  tcount+=1
  if tcount>=10:
    tcount=0
    ttt=time.time()
    elapsed=ttt-tt0
    CycleLab['text']=f'{elapsed*100:8.3f}'+' ms'
    tt0=ttt
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-ElapsIter)
#--------------------------------------------------------------- Exit
root.destroy()
  
