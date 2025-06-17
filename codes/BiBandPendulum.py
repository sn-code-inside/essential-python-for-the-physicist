#!/usr/bin/env python3
#coding: utf8
import os
from numpy import *
from tkinter import *
from random import *
from scipy.integrate import odeint

global RunAll
global RunIter
global GetData
RunAll=True
RunIter=False
GetData=False

deg=180.0/pi

def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StartButton["text"]="Stop"
  else:
    StartButton["text"]="Restart"
    
def StopAll():
  global RunAll
  RunAll=False
  
def ReadData(*arg):
  global GetData
  GetData=True 
  
root=Tk()
root.title("Double Elastic Band Pendulum")
root.bind('<Return>',ReadData)
# ..................................................................... canvas
cw=800
ch=800
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ..................................................................... toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1, sticky=N)
# ..................................................................... buttons
StartButton=Button(toolbar,text="Start",command=StartStop,width=9)
StartButton.grid(row=0,column=0,sticky=W)

ReadButton=Button(toolbar, text="Read Data", command=ReadData,width=9)
ReadButton.grid(row=1,column=0,columnspan=2,sticky=W)

CloseButton=Button(toolbar, text="Exit", command=StopAll,width=9)
CloseButton.grid(row=2,column=0,sticky=W)
# ..................................................................... arrays
LabVar=[]
EntryVar=[]
LabPar=[]
EntryPar=[]
VarList=["x\u2081","vx\u2081","y\u2081","vy\u2081","x\u2082","vx\u2082",\
  "y\u2082","vy\u2082"]
nVar=len(VarList)
ParList=["L\u2081","Hooke\u2081","m\u2081","visc\u2081",\
  "L\u2082","Hooke\u2082","m\u2082","visc\u2082","G","Ox","Oy"]
nPar=len(ParList)
# ..................................................................... Entries
nr=3
for i in range(nVar):
  LabVar.append(Label(toolbar,text=str(VarList[i]),font=("Helvetica",12)))
  LabVar[i].grid(row=nr,column=0)
  EntryVar.append(Entry(toolbar,bd =5,width=8))
  EntryVar[i].grid(row=nr,column=1)
  nr+=1
for i in range(nPar):
  LabPar.append(Label(toolbar,text=str(ParList[i]),font=("Helvetica",12)))
  LabPar[i].grid(row=nr,column=0)
  EntryPar.append(Entry(toolbar,bd =5,width=8))
  EntryPar[i].grid(row=nr,column=1)
  nr+=1
# ........................................................... frame persistence
cycle_period=20 #milliseconds
# ...................................................................... Origin
Ox=cw/2
Oy=ch/2
prad=3
# ..................................................................... gravity
G=9.8
# .................................................................. pendulum 1
L1=150.0
Hooke1=10.0
rad1=12
m1=10.0
visc1=0.0
pColor1="red"
# .................................................................. pendulum 2
L2=170.0
Hooke2=10.0
rad2=12
m2=10.0
visc2=0.0
pColor2="blue"
#.............................................................. initial values
theta1=pi/2.0
theta2=0.25*pi
# ..................................................................
x1=Ox+L1*sin(theta1)
y1=Oy+L1*cos(theta1)
x2=x1+L2*sin(theta2)
y2=y1+L2*cos(theta2)
y=vx1=vy1=vx2=vy2=0.0
# ............................................................................
y=[x1,vx1,y1,vy1,x2,vx2,y2,vy2]
# ..................................................................... degrees
# .................................................................. parameters
params=[L1,Hooke1,m1,visc1,L2,Hooke2,m2,visc2,G,Ox,Oy]
# .......................................................... initialize entries
for i in range(nVar):
  buff="%.2f" % y[i]
  EntryVar[i].delete(0,'end')
  EntryVar[i].insert(0,buff)

for i in range(nPar):
  buff="%.2f" % params[i]
  EntryPar[i].delete(0,'end')
  EntryPar[i].insert(0,buff)
  
# .................................................................... function
def dydt(y, t, params):
  x1,vx1,y1,vy1,x2,vx2,y2,vy2=y                 # unpack current values of y
  L1,Hooke1,m1,visc1,L2,Hooke2,m2,visc2,G,Ox,Oy=params   # unpack parameters
  L1temp=sqrt((x1-Ox)**2+(y1-Oy)**2)
  L2temp=sqrt((x2-x1)**2+(y2-y1)**2)
  dL1=L1temp-L1
  dL2=L2temp-L2
  ctheta1=(y1-Oy)/L1temp
  stheta1=(x1-Ox)/L1temp
  ctheta2=(y2-y1)/L2temp
  stheta2=(x2-x1)/L2temp
  f1=0.0
  if dL1>0:
    f1=-dL1*Hooke1
  f2=0.0
  if dL2>0:
    f2=-dL2*Hooke2
  ax1=f1*stheta1-f2*stheta2-visc1*vx1
  ay1=f1*ctheta1-f2*ctheta2-m1*G-visc1*vy1
  ax2=f2*stheta2-visc2*vx2
  ay2=f2*ctheta2-m2*G-visc2*vy2
  derivs = [vx1,ax1,vy1,ay1,vx2,ax2,vy2,ay2] # list of dy/dt=f functions
  return derivs
# ..................................................... numerical time interval
t=[0.0,0.05]
while RunAll:
  # ...................................................... draw double pendulum
  canvas.delete(ALL)
  canvas.create_line(0,ch-Oy,cw,ch-Oy,fill="green")
  canvas.create_oval(Ox-prad,ch-(Oy+prad),Ox+prad,ch-(Oy-prad),fill="black")
  deltax1=x1-Ox
  deltay1=y1-Oy
  length1sq=deltax1**2+deltay1**2
  length1=sqrt(length1sq)
  if length1>=L1:
    canvas.create_line(Ox,ch-Oy,x1,ch-y1,fill="black")
  else:
    alpha=arcsin(length1/L1)
    beta=arctan2(deltay1,deltax1)
    gamma=(pi/2.0)+beta-alpha
    x3=Ox+0.5*L1*cos(gamma)
    y3=Oy+0.5*L1*sin(gamma)
    canvas.create_line(Ox,ch-Oy,x3,ch-y3,fill="black")
    canvas.create_line(x3,ch-y3,x1,ch-y1,fill="black")
  deltax2=x2-x1
  deltay2=y2-y1
  length2sq=deltax2**2+deltay2**2
  length2=sqrt(length2sq)
  if length2>=L1:
    canvas.create_line(x1,ch-y1,x2,ch-y2,fill="black")
  else:
    alpha=arcsin(length2/L2)
    beta=arctan2(deltay2,deltax2)
    gamma=(pi/2.0)+beta-alpha
    x3=x1+0.5*L2*cos(gamma)
    y3=y1+0.5*L2*sin(gamma)
    canvas.create_line(x1,ch-y1,x3,ch-y3,fill="black")
    canvas.create_line(x3,ch-y3,x2,ch-y2,fill="black")
  canvas.create_oval(x1-rad1,ch-(y1+rad1),x1+rad1,ch-(y1-rad1),fill=pColor1)
  canvas.create_oval(x2-rad2,ch-(y2+rad2),x2+rad2,ch-(y2-rad2),fill=pColor2)
  canvas.update()
  canvas.after(cycle_period)
  if RunIter:
    # .......................................................... next step
    psoln = odeint(dydt,y,t,args=(params,))
    x1=psoln[1,0]
    vx1=psoln[1,1]
    y1=psoln[1,2]
    vy1=psoln[1,3]
    x2=psoln[1,4]
    vx2=psoln[1,5]
    y2=psoln[1,6]
    vy2=psoln[1,7] 
    # ......................................................................
    y=[x1,vx1,y1,vy1,x2,vx2,y2,vy2]
  else:
    if GetData:
      for i in range(nVar):
        try:
          y[i]=float(EntryVar[i].get())
        except ValueError:
          pass
      for i in range(nPar):
        try:
          params[i]=float(EntryPar[i].get())
        except ValueError:
          pass
      x1,vx1,y1,vy1,x2,vx2,y2,vy2=y
      L1,Hooke1,m1,visc1,L2,Hooke2,m2,visc2,G,Ox,Oy=params
      for i in range(nVar):
        buff="%.2f" % y[i]
        EntryVar[i].delete(0,'end')
        EntryVar[i].insert(0,buff)
      for i in range(nPar):
        buff="%.2f" % params[i]
        EntryPar[i].delete(0,'end')
        EntryPar[i].insert(0,buff)
      GetData=False

  #----------------------------------------------------------------------------
root.destroy()
canvas.mainloop()
  