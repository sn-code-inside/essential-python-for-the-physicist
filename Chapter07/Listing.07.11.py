#!/usr/bin/env python3
from tkinter import *
import numpy as np
# .................................................. Global variables
RunAll=True
RunMotion=GetData=Grabbed=False
# ......................................................... Variables
cw=600
ch=400
delay=20 #milliseconds
rad=20
color='red'
x=rad
y=ch-rad
vx=4.0
vy=-7.5
ay=0.1
alpha=30*np.pi/180
sinalpha=np.sin(alpha)
cosalpha=np.cos(alpha)
tanalpha=np.tan(alpha)
triangle=[cw,0,cw,ch,cw-ch*tanalpha,ch]
k=cw-rad/cosalpha
# ................................................. Start/Stop motion
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  if RunMotion:
    StartButton['text']='Stop'
    CloseButton['state']=DISABLED
    EntryVx['state']=DISABLED
    EntryAccel['state']=DISABLED
  else:
    StartButton['text']='Restart'
    CloseButton['state']=NORMAL
    EntryVx['state']=NORMAL
    EntryAccel['state']=NORMAL
# ...................................................... Exit program
def StopAll():
  global RunAll
  RunAll=False
# ...................................................... Read entries
def ReadData(*arg):
  global GetData
  GetData=True
# ......................................................... Grab ball
def GrabBall(event):
  global Grabbed,rad,RunMotion,x,y
  if not RunMotion:
    Grabbed=((x-event.x)**2+(y-event.y)**2)<rad**2
# ...................................................... Release ball
def ReleaseBall(event):
  global Grabbed
  Grabbed=False
# ......................................................... Drag ball
def DragBall(event):
  global Grabbed,tanalpha,x,y
  if Grabbed:
    right=k-event.y*tanalpha
    x,y=np.clip(event.x,rad,right),np.clip(event.y,rad,ch-rad)
# ................................................ Create root window
root=Tk()
root.title('Leaning Wall')
root.bind('<Return>',ReadData)
# ......................................... Add canvas to root window
canvas=Canvas(root, width=cw, height=ch, background='white')
canvas.grid(row=0,column=0)
# ...................................................... Mouse button
canvas.bind('<Button-1>',GrabBall)
canvas.bind('<B1-Motion>',DragBall)
canvas.bind('<ButtonRelease-1>',ReleaseBall)
# ........................................ Add toolbar to root window
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ................................................... Toolbar buttons
StartButton=Button(toolbar,text='Start',command=StartStop,width=7)
StartButton.grid(row=0,column=0)
CloseButton=Button(toolbar, text='Close', command=StopAll)
CloseButton.grid(row=0,column=1)
# ........................................ Toolbar labels and entries
LabVx=Label(toolbar,text='Vx')
LabVx.grid(row=1,column=0)
EntryVx=Entry(toolbar,bd=5,width=8)
EntryVx.grid(row=1,column=1)
LabAccel=Label(toolbar,text='Ay')
LabAccel.grid(row=2,column=0)
EntryAccel=Entry(toolbar,bd=5,width=8)
EntryAccel.grid(row=2,column=1)
# ................................ Write variable values into entries
EntryVx.insert(0,f'{vx:.2f}')
EntryAccel.insert(0,f'{ay:.2f}')
# ......................................................... Main loop
while RunAll:
  # .............................................. Draw ball on canvas
  canvas.delete(ALL)
  canvas.create_polygon(triangle,fill='green')
  canvas.create_oval(x-rad,y-rad,x+rad,y+rad,fill=color)
  canvas.update()
  # .................................................. Ball is moving
  if RunMotion:
    # ...................................................... Bouncing
    if x>=k-y*tanalpha:
      vxi=vx*cosalpha+vy*sinalpha
      veta=-vx*sinalpha+vy*cosalpha
      vxi=-abs(vxi)
      vx=vxi*cosalpha-veta*sinalpha
      vy=+vxi*sinalpha+veta*cosalpha
    elif (y+rad)>=ch:
      vy=-abs(vy)
    elif x<=rad:
      vx=abs(vx)
    elif y<=rad:
      vy=abs(vy)
    # .................................. Update position and velocity
    x+=vx
    y+=vy+0.5*ay
    vy+=ay
  # .................................................... Read entries
  elif GetData:
    try:
      vx=float(EntryVx.get())
    except ValueError:
      pass
    try:
      ay=float(EntryAccel.get())
    except ValuError:
      pass
    EntryVx.delete(0,'end')
    EntryVx.insert(0,f'{vx:.2f}')
    EntryAccel.delete(0,'end')
    EntryAccel.insert(0,f'{ay:.2f}')
    GetData=False
  # ................................................. Wait delay time
  canvas.after(delay)
  #-------------------------
root.destroy()
  
