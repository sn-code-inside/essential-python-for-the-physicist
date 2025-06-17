#!/usr/bin/env python3
from tkinter import *
# .................................................. Global variables
RunAll=True
RunMotion=False
# ................................................. Start/Stop motion
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  if RunMotion:
    StartButton["text"]="Stop"
    CloseButton['state']=DISABLED
  else:
    StartButton["text"]="Restart"
    CloseButton['state']=NORMAL
# ...................................................... Exit program
def StopAll():
  global RunAll
  RunAll=False
# ................................................ Create root window
root=Tk()
root.title("Button ball")
# ......................................... Add canvas to root window
cw=800
ch=400
canvas=Canvas(root, width=cw, height=ch, background='white')
canvas.grid(row=1,column=0)
# ........................................ Add toolbar to root window
toolbar=Frame(root)
toolbar.grid(row=0,column=0,sticky=W)
# ................................................... Toolbar buttons
StartButton=Button(toolbar,text="Start",command=StartStop)
StartButton.grid(row=0,column=0)
CloseButton=Button(toolbar, text="Close", command=StopAll)
CloseButton.grid(row=0,column=1)
# ......................................................... Variables
delay=20 #milliseconds
rad=20
color="red"
x=rad
y=ch-rad
vx=4.0
vy=-7.5
ay=0.1
# ......................................................... Main loop
while RunAll:
  # ............................................. Draw ball on canvas
  canvas.delete(ALL)
  canvas.create_oval(x-rad,y-rad,x+rad,y+rad,fill=color)
  canvas.update()
  # .................................. Bouncing on the canvas borders
  if RunMotion:
    if (x+rad)>=cw:
      vx=-abs(vx)
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
  # ------------------------------------------------- Wait delay time
  canvas.after(delay)
  #-------------------------
root.destroy()
  
