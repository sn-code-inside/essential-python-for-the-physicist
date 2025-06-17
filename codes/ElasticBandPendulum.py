#!/usr/bin/env python3
from tkinter import *
import numpy as np
import time
from scipy.integrate import odeint
# .................................................. Global variables
RunAll=True
GetData=RunIter=False
# ............................................. interaction functions
def StartStop():# ....... start/stop pendulum motion
  global RunIter
  RunIter=not RunIter
  if RunIter:
    StartButton['text']='Stop'
    ExitButton['state']=DISABLED
    for ep in EntryPar:
      ep['state']=DISABLED
  else:
    StartButton['text']='Restart'
    ExitButton['state']=NORMAL
    for ep in EntryPar:
      ep['state']=NORMAL
def ReadData(*args):# ................. read entries
  global GetData
  if not RunIter:
    GetData=True
def StopAll():# ....................... exit program
  global RunAll
  RunAll=False
# ....................................................... Canvas data
ButtWidth=9
cw=800
ch=640
Ox=cw/2
Oy=ch/2
# ............................................... Physical parameters
g=9.8           # m/s^2
L=4.0           # m
m=5.0           # kg
Hooke=500.0     # N/m
eta=0.0         # kg/s
dt=0.01         # s
# ................................................ Drawing parameters
prad=3          #  pivot radius
rad=12          #  bob radius
bColor='red'    #  bob color
# ..............................................................
scale=50.0      # pixels/m
tau=20          # milliseconds
# ..................................... Initial position and velocity
xx=1.1*L
vx=0.0
yy=0.0
vy=0.0
# .................................... variable and parameter vectors
params=[xx,vx,yy,vy,L,Hooke,m,eta,g,scale,dt,tau]
StartVal=params[0:4]
# .................................... derivatives-computing function
def dfdt(InputVal,t,params):
  xx,vx,yy,vy=InputVal                    # unpack initial conditions
  L,Hooke,m,eta,g,scale,dt,tau=params[4:]   # unpack parameters
  length=np.sqrt(xx**2+yy**2)
  stretch=length-L
  theta=np.arctan2(yy,xx)
  if stretch>0:
    force=-Hooke*stretch
  else:
    force=0.0
  fx=force*np.cos(theta)-eta*vx
  fy=force*np.sin(theta)-eta*vy
  ax=(fx/m)
  ay=(fy/m)-g
  return [vx,ax,vy,ay]
# ........................................... Create root window
root=Tk()
root.title('Elastic-Band Pendulum')
root.bind('<Return>',ReadData)
# ..................................... Add canvas to root window
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# ...................................... Add toolbar to root window
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ................................................... Toolbar buttons
nr=0
StartButton=Button(toolbar,text='Start',command=StartStop,\
  width=ButtWidth)
StartButton.grid(row=nr,column=0,sticky=W)
nr+=1
ExitButton=Button(toolbar,text='Exit',command=StopAll,\
  width=ButtWidth)
ExitButton.grid(row=nr,column=0,sticky=W)
nr+=1
# ............................................ Label and Entry arrays
LabPar=[]
EntryPar=[]
ParList=['x\u2080','vx\u2080','y\u2080','vy\u2080','Length',\
  'Hooke','Mass','\u03B7','g','scale','Time step','\u03C4/ms']
nPar=len(ParList)
# ........................................................... Entries
for i,ParName in enumerate(ParList):
  LabPar.append(Label(toolbar,text=str(ParName),\
    font=('Helvetica',12)))
  LabPar[i].grid(row=nr,column=0)
  EntryPar.append(Entry(toolbar,bd =5,width=ButtWidth))
  EntryPar[i].grid(row=nr,column=1)
  nr+=1
# ........................................................ time label
CycleLab0=Label(toolbar,text='Period:',font=('Helvetica',11))
CycleLab0.grid(row=nr,column=0)
CycleLab=Label(toolbar,text='     ',font=('Helvetica',11))
CycleLab.grid(row=nr,column=1,sticky=W)
nr+=1
# ................................................ Initialize entries
for i,ep in enumerate(EntryPar):
  ep.insert(0,'{:.3f}'.format(params[i]))
# ...................................................................
t=[0.0,dt]
tcount=0
tt0=time.time()
# ......................................................... Main loop
while RunAll:
  StartIter=time.time()
  # ................................................... Draw pendulum
  canvas.delete(ALL)
  canvas.create_oval(Ox-scale*L,ch-Oy+scale*L,\
    Ox+scale*L,ch-Oy-scale*L,outline='green',width=1)
  canvas.create_line(0,ch-Oy,cw,ch-Oy,fill='green')
  canvas.create_oval(Ox-prad,ch-(Oy+prad),Ox+prad,ch-(Oy-prad),\
    fill='black')
  lengthsq=xx**2+yy**2
  length=np.sqrt(lengthsq)
  if length>=L:
    canvas.create_line(Ox,ch-Oy,Ox+scale*xx,ch-Oy-scale*yy,\
      fill='black')
  else:
    alpha=np.arcsin(length/L)
    beta=np.arctan2(yy,xx)
    gamma=(np.pi/2.0)+beta-alpha
    xx2=0.5*L*np.cos(gamma)
    yy2=0.5*L*np.sin(gamma)
    canvas.create_line(Ox,ch-Oy,Ox+scale*xx2,ch-Oy-scale*yy2,\
      Ox+scale*xx,ch-Oy-scale*yy,fill='black')
  canvas.create_oval(Ox+scale*xx-rad,ch-Oy-scale*yy-rad,\
    Ox+scale*xx+rad,ch-Oy-scale*yy+rad,fill=bColor)
  canvas.update()
  if RunIter:
    # .......................... Velocity and position for next frame
    psoln=odeint(dfdt,StartVal,t,args=(params,))
    xx,vx,yy,vy=StartVal=psoln[1]
  # .................................................... Read entries
  elif GetData:
    for i,ep in enumerate(EntryPar):
      try:
        params[i]=float(ep.get())
      except ValueError:
        pass
    for i,ep in enumerate(EntryPar):
      ep.delete(0,END)
      ep.insert(0,'{:.3f}'.format(params[i]))
    xx,vx,yy,vy,L,Hooke,m,eta,g,scale,dt,tau=params
    StartVal=params[:4]
    tau=int(tau)
    t=[0.0,dt]
    GetData=False
  # .................................................. cycle duration
  tcount+=1
  if tcount%10==0:
    ttt=time.time()
    elapsed=ttt-tt0
    CycleLab['text']='%8.3f'%(elapsed*100.0)+' ms'
    tt0=ttt
  # .................................................................
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-ElapsIter)
  # .................................................................
root.destroy()
  
