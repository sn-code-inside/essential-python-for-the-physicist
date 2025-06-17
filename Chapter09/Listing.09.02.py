#!/usr/bin/env python3
from tkinter import *
from scipy.integrate import odeint,solve_ivp
from datetime import timedelta
import numpy as np
import time
# .................................................. Global variables
RunAll=True
GetData=RunMotion=False
# ........................................................... Methods
EULER,VERLET,ODEINT,YOSHIDA=range(4)
method=['Euler','Verlet','odeint','Yoshida']
col=['magenta','blue','red','green','black']
ITER,ELAPSED,ORBITS,PERIOD,CYCLE,SCALE=range(6)
quant=['Iterations','Elapsed Time','Orbits','Orbital Period',\
  'Cycle','Scale']
# ................................................... Physical values
ME=5.9722e24           # Earth mass/kg
G=6.674e-11            # Gravitational constant [m^3/(kg s^2)]
GM=ME*G
dt=10.0                # s
dT=3*dt                # s
step=[dt,dt,dT,dT]
# ................................................. Yoshida Constants
Theta=1.0/(2-2**(1.0/3.0))
CX1=CX4=0.5*Theta
CX2=CX3=0.5*(1.0-Theta)
CV1=CV3=Theta
CV2=1.0-2.0*Theta
# .................................. Drawing and Animation Parameters
tau=1                  # ms
scale=1.0e-5           # px/m
cw,ch=600,500          # px
Ox,Oy=cw//4,ch//2
rad=4                  # px
ms=1.0e3               # satellite mass/kg
TrailLength=400
x0=4.0e7               # satellite apogee/m 
vx0=0.0
y0=0.0
vy0=0.5*np.sqrt(GM/x0) # ~1580 m/s
# ............................................... Start/Stop function
def StartStop():
  global butts,TimeEntry,RunMotion
  RunMotion=not RunMotion
  butts[0]['text']='Stop' if RunMotion else 'Restart'
  for widg in butts[2:]+TimeEntry:
    widg['state']=DISABLED if RunMotion else NORMAL
# ..................................................... Exit function
def StopAll():
  global RunAll
  RunAll=False
# ................................................ Canvas Coordinates
def meter2pix(pos):
  global Ox,Oy,scale
  CanvPos=[]
  for i,xy in enumerate(pos):
    CanvPos.append(Ox+scale*xy if i%2==0 else Oy-scale*xy)
  return CanvPos
# .............................................. Physical Coordinates
def pix2meter(pos):
  global Ox,Oy,scale
  PhysPos=[]
  for i,xy in enumerate(pos):
    PhysPos.append((xy-Ox)/scale if i%2==0 else (Oy-xy)/scale)
  return PhysPos
# ................................................ Circle Coordinates
def circ(pos,radius):
  global Ox,Oy,scale
  xx,yy=meter2pix(pos)
  return [xx-radius,yy-radius,xx+radius,yy+radius]
# ..................................................... Scale up/down
def ScaleUpDown(event,ud=0):
  global scale,trail
  for i,tr in enumerate(trail):
    trail[i]=pix2meter(tr)
  scale*=np.sqrt(2)**ud
  for i,tr in enumerate(trail):
    trail[i]=meter2pix(tr)
  QtLab[SCALE]['text']=f'{scale:10.3e}'
# ........................................................ Read Entry
def ReadData(*args):
  global GetData
  GetData=True
# ..................................................... Time Reversal
def TimeReversal():
  global step,dt,dT
  dt=-dt
  dT=3*dt
  step=[dt,dt,dT,dT]
# ...................................................... acceleration  
def accel(pos):
  aa=-GM/np.dot(pos,pos)
  theta=np.arctan2(pos[1],pos[0])
  ax=aa*np.cos(theta)
  ay=aa*np.sin(theta)
  return np.array([ax,ay])
# ............................................................ energy
def ener(state):
  pot=-GM*ms/np.linalg.norm(state[:2])
  kin=0.5*ms*np.dot(state[2:],state[2:])
  return pot+kin
# ................................................... odeint Function
def dfdt(state,t):
  ax,ay=accel(state[:2])
  vx,vy=state[2:]
  return [vx,vy,ax,ay]
# .................................................. odeint Algorithm
def OdeintAlgo(state,step):
  tt=[0,step]
  psoln=odeint(dfdt,state,tt)
  state=psoln[1]
  return state
# ................................................. Yoshida Algorithm
def yoshida(state,h):
  state[:2]+=CX1*h*state[2:]
  state[2:]+=CV1*h*accel(state[:2])
  state[:2]+=CX2*h*state[2:]
  state[2:]+=CV2*h*accel(state[:2])
  state[:2]+=CX3*h*state[2:]
  state[2:]+=CV3*h*accel(state[:2])
  state[:2]+=CX4*h*state[2:]
  return state
# .................................................. Verlet Algorithm
def verlet(state,h):
  global VerlAccel
  for _ in range(3):
    state[2:]+=0.5*h*VerlAccel
    state[:2]+=h*state[2:]
    VerlAccel=accel(state[:2])
    state[2:]+=0.5*h*VerlAccel
  return state
# ................................................... Euler Algorithm
def euler(state,h):
  for _ in range(3):
    state[:2]+=h*state[2:]
    state[2:]+=h*accel(state[:2])
  return state
# .................................................... Algorithm List
algo=[euler,verlet,OdeintAlgo,yoshida]
# ....................................................... Root Window
root=Tk()
root.title('Gravitational Orbit')
root.bind('<Control-plus>',lambda event,num=1:ScaleUpDown(None,num))
root.bind('<Control-minus>',lambda event,num=-1:ScaleUpDown(None,num))
root.bind('<Return>',ReadData)
# ............................................................ Canvas
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# ........................................................... Toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
toolbar.columnconfigure(1,minsize=130)
toolbar.option_add('*Font','Helvetica 11')
# ............................................................ Buttons
nr=0
butts=[]
ButtLab=['Start','Time Reversal','Exit']
ButtComm=[StartStop,TimeReversal,StopAll]
for i,(ll,cc) in enumerate(zip(ButtLab,ButtComm)):
  butts.append(Button(toolbar,text=ll,command=cc,width=11))
  butts[i].grid(row=nr,column=0,sticky=W)
  nr+=1
# ...................................................... Time Entries
TimeEntry=[]
TimeTxt=['Time Step/s','\u03C4/ms']
inputs=[dt,tau]
tfor=['{:.2f}','{:d}']
ttype=[float,int]
for i,tt in enumerate(TimeTxt):
  lb=Label(toolbar,text=tt)
  lb.grid(row=nr,column=0)
  TimeEntry.append(Entry(toolbar,bd=5,width=11))
  TimeEntry[i].grid(row=nr,column=1)
  TimeEntry[i].insert(0,tfor[i].format(inputs[i]))
  nr+=1
# ..................................................... Energy Labels
EnLab=[]
for i,mm in enumerate(method+['Initial']):
  lab=Label(toolbar,text=mm+' Energy')
  lab.grid(row=nr,column=0)
  EnLab.append(Label(toolbar,text='     '))
  EnLab[i].grid(row=nr,column=1)
  EnLab[i].config(fg=col[i])
  nr+=1
# ...................................................... Other Labels
QtLab=[]
for i,qt in enumerate(quant):
  lab=Label(toolbar,text=qt)
  lab.grid(row=nr,column=0)
  QtLab.append(Label(toolbar,text='0'))
  QtLab[i].grid(row=nr,column=1)
  nr+=1
QtLab[SCALE]['text']=f'{scale:10.3e}'
# .................................... Draw Coordinate Axes and Earth
canvas.create_line(0,Oy,cw,Oy,fill='black')
canvas.create_line(Ox,0,Ox,ch,fill='black')
canvas.create_oval(circ([0,0],8),fill='#50a0ff',outline='#50a0ff')
# ............................ Create Satellite Image for Each Method
Image,trail,ImTrail,state=([] for _ in range(4))
for i,mm in enumerate(method):
  Image.append(canvas.create_oval(circ([x0,y0],rad),fill=col[i]))
  trail.append(meter2pix([x0,y0])*TrailLength)
  ImTrail.append(canvas.create_line(trail[i],fill=col[i]))
  state.append(np.array([x0,y0,vx0,vy0]))
ypair=[y0,y0]
# ........................ Initial Accelerations for Verlet Algorithm
VerlAccel=accel([x0,y0])
# .................................................... Initial Energy
en=ener([x0,y0,vx0,vy0])
for el in EnLab:
  el.config(text=f'{en:.6e}')
# ........................................................ Initialize
tt0=time.time()
tcount=nIter=nOrbits=0
Telaps=0.0
# .................................................... Animation Loop
while RunAll:
  StartIter=time.time()
  # ........................................... Draw Satellite Images
  for i,ima in enumerate(Image):
    canvas.coords(ima,circ(state[i][:2],rad))
    canvas.coords(ImTrail[i],trail[i])
  # .......................................................... update
  canvas.update()
  # .......................................................... motion
  if RunMotion:
    # ........................................... update elapsed time
    Telaps+=dT
    # ......................................... Move Satellite Images
    for i,(al,tr) in enumerate(zip(algo,trail)):
      state[i]=al(state[i],step[i])
      # ............................................... Update Trails
      xx,yy=meter2pix(state[i][:2])
      if np.linalg.norm([xx-tr[-2],yy-tr[-1]])>10:
        del trail[i][:2]
        trail[i].extend([xx,yy])
    # .................................................. Count Orbits
    ypair[0]=ypair[1]
    ypair[1]=state[YOSHIDA][1]
    if ypair[0]<0 and ypair[1]>0:
      nOrbits+=1
      QtLab[ORBITS]['text']=str(nOrbits)
      OrbPeriod=Telaps/nOrbits
      QtLab[PERIOD]['text']=str(timedelta(seconds=int(OrbPeriod)))
    # ........................................ show iteration counter
    nIter+=1
    if nIter%20==0:
      QtLab[ELAPSED]['text']=str(timedelta(seconds=int(Telaps)))
      QtLab[ITER]['text']=str(nIter)
      for i,st in enumerate(state):
        EnLab[i]['text']=f'{ener(st):.6e}'
  elif GetData:
    # ...................................... Read Entries and Restart
    tauOld=tau
    for i,te in enumerate(TimeEntry):
      try:
        inputs[i]=ttype[i](te.get())
      except ValueError:
        pass
      te.delete(0,END)
      te.insert(0,tfor[i].format(inputs[i]))
    dt,tau=inputs
    dT=3*dt
    step=[dt,dt,dT,dT]
    # ................................... Resets Positions and Trails
    if tau==tauOld:
      for i,mm in enumerate(method):
        state[i]=np.array([x0,y0,vx0,vy0])
        trail[i]=meter2pix([x0,y0])*TrailLength
      ypair=[y0,y0]
      VerlAccel=accel([x0,y0])
      nOrbits=0
      Telaps=0.0
    GetData=False
  # ................................................ Cycle Duration
  tcount+=1
  if tcount>=10:
    tcount=0
    ttt=time.time()
    elapsed=ttt-tt0
    QtLab[CYCLE]['text']=f'{elapsed*100.0:8.3f}'+' ms'
    tt0=ttt
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-ElapsIter)
#----------------------------------------------------------------------
root.destroy()
  
