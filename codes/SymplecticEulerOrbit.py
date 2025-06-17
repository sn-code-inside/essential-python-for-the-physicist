#!/usr/bin/env python3
from tkinter import *
from datetime import timedelta
import numpy as np
import time
# .................................................. Global variables
RunAll=True
GetCycle=GetStep=RunIter=False
# ................................................... Physical values
ME=5.9722e24          # Earth mass/kg
G=6.674e-11           # Gravitational constant [m^3/(kg s^2)]
GM=ME*G
dt=20.0              # s
# .................................. Drawing and Animation Parameters
cycle=5               # ms
scale=1.0e-5          # px/m
cw=600                # px
ch=500                # px
Ox=150                # px
Oy=ch/2.0             # px
rad=4                 # px
ms=1.0e3              #  satellite mass / kg
TrailLength=400
x0=4.0e7
vx0=0.0
y0=0.0
vy0=0.5*np.sqrt(GM/x0) # m/s
col='red'
# ...................................................................
INITENER,EULERENER,ITER,ELAPSED,ORBITS,PERIOD,CYCLE,SCALE=range(8)
quant=['Initial Energy','EulerEnergy','Iterations',\
  'Elapsed Time','Orbits','Orbital Period','Cycle','Scale']
# ............................................... Start/Stop function
def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StartButton['text']='Stop'
    CloseButton['state']=DISABLED
  else:
    StartButton['text']='Restart'
    CloseButton['state']=NORMAL
# ..................................................... Exit function
def StopAll():
  global RunAll
  RunAll=False
# ........................................................ Scale Down
def ScaleUpDown(event,ud):
  global scale
  fact=np.sqrt(2)
  if ud==-1:
    fact=1.0/fact
  scale*=fact
  QtLab[SCALE]['text']='{:10.3e}'.format(scale)
# ........................................................ Read Entry
def ReadData(event,tx):
  global GetStep,GetCycle
  if tx==0:
    GetStep=True
  elif tx==1:
    GetCycle=True
# ...................................................... acceleration  
def accel(x,y):
  r2=x**2+y**2
  aa=-GM/r2
  alpha=np.arctan2(y,x)
  ax=aa*np.cos(alpha)
  ay=aa*np.sin(alpha)
  return [ax,ay]
# ............................................................ energy
def ener(x,vx,y,vy):
  r=np.sqrt(x**2+y**2)
  pot=-GM*ms/r
  kin=0.5*ms*(vx**2+vy**2)
  return pot+kin
def TimeReversal():
  global dt
  dt=-dt
# ....................................................... root window
root=Tk()
root.title('Symplectic-Euler Satellite')
root.bind('<Control-plus>',lambda event,num=1:ScaleUpDown(None,num))
root.bind('<Control-minus>',lambda event,num=-1:ScaleUpDown(None,num))
# ............................................................ canvas
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# ........................................................... toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
toolbar.columnconfigure(1,minsize=120)
# ............................................................ buttons
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
tVal=[dt,cycle]
tfor=['{:.2f}','{:d}']
for i,tt in enumerate(TimeTxt):
  lb=Label(toolbar,text=tt,font=('Helvetica',11))
  lb.grid(row=nr,column=0)
  TimEntry.append(Entry(toolbar,bd=5,width=11))
  TimEntry[i].grid(row=nr,column=1)
  TimEntry[i].insert(0,tfor[i].format(tVal[i]))
  TimEntry[i].bind('<Return>',lambda event,num=i:ReadData(None,num))
  nr+=1
## ............................................................ Labels
QtLab=[]
for i,qt in enumerate(quant):
  lab=Label(toolbar,text=qt,font=('Helvetica',11))
  lab.grid(row=nr,column=0)
  QtLab.append(Label(toolbar,text='0',font=('Helvetica',11)))
  QtLab[i].grid(row=nr,column=1)
  nr+=1
QtLab[SCALE]['text']='{:10.3e}'.format(scale)
nr+=1
# ........................................... numerical time interval
tt0=time.time()
tcount=0
# .............................................. draw coordinate axes
canvas.create_line(0,Oy,cw,Oy,fill='black')
canvas.create_line(Ox,0,Ox,ch,fill='black')
canvas.create_oval(Ox-6,Oy-8,Ox+8,Oy+8,outline='#50a0ff',fill='#50a0ff')
# .................................................... Initial Values
x,vx,y,vy=x0,vx0,y0,vy0
# ................................................... Euler Satellite
ImEuler=canvas.create_oval(Ox+scale*x-rad,Oy-scale*y+rad,\
  Ox+scale*x+rad,Oy-scale*y-rad,fill=col,outline=col)
Trail=[x,y]*TrailLength
ScaledTrail=[Ox+scale*x,Oy-scale*y]*TrailLength
ImTrail=canvas.create_line(ScaledTrail,fill=col)
# .................................................... Initial Energy
en=ener(x0,vx0,y0,vy0)
QtLab[INITENER].config(text='{:.6e}'.format(en))
QtLab[EULERENER].config(text='{:.6e}'.format(en))
# ...................................................................
nIter=0
nOrbits=0
Telaps=0.0
ypair=[y0,y0]
# ...................................................................
while RunAll:
  StartIter=time.time()
  # ............................................ Draw Euler Satellite
  canvas.coords(ImEuler,Ox+scale*x-rad,Oy-scale*y+rad,\
    Ox+scale*x+rad,Oy-scale*y-rad)
  canvas.coords(ImTrail,ScaledTrail)
  # .......................................................... update
  canvas.update()
  # .......................................................... motion
  if RunIter:
    Telaps+=dt
    # ............................................... Euler Algorithm
    x+=vx*dt
    y+=vy*dt
    ax,ay=accel(x,y)
    vx+=ax*dt
    vy+=ay*dt
     # .......................................... update odeint trail
    if (abs(x-Trail[-2])+abs(y-Trail[-1]))>10/scale:
      del Trail[:2]
      Trail.append(x)
      Trail.append(y)
      ScaledTrail[::2]=[Ox+scale*zz for zz in Trail[::2]]
      ScaledTrail[1::2]=[Oy-scale*zz for zz in Trail[1::2]]
    # ................................................. update ypair
    ypair[0]=ypair[1]
    ypair[1]=y
    if ypair[0]<0 and ypair[1]>0:
      nOrbits+=1
      QtLab[ORBITS].config(text=str(nOrbits))
      OrbPeriod=Telaps/nOrbits
      QtLab[PERIOD].config(text=str(timedelta(seconds=int(OrbPeriod))))
    # ........................................ show iteration counter
    nIter+=1
    if nIter%20==0:
      QtLab[ELAPSED].config(text=str(timedelta(seconds=int(Telaps))))
      QtLab[ITER].config(text=str(nIter))
      en=ener(x,vx,y,vy)
      QtLab[EULERENER].config(text='{:.6e}'.format(en))
  # ................................................... New Time Step
  elif GetStep:
    try:
      dt=float(TimEntry[0].get())
    except ValueError:
      pass
    TimEntry[0].delete(0,END)
    TimEntry[0].insert(0,'{:.2f}'.format(dt))
    # ..................................... Resets Position and Trail
    x,vx,y,vy=x0,vx0,y0,vy0
    Trail=[x0,y0]*TrailLength
    ScaledTrail=[Ox+scale*x0,Oy-scale*y0]*TrailLength
    ypair=[y0,y0]
    nOrbits=0
    Telaps=0.0
    GetStep=FALSE
  elif GetCycle:
    try:
      cycle=int(TimEntry[1].get())
    except ValueError:
      pass
    TimEntry[1].delete(0,END)
    TimEntry[1].insert(0,'{:d}'.format(cycle))
    GetCycle=FALSE
  # ................................................ cycle duration
  tcount+=1
  if tcount>=10:
    tcount=0
    ttt=time.time()
    elapsed=ttt-tt0
    QtLab[CYCLE]['text']='%8.3f'%(elapsed*100.0)+' ms'
    tt0=ttt
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(cycle-ElapsIter)
#----------------------------------------------------------------------
root.destroy()
  
