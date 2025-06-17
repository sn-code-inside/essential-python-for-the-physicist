#!/usr/bin/env python3
from tkinter import *
import numpy as np
import time
from scipy.integrate import odeint
from scipy.optimize import fsolve
from numpy.linalg import norm
# .................................................. Global Variables
RunAll=True
GetData=Grabbed=RunMotion=False
# ....................................................... Canvas Data
ButtWidth=9
cw,ch=800,640
Ox,Oy=cw//2,ch//2
# ............................................... Physical Parameters
g=9.8           # m/s**2
L=4.0           # m
m=5.0           # kg
k=500.0         # N/m
eta=0.0         # kg/s
dt=0.01         # s
# ........................................................... Display
prad=3          #  pivot radius
rad=12          #  bob radius
bColor='red'    #  bob color
scale=50.0      # pixels/m
tau=20          # milliseconds
TrailLength=400
# ..................................... Initial position and velocity
state=[1.1*L,0.0,0.0,0.0]  #   [x0,y0,vx0,vy0]
trail=[Ox+scale*1.1*L,Oy]*TrailLength
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
    dist=np.array(meter2pix(state[:2]))-np.array([event.x,event.y])
    Grabbed=norm(dist)<rad
# ......................................................... Drag ball
def DragBall(event):
  global Grabbed,Ox,Oy,rad,scale,state
  if Grabbed:
    state[0]=(np.clip(event.x,rad,cw-rad)-Ox)/scale
    state[1]=(Oy-np.clip(event.y,rad,ch-rad))/scale
# ...................................................... Release ball
def ReleaseBall(event):
  global Grabbed,Lab,state,trail
  state[2:]=[0.0,0.0]
  trail=meter2pix(state[:2])*TrailLength
  en=ener(state)
  Lab[ENER0]['text']=Lab[ENER1]['text']=f'{en:.8e}'
  Grabbed=False
# ......................................................... meter2pix
def meter2pix(pos):
  global Ox,Oy,scale
  CanvPos=[]
  for i,xy in enumerate(pos):
    CanvPos.append(Ox+scale*xy if i%2==0 else Oy-scale*xy)
  return CanvPos
# .............................................................. circ
def circ(pos):
  global rad
  cx,cy=meter2pix(pos)
  return [cx+rad,cy+rad,cx-rad,cy-rad]
# ........................................................... CateFun
def CateFun(x,CatePar):
  L,cx,cy=CatePar
  rr=np.sqrt(L**2-cy**2)/cx
  return rr-np.sinh(x)/x
# .......................................................... catenary
def catenary(pos):
  global L,scale
  r=norm(pos)
  band=[Ox,Oy]
  if r<L:
    if abs(pos[0]*scale)<4:
      band.extend(meter2pix([0.5*pos[0],0.5*(pos[1]-L)]))
    else:
      absx=abs(pos[0])
      CatePar=[L,absx,pos[1]]
      AA0=0.01
      AA=fsolve(CateFun,AA0,CatePar)[0]
      aa=0.5*absx/AA
      bb=0.5*absx-aa*np.arctanh(pos[1]/L)
      cc=0.5*(pos[1]-L/np.tanh(AA))
      for i in range(1,20):
        x1=pos[0]*i/20.0
        band.extend(meter2pix([x1,aa*np.cosh((abs(x1)-bb)/aa)+cc]))
  band.extend(meter2pix(pos))
  return band
# ............................................................ Energy
def ener(state):
  pot=m*g*state[1]
  r=norm(state[:2])
  if r>L:
    pot+=0.5*k*(r-L)**2
  return pot+0.5*m*np.dot(state[2:],state[2:])
# .................................... Derivatives-Computing Function
def dfdt(state,t):
  global eta,g,k,L,m
  theta=np.arctan2(state[1],state[0])
  r=norm(state[:2])
  stretch=r-L
  force=-k*stretch if stretch>0 else 0.0
  fx=force*np.cos(theta)-eta*state[2]
  fy=force*np.sin(theta)-eta*state[3]
  ax=(fx/m)
  ay=(fy/m)-g
  return [state[2],state[3],ax,ay]
# ................................................ Create Root window
root=Tk()
root.title('Catenary Pendulum')
root.bind('<Return>',ReadData)
# ......................................... Add canvas to root window
canvas=Canvas(root,width=cw,height=ch,background='#ffffff')
canvas.grid(row=0,column=0)
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
VarLab=['x\u2080 (m)','y\u2080 (m)','vx\u2080 (m/s)','vy\u2080 (m/s)',\
  'Length (m)','k (N/m)','Mass (kg)','\u03B7 (Ns/m)','scale (px/m)',\
    'Time step (s)','\u03C4 (ms)']
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
circle=canvas.create_oval(meter2pix([-L,L,L,-L]),outline='green')
canvas.create_line(0,ch-Oy,cw,ch-Oy,fill='green')
# ..................................................... Draw Pendulum
canvas.create_oval(Ox-prad,Oy-prad,Ox+prad,Oy+prad,fill='black')
BandImg=canvas.create_line([Ox,Oy]+meter2pix(state[:2]),fill='black')
BobImg=canvas.create_oval(circ(state[:2]),fill=bColor)
TrailImg=canvas.create_line(trail,fill=bColor)
# ...................................................................
t=[0.0,dt]
tcount=0
nIter=0
tt0=time.time()
en=ener(state)
Lab[ENER0]['text']=Lab[ENER1]['text']=f'{en:.8e}'
# ......................................................... Main loop
while RunAll:
  StartIter=time.time()
  # ................................................... Draw pendulum
  canvas.coords(BandImg,catenary(state[:2]))
  canvas.coords(TrailImg,trail)
  canvas.coords(BobImg,circ(state[:2]))
  canvas.update()
  if RunMotion:
    nIter+=1
    # .......................... Velocity and position for next frame
    psoln=odeint(dfdt,state,t)
    state=psoln[1]
    if nIter%20==0:
      en=ener(state)
      Lab[ENER1]['text']=f'{en:.8e}'
      Lab[ITER]['text']=f'{nIter:d}'
    # .................................................. Update Trail
    xx,yy=meter2pix(state[:2])
    if norm(np.array([xx,yy])-np.array(trail[-2:]))>10:
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
    Lab[ENER0]['text']=Lab[ENER1]['text']=f'{en:.8e}'
    trail=meter2pix(state[:2])*TrailLength
    canvas.coords(circle,meter2pix([-L,L,L,-L]))
    GetData=False
  # .................................................. Cycle Duration
  tcount+=1
  if tcount%20==0:
    ttt=time.time()
    Lab[PERIOD]['text']=f'{(ttt-tt0)*50.0:8.3}'+' ms'
    tt0=ttt
  # .................................................................
  ElapsIter=int((time.time()-StartIter)*1000.0)
  canvas.after(tau-ElapsIter)
  #------------------------------------------------------------------
root.destroy()
  
