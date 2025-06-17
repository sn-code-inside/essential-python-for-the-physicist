#!/usr/bin/env python3
import numpy as np
from tkinter import *
# .................................................. Global variables
RunAll=True
GetData=RunMotion=False
ButtWidth=9
# ...................................................................
cycle=20 #milliseconds
# ........................................................ Parameters
cw=ch=800
Ox=Oy=cw/2
rad=12
OrbitRad=350
# ............................. Initial Position and Angular Velocity
x=350.0
y=0.0
alpha=0
omega=0.01
# ......................................................... StartStop
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  StartButton['text']='Stop' if RunMotion else 'Restart'
  EntryRad['state']=DISABLED if RunMotion else NORMAL
  EntryOmega['state']=DISABLED if RunMotion else NORMAL
# .......................................................... ReadData
def ReadData(*arg):
  global GetData
  GetData=True
# ........................................................... StopAll   
def StopAll():
  global RunAll
  RunAll=False
# ................................................ Create Root Window
root=Tk()
root.title('Circular Orbit')
root.bind('<Return>',ReadData)
# ..................................................... Create Canvas
canvas=Canvas(root,width=cw,height=ch,background='white')
canvas.grid(row=0,column=0)
canvas.update()
# .................................................... Create Toolbar
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ....................................................... Add Buttons
nr=1
StartButton=Button(toolbar,text='Start',command=StartStop,\
  width=ButtWidth)
StartButton.grid(row=nr,column=0,sticky=W)
nr+=1
CloseButton=Button(toolbar,text='Exit',command=StopAll,width=ButtWidth)
CloseButton.grid(row=nr,column=0,sticky=W)
nr+=1
# ....................................................... Add Entries
Label(toolbar,text='Orbit radius').grid(row=nr,column=0)
EntryRad=Entry(toolbar,bd=5,width=8)
EntryRad.grid(row=nr,column=1)
nr+=1
Label(toolbar,text='Angular velocity').grid(row=nr,column=0)
EntryOmega=Entry(toolbar,bd=5,width=8)
EntryOmega.grid(row=nr,column=1)
nr+=1
EntryRad.insert(0,f'{OrbitRad:.1f}')
EntryOmega.insert(0,f'{omega:.4f}')
# .................................................... Animation Loop
while RunAll:
  # ....................................................... Draw Body
  canvas.delete(ALL)
  canvas.create_line(0,ch-Oy,cw,ch-Oy,fill='green')
  canvas.create_line(Ox,ch,Ox,0,fill='green')
  canvas.create_oval(Ox+x-rad,Oy-(y+rad),Ox+x+rad,Oy-(y-rad),fill='red')
  canvas.update()
  if RunMotion:
    # ..................................................... Move Body
    alpha+=omega
    x=OrbitRad*np.cos(alpha)
    y=OrbitRad*np.sin(alpha)
    # .................................................. Read Entries
  elif GetData:
    try:
      OrbitRad=float(EntryRad.get())
    except ValueError:
      pass
    try:
      omega=float(EntryOmega.get())
    except ValueError:
      pass
    EntryRad.delete(0,'end')
    EntryRad.insert(0,f'{OrbitRad:.1f}')
    EntryOmega.delete(0,'end')
    EntryOmega.insert(0,f'{omega:.4f}')
    x=OrbitRad*np.cos(alpha)
    y=OrbitRad*np.sin(alpha)
    GetData=False
  # .............................................................
  canvas.after(cycle)
  #----------------------------------------------------------------------------
root.destroy()
  
