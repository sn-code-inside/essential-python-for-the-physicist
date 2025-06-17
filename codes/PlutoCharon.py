#!/usr/bin/env python3
import numpy as np
import time
from tkinter import *
from scipy.integrate import odeint
# ......................................................... Constants
RunAll=True
RunMotion=False
cw=ch=800
Ox=Oy=cw/2
scale=2e-5            # px/m
G=6.67408e-11         # Gravitational Constant (m^3 kg^-1 s^-2)
# .................................................... Time constants
t=[0,600]             # s
tau=20                # ms
# ............................................................. Pluto
m1=1.3e22             # kg
x1=y1=0
vx1=vy1=0
rad1=10               # px
# ............................................................ Charon
m2=1.6e21             # kg
x2=1.9e7              # m
y2=0
vx2=0
vy2=2e2               # m/s
rad2=5                # px
# ......................................... Move to Barycenter System
mtot=m1+m2
xb=(m1*x1+m2*x2)/mtot
yb=(m1*y1+m2*y2)/mtot
vxb=0
vyb=(m1*vy1+m2*vy2)/mtot
x1-=xb
y1-=yb
x2-=xb
y2-=yb
vx1-=vxb
vy1-=vyb
vx2-=vxb
vy2-=vyb
# ..................................................... Initial State
state=[x1,y1,x2,y2,vx1,vy1,vx2,vy2]
# ......................................................... StartStop
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  StartButton['text']='Stop' if RunMotion else 'Restart'
  CloseButton['state']=DISABLED if RunMotion else NORMAL
# ........................................................... StopAll
def StopAll():
  global RunAll
  RunAll=False
# ............................................................. circ
def circ(x,y,r):
  global Ox,Oy,scale
  xx=scale*x
  yy=scale*y
  return [Ox+xx-r,Oy-yy-r,Ox+xx+r,Oy-yy+r]
# .............................................................. dfdt
def dfdt(state,t):
  global G
  x1,y1,x2,y2,vx1,vy1,vx2,vy2=state
  distx=x2-x1
  disty=y2-y1
  r2=distx**2+disty**2
  alpha=np.arctan2(disty,distx)
  f=G/r2
  fx=f*np.cos(alpha)
  fy=f*np.sin(alpha)
  ax1=fx*m2
  ay1=fy*m2
  ax2=-fx*m1
  ay2=-fy*m1
  return [vx1,vy1,vx2,vy2,ax1,ay1,ax2,ay2]
# ...................................................................
root=Tk()
root.title('Pluto-Charon system')
canvas=Canvas(root,width=cw,height=ch,background='white')
canvas.grid(row=0,column=0)
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ............................................ add buttons to toolbar
bwidth=10
StartButton=Button(toolbar,text='Start',command=StartStop,width=bwidth)
StartButton.grid(row=0,column=0)
CloseButton=Button(toolbar,text='Exit',command=StopAll,width=bwidth)
CloseButton.grid(row=1,column=0)
# ........................................................
canvas.create_line(0,Oy,cw,Oy,fill='black')
canvas.create_line(Ox,0,Ox,ch,fill='black')
Pluto=canvas.create_oval(circ(x1,y1,rad1),fill='blue')
Charon=canvas.create_oval(circ(x2,y2,rad2),fill='red')
# .................................................... Animation Loop
while RunAll:
  StartIter=time.time()
  # ................................................... Update Bodies
  canvas.coords(Pluto,circ(state[0],state[1],rad1))
  canvas.coords(Charon,circ(state[2],state[3],rad2))
  canvas.update()
  # ................................................... Update Motion
  if RunMotion:
    psoln=odeint(dfdt,state,t)
    state=psoln[1,:]
  # ......................................... Control Animation Speed
  ElapsTime=int((time.time()-StartIter)*1000)
  canvas.after(tau-ElapsTime)
root.destroy()











