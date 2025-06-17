#!/usr/bin/env python3
#coding: utf8
import os
from numpy import *
from tkinter import *
from random import *
from scipy.integrate import odeint
# ................................................. global variables
RunAll=True
ChangeEntries=GetData=Grabbed1=Grabbed2=False
MouseChange=Relax=RunIter=False
# .......................................... radian/degree conversion
deg=180.0/pi
ButtWidth=9
# ................................................. start/stop motion
def StartStop():
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StartButton["text"]="Stop"
  else:
    StartButton["text"]="Restart"
# ...................................................... stop program
def StopAll():
  global RunAll
  RunAll=False
# ............................................ read data from entries
def ReadData(*arg):
  global GetData
  GetData=True
# .................................... relax lengths of pendulum rods
def RelaxLength():
  global Relax
  Relax=True
# ........................................ grab pendulum with mouse
def grab_disk(event):
  global Grabbed1,Grabbed2,Ox,Oy,x1,x2,y1,y2
  Grabbed1=((Ox+x1-event.x)**2+(Oy-y1-event.y)**2)<100
  if not Grabbed1:
    Grabbed2=((Ox+x2-event.x)**2+(Oy-y2-event.y)**2)<100
# ............................................ free grabbed pendulum
def free_disk(event):
  global Grabbed1,Grabbed2,MouseChange
  if Grabbed1:
    y[0]=float(x1)
    y[2]=float(y1)
    MouseChange=True
  elif Grabbed2:
    y[4]=float(x2)
    y[6]=float(y2)
    MouseChange=True
  Grabbed1=Grabbed2=False
# ............................................. move grabbed pendulum
def drag_disk(event):
  global Grabbed1,Grabbed2,x1,x2,y1,y2
  if Grabbed1:
    x1,y1=event.x-Ox,Oy-event.y
  elif Grabbed2:
    x2,y2=event.x-Ox,Oy-event.y
# .........................................................................
root=Tk()
root.title("Double Elastic Band Pendulum (Mouse)")
root.bind('<Return>',ReadData)
# ..................................................................... canvas
cw=800
ch=800
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ............................................................... mouse buttons
canvas.bind("<Button-1>",grab_disk)
canvas.bind("<B1-Motion>",drag_disk)
canvas.bind("<ButtonRelease-1>",free_disk)
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
LengthButton=Button(toolbar, text="Relax Lengths",command=RelaxLength,\
  width=ButtWidth)
LengthButton.grid(row=nr,column=0,columnspan=2,sticky=W)
nr+=1
CloseButton=Button(toolbar, text="Exit", command=StopAll,width=ButtWidth)
CloseButton.grid(row=nr,column=0,sticky=W)
nr+=1
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
for i in range(len(VarList)):
  LabVar.append(Label(toolbar,text=str(VarList[i]),font=("Helvetica",12)))
  LabVar[i].grid(row=nr,column=0)
  EntryVar.append(Entry(toolbar,bd =5,width=ButtWidth))
  EntryVar[i].grid(row=nr,column=1)
  nr+=1
for i in range(len(ParList)):
  LabPar.append(Label(toolbar,text=str(ParList[i]),font=("Helvetica",12)))
  LabPar[i].grid(row=nr,column=0)
  EntryPar.append(Entry(toolbar,bd =5,width=ButtWidth))
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
# ........................................................... impact parameter
impact2=(rad1+rad2)**2
DeltaM=m1-m2
Mtot=m1+m2
#.............................................................. initial values
theta1=pi/2.0
theta2=0.75*pi
# ..................................................................
x1=L1*sin(theta1)
y1=L1*cos(theta1)
x2=x1+L2*sin(theta2)
y2=y1-L2*cos(theta2)
vx1=vy1=vx2=vy2=0.0
# ............................................................................
y=[x1,vx1,y1,vy1,x2,vx2,y2,vy2]
# .................................................................. parameters
params=[L1,Hooke1,m1,visc1,L2,Hooke2,m2,visc2,G,Ox,Oy]
# .......................................................... initialize entries
for i in range(len(VarList)):
  EntryVar[i].insert(0,str(y[i]))
for i in range(len(ParList)):
  EntryPar[i].insert(0,str(params[i]))
# .................................................................... function
def dydt(y, t, params):
  x1,vx1,y1,vy1,x2,vx2,y2,vy2=y                # unpack current values of y
  L1,Hooke1,m1,visc1,L2,Hooke2,m2,visc2,G,Ox,Oy=params  # unpack parameters
  L1temp=sqrt(x1**2+y1**2)
  L2temp=sqrt((x2-x1)**2+(y2-y1)**2)
  dL1=L1temp-L1
  dL2=L2temp-L2
  ctheta1=y1/L1temp
  stheta1=x1/L1temp
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
  canvas.create_line(0,Oy,cw,Oy,fill="green")
  canvas.create_oval(Ox-prad,Oy-prad,Ox+prad,Oy+prad,fill="black")
  canvas.create_line(Ox,Oy,Ox+x1,Oy-y1,fill="black")
  canvas.create_line(Ox+x1,Oy-y1,Ox+x2,Oy-y2,fill="black")
  canvas.create_oval(Ox+x1-rad1,Oy-y1-rad1,Ox+x1+rad1,Oy-y1+rad1,fill=pColor1)
  canvas.create_oval(Ox+x1-L1,Oy-y1-L1,Ox+x1+L1,Oy-y1+L1,outline=pColor1,width=1)
  canvas.create_oval(Ox+x2-rad2,Oy-y2-rad2,Ox+x2+rad2,Oy-y2+rad2,fill=pColor2)
  canvas.create_oval(Ox+x2-L2,Oy-y2-L2,Ox+x2+L2,Oy-y2+L2,outline=pColor2,width=1)
  canvas.update()
  canvas.after(cycle_period)
  if RunIter:
    # .............................................................. collision?
    if ((x1-x2)**2+(y1-y2)**2)<=impact2:
      deltax=x1-x2
      deltay=y1-y2
      alpha=arctan2(deltay,deltax)
      csalpha=cos(alpha)
      snalpha=sin(alpha)
      vXI1=vx1*csalpha+vy1*snalpha
      vETA1=-vx1*snalpha+vy1*csalpha
      vXI2=vx2*csalpha+vy2*snalpha
      vETA2=-vx2*snalpha+vy2*csalpha
      NewvXI1=(DeltaM*vXI1+2.0*m2*vXI2)/Mtot
      NewvXI2=(2.0*m1*vXI1-DeltaM*vXI2)/Mtot
      vx1=NewvXI1*csalpha-vETA1*snalpha
      vy1=NewvXI1*snalpha+vETA1*csalpha
      vx2=NewvXI2*csalpha-vETA2*snalpha
      vy2=NewvXI2*snalpha+vETA2*csalpha
      y=[x1,vx1,y1,vy1,x2,vx2,y2,vy2]
    # ............................................................... next step
    psoln = odeint(dydt,y,t,args=(params,))
    x1=psoln[1,0]
    vx1=psoln[1,1]
    y1=psoln[1,2]
    vy1=psoln[1,3]
    x2=psoln[1,4]
    vx2=psoln[1,5]
    y2=psoln[1,6]
    vy2=psoln[1,7] 
    # .........................................................................
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
      ChangeEntries=True
      GetData=False
    if MouseChange:
      ChangeEntries=True
      MouseChange=False
    if Relax:
      L1=sqrt((x1-Ox)**2+(y1-Ox)**2)
      L2=sqrt((x2-x1)**2+(y2-y1)**2)
      params=[L1,Hooke1,m1,visc1,L2,Hooke2,m2,visc2,G,Ox,Oy]
      ChangeEntries=True
      Relax=False
    if ChangeEntries:
      for i in range(len(VarList)):
        buff="%.2f" % y[i]
        EntryVar[i].delete(0,'end')
        EntryVar[i].insert(0,buff)
      for i in range(len(ParList)):
        buff="%.2f" % params[i]
        EntryPar[i].delete(0,'end')
        EntryPar[i].insert(0,buff)
      ChangeEntries=False
  #----------------------------------------------------------------------------
root.destroy()
root.mainloop()
  