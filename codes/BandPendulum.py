#!/usr/bin/env python3
import numpy as np
import time
from tkinter import *
from scipy.integrate import odeint
# .................................................. Global variables
RunAll=True
GetData=RunMotion=False
# ....................................................... Canvas data
ButtWidth=9
cw=800
ch=580
Ox=cw/2
Oy=ch/2
# ............................................... Physical parameters
g=9.8           # m/s^2
L=4.0           # m
m=5.0           # kg
k=500.0         # N/m
eta=0.0         # kg/s
dt=0.01         # s
# ................................................................
prad=3          #  px  pivot radius
rad=12          #  px  bob radius
bColor='blue'   #  bob color
# ..............................................................
scale=50.0      # px/m
tau=20          # milliseconds
TrailLength=400
# ........................................................ Start/Stop
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  StartButton['text']='Stop' if RunMotion else 'Restart'
  for ee in [ExitButton]+VarEntry:
    ee['state']=DISABLED if RunMotion else NORMAL
# ...................................................... Exit Program
def StopAll():
  global RunAll
  RunAll=False
# ...................................................... Read Entries
def ReadData(*args):
  global GetData
  GetData=True
# ......................................................... Grab ball
def GrabBall(event):
  global Grabbed,rad,RunMotion,state
  if not RunMotion:
    xx,yy=meter2pix(state[:2])
    Grabbed=((xx-event.x)**2+(yy-event.y)**2)<rad**2
# ......................................................... Drag ball
def DragBall(event):
  global Grabbed,Ox,Oy,rad,scale,state
  if Grabbed:
    state[0]=(np.clip(event.x,rad,cw-rad)-Ox)/scale
    state[1]=(Oy-np.clip(event.y,rad,ch-rad))/scale
# ...................................................... Release ball
def ReleaseBall(event):
  global Grabbed,Ox,Oy,state,scale,ScaledTrail,trail,TrailLength
  if Grabbed:
    state[2:]=[0.0,0.0]
    trail=meter2pix(state[:2])*TrailLength
    en=ener(state)
    Lab[ENER0].config(text=f'{en:.8e}')
    Lab[ENER1].config(text=f'{en:.8e}')
    Grabbed=False
# ................................................ Canvas Coordinates
def meter2pix(pos):
  global Ox,Oy,scale
  CanvPos=[]
  for i,xy in enumerate(pos):
    CanvPos.append(Ox+scale*xy if i%2==0 else Oy-scale*xy)
  return CanvPos
# ................................................ Circle Coordinates
def circ(pos,radius):
  global Ox,Oy,scale
  xx,yy=meter2pix(pos)
  rr=radius*scale
  return [xx-radius,yy-radius,xx+radius,yy+radius]
# ............................................................ Energy
def ener(state):
  global g,k,L,m
  pot=m*g*state[1]
  r=np.linalg.norm(state[:2])
  if r>L:
    pot+=0.5*k*(r-L)**2
  return pot+0.5*m*np.dot(state[2:],state[2:])
# .................................... derivatives-computing function
def dfdt(state,t):
  global eta,g,k,L,m
  theta=np.arctan2(state[1],state[0])
  r=np.linalg.norm(state[:2])
  stretch=r-L
  if stretch>0:
    force=-k*stretch
  else:
    force=0.0
  fx=force*np.cos(theta)-eta*state[2]
  fy=force*np.sin(theta)-eta*state[3]
  ax=(fx/m)
  ay=(fy/m)-g
  derivs=[state[2],state[3],ax,ay]
  return derivs
# ..................................... Initial position and velocity
state=[1.1*L,0.0,0.0,0.0]
trail=meter2pix(state[:2])*TrailLength
# ................................................ Create root window
root=Tk()
root.title('Elastic-Band Pendulum')
root.bind('<Return>',ReadData)
# ......................................... Add canvas to root window
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
# ...................................................... Mouse button
canvas.bind('<Button-1>',GrabBall)
canvas.bind('<B1-Motion>',DragBall)
canvas.bind('<ButtonRelease-1>',ReleaseBall)
# ........................................ Add toolbar to root window
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
toolbar.option_add('*Font','Helvetica 11')
# ................................................... Toolbar buttons
nr=0
StartButton=Button(toolbar,text='Start',command=StartStop,\
  width=ButtWidth)
StartButton.grid(row=nr,column=0,sticky=W)
nr+=1
ExitButton=Button(toolbar,text='Exit',command=StopAll,width=ButtWidth)
ExitButton.grid(row=nr,column=0,sticky=W)
nr+=1
# ............................................ Label and Entry arrays
VarLab=['x\u2080','y\u2080','vx\u2080','vy\u2080','Length','k',\
  'Mass','\u03B7','scale','Time step','\u03C4/ms']
inputs=state+[L,k,m,eta,scale,dt,tau]
VarEntry=[]
for i,lab in enumerate(VarLab):
  Label(toolbar,text=str(lab)).grid(row=nr,column=0)
  VarEntry.append(Entry(toolbar,bd=5,width=ButtWidth))
  VarEntry[i].grid(row=nr,column=1)
  VarEntry[i].insert(0,f'{inputs[i]:.3f}')
  nr+=1
# ............................................................ Labels
LabList=['Period','Initial Energy','Energy','Iterations']
PERIOD,ENER0,ENER1,ITER=range(4)
Lab=[]
for i,ll in enumerate(LabList):
  Label(toolbar,text=ll,).grid(row=nr,column=0)
  Lab.append(Label(toolbar,text='     '))
  Lab[i].grid(row=nr,column=1,sticky=W)
  nr+=1
# ................................... Draw Circle and Horizontal Line
circle=canvas.create_oval(circ([0,0],L*scale),outline='green')
canvas.create_line(0,Oy,cw,Oy,fill='green')
# ..................................................... Draw Pendulum
canvas.create_oval(circ([0,0],prad),fill='black')
BandImg=canvas.create_line(Ox,Oy,meter2pix(state[:2]),fill='red')
BobImg=canvas.create_oval(circ(state[:2],rad),fill=bColor)
TrailImg=canvas.create_line(trail,fill=bColor)
# ...................................................................
t=[0.0,dt]
tcount=0
nIter=0
tt0=time.time()
en=ener(state)
Lab[ENER0].config(text=f'{en:.8e}')
Lab[ENER1].config(text=f'{en:.8e}')
# ......................................................... Main loop
while RunAll:
  StartIter=time.time()
  # ................................................... Draw pendulum
  canvas.coords(BandImg,Ox,Oy,meter2pix(state[:2]))
  r=np.linalg.norm(state[:2])
  if r>L:
    canvas.itemconfigure(BandImg,fill='red')
  else:
    canvas.itemconfigure(BandImg,fill='black')
  canvas.coords(BobImg,circ(state[:2],rad))
  canvas.coords(TrailImg,trail)
  canvas.update()
  if RunMotion:
    nIter+=1
    # .......................... Velocity and position for next frame
    psoln=odeint(dfdt,state,t)
    state=psoln[1]
    if nIter%20==0:
      en=ener(state)
      Lab[ENER1].config(text=f'{en:.8e}')
      Lab[ITER].config(text='f{nIter:d}')
    # .................................................. Update Trail
    xx,yy=meter2pix(state[:2])
    if np.linalg.norm([xx-trail[-2],yy-trail[-1]])>10:
      trail=trail[2:]
      trail.extend([xx,yy])
  # .................................................... Read Entries
  elif GetData:
    for i,ve in enumerate(VarEntry):
      try:
        inputs[i]=float(ve.get())
      except ValueError:
        pass
      ve.delete(0,END)
      ve.insert(0,f'{inputs[i]:.3f}')
    state=inputs[:4]
    L,k,m,eta,scale,dt,tau=inputs[4:]
    tau=int(tau)
    t=[0.0,dt]
    en=ener(state)
    Lab[ENER0].config(text=f'{en:.8e}')
    Lab[ENER1].config(text=f'{en:.8e}')
    trail=meter2pix(state[:2])*TrailLength
    canvas.coords(circle,circ([0,0],L*scale))
    GetData=False  
  # .................................................. Cycle Duration
  tcount+=1
  if tcount%20==0:
    ttt=time.time()
    elapsed=ttt-tt0
    Lab[PERIOD]['text']='%8.3f'%(elapsed*50.0)+' ms'
    tt0=ttt
  # .................................................................
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-ElapsIter)
  #------------------------------------------------------------------
root.destroy()
