#!/usr/bin/env python3
from tkinter import *
from datetime import timedelta
import numpy as np
from numpy.linalg import norm
import time
# .................................................. Global variables
RunAll=True
GetData=RunMotion=False
# ................................................... Physical values
ME=5.9722e24          # Earth mass/kg
G=6.674e-11           # Gravitational constant [m^3/(kg s^2)]
GM=ME*G
dt=10.0               # s
# .................................. Drawing and Animation Parameters
tau=5                 # ms
scale=5.0e-6          # px/m
cw=600                # px
ch=500                # px
Ox,Oy=cw//4,ch//2.0
rad=4                 # px
ms=1.0e3              # satellite mass
TrailLength=400
x0=4.0e7
y0=0.0
vx0=0.0
vy0=0.5*np.sqrt(GM/x0)
col='red'
# ............................................. Define Some Constants
INITENER,EULERENER,ITER,ELAPSED,ORBITS,PERIOD,CYCLE,SCALE=range(8)
quant=['Initial Energy','Euler-Cromer Energy','Iterations',\
  'Elapsed Time','Orbits','Orbital Period','Cycle','Scale']
# ............................................... Start/Stop function
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  StartButton['text']='Stop' if RunMotion else 'Restart'
  for wg in [CloseButton]+TimEntry:
    wg['state']=DISABLED if RunMotion else NORMAL
# ..................................................... Exit function
def StopAll():
  global RunAll
  RunAll=False
# ......................................................... meter2pix
def meter2pix(pos):
  global Ox,Oy,scale
  for i,xy in enumerate(pos):
    pos[i]=Ox+scale*xy if i%2==0 else Oy-scale*xy
  return pos
# ......................................................... pix2meter
def pix2meter(pos):
  global Ox,Oy,scale
  for i,xy in enumerate(pos):
    pos[i]=(xy-Ox)/scale if i%2==0 else (Oy-xy)/scale
  return pos
# ................................................ Circle Coordinates
def circ(x,y,radius):
  global Ox,Oy,scale
  xx,yy=meter2pix([x,y])
  return [xx-radius,yy-radius,xx+radius,yy+radius]
# ........................................................ Scale Down
def ScaleUpDown(ud):
  global scale,trail
  trail=pix2meter(trail)
  scale*=np.sqrt(2)**ud
  trail=meter2pix(trail)
  QtLab[SCALE]['text']=f'{scale:10.3e}'
# ...................................................... Read Entries
def ReadData(event):
  global GetData
  GetData=True
# ...................................................... Acceleration  
def accel(x,y):
  r2=x**2+y**2
  aa=-GM/r2
  alpha=np.arctan2(y,x)
  ax=aa*np.cos(alpha)
  ay=aa*np.sin(alpha)
  return [ax,ay]
# ............................................................ Energy
def ener(x,y,vx,vy):
  r=norm([x,y])
  pot=-GM*ms/r
  kin=0.5*ms*(vx**2+vy**2)
  return pot+kin
# ..................................................... Time Reversal
def TimeReversal():
  global dt
  dt=-dt
# ....................................................... Root Window
root=Tk()
root.title('Euler-Cromer Satellite')
root.bind('<Control-plus>',lambda event,num=1:ScaleUpDown(num))
root.bind('<Control-minus>',lambda event,num=-1:ScaleUpDown(num))
# ............................................................ Canvas
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# ........................................................... Toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
toolbar.columnconfigure(1,minsize=120)
# ............................................................ Buttons
nr=0
StartButton=Button(toolbar,text='Start',command=StartStop,width=11)
StartButton.grid(row=nr,column=0,sticky=W)
nr+=1
TimeRevButton=Button(toolbar,text='Time Reversal',\
  command=TimeReversal,width=11)
TimeRevButton.grid(row=nr,column=0,sticky=W)
nr+=1
CloseButton=Button(toolbar, text='Exit', command=StopAll,width=11)
CloseButton.grid(row=nr,column=0,columnspan=2,sticky=W)
nr+=1
# ...................................................... Time Entries
TimEntry=[]
TimeTxt=['Time Step/s','\u03C4/ms']
tVal=[dt,tau]
tfor=['{:.2f}','{:d}']
for i,tt in enumerate(TimeTxt):
  lb=Label(toolbar,text=tt,font=('Helvetica',11))
  lb.grid(row=nr,column=0)
  TimEntry.append(Entry(toolbar,bd=5,width=11))
  TimEntry[i].grid(row=nr,column=1)
  TimEntry[i].insert(0,tfor[i].format(tVal[i]))
  TimEntry[i].bind('<Return>',ReadData)
  nr+=1
# ............................................................ Labels
QtLab=[]
for i,qt in enumerate(quant):
  lab=Label(toolbar,text=qt,font=('Helvetica',11))
  lab.grid(row=nr,column=0)
  QtLab.append(Label(toolbar,text='0',font=('Helvetica',11)))
  QtLab[i].grid(row=nr,column=1)
  nr+=1
QtLab[SCALE]['text']=f'{scale:10.3e}'
nr+=1
# .............................................. Draw Coordinate Axes
canvas.create_line(0,Oy,cw,Oy,fill='black')
canvas.create_line(Ox,0,Ox,ch,fill='black')
canvas.create_oval(circ(0,0,8),fill='#50a0ff',outline='#50a0ff')
# .................................................... Initial Values
x,y,vx,vy=[x0,y0,vx0,vy0]
# ................................................... Euler Satellite
SatImg=canvas.create_oval(circ(x,y,rad),fill=col,outline=col)
trail=meter2pix([x,y])*TrailLength
ImTrail=canvas.create_line(trail,fill=col)
# .................................................... Initial Energy
en=ener(x0,y0,vx0,vy0)
QtLab[INITENER]['text']=QtLab[EULERENER]['text']=f'{en:.6e}'
# ...................................................................
nIter=0
tcount=0
nOrbits=0
Telaps=0.0
ypair=[y0,y0]
tt0=time.time()
# ......................................................... Main Loop
while RunAll:
  StartIter=time.time()
  # ............................................ Draw Euler Satellite
  canvas.coords(ImTrail,trail)
  canvas.coords(SatImg,circ(x,y,rad))
  canvas.update()
  # .......................................................... Motion
  if RunMotion:
    Telaps+=dt
    # ........................................ Euler-Cromer Algorithm
    x+=vx*dt
    y+=vy*dt
    ax,ay=accel(x,y)
    vx+=ax*dt
    vy+=ay*dt
    # ................................................. Update Trail
    if norm(np.array(meter2pix([x,y]))-np.array(trail[-2:]))>10:
      del trail[:2]
      trail.extend(meter2pix([x,y]))
    # ................................................. Update ypair
    ypair[0]=ypair[1]
    ypair[1]=y
    if ypair[0]<0 and ypair[1]>0:
      nOrbits+=1
      QtLab[ORBITS].config(text=str(nOrbits))
      OrbPeriod=Telaps/nOrbits
      QtLab[PERIOD].config(text=str(timedelta(seconds=int(OrbPeriod))))
    # ........................................ Show Iteration Counter
    nIter+=1
    if nIter%20==0:
      QtLab[ELAPSED].config(text=str(timedelta(seconds=int(Telaps))))
      QtLab[ITER].config(text=str(nIter))
      en=ener(x,y,vx,vy)
      QtLab[EULERENER]['text']=f'{en:.6e}'
  # ........................................... New tau and Time Step
  elif GetData:
    tauOld=tau
    try:
      dt=float(TimEntry[0].get())
    except ValueError:
      pass
    try:
      tau=int(TimEntry[1].get())
    except ValueError:
      pass
    TimEntry[0].delete(0,END)
    TimEntry[0].insert(0,f'{dt:.2f}')
    TimEntry[1].delete(0,END)
    TimEntry[1].insert(0,f'{tau:d}')
    # ...................................... Reset Position and Trail
    if tauOld==tau:
      x,vx,y,vy=x0,vx0,y0,vy0
      trail=meter2pix([x0,y0])*TrailLength
      ypair=[y0,y0]
      nOrbits=0
      Telaps=0.0
    GetData=FALSE
  # ................................................ Cycle Duration
  tcount+=1
  if tcount>=10:
    tcount=0
    ttt=time.time()
    elapsed=ttt-tt0
    QtLab[CYCLE]['text']=f'{elapsed*100:8.3f}'+' ms'
    tt0=ttt
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-ElapsIter)
#----------------------------------------------------------------------
root.destroy()
  
