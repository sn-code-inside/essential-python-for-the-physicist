#!/usr/bin/env python3
from tkinter import *
# .................................................. Global variables
RunAll=True
RunMotion=GetData=False
# ................................................. Start/Stop motion
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  if RunMotion:
    StartButton["text"]="Stop"
  else:
    StartButton["text"]="Restart"
# ...................................................... Exit program
def StopAll():
  global RunAll
  RunAll=False
# ...................................................... Read entries
def ReadData(*arg):
  global GetData
  GetData=True
# ................................................ Create root window
root=Tk()
root.title("Entry ball")
root.bind('<Return>',ReadData)
# ......................................... Add canvas to root window
cw=800
ch=400
canvas=Canvas(root, width=cw, height=ch, background='white')
canvas.grid(row=0,column=0)
# ........................................ Add toolbar to root window
toolbar=Frame(root)
toolbar.grid(row=0,column=1,sticky=N)
# ................................................... Toolbar buttons
StartButton=Button(toolbar,text="Start",command=StartStop,width=7)
StartButton.grid(row=0,column=0)
CloseButton=Button(toolbar, text="Close", command=StopAll)
CloseButton.grid(row=0,column=1)
# ........................................ Toolbar labels and entries
LabVx=Label(toolbar,text="Vx")
LabVx.grid(row=1,column=0)
EntryVx=Entry(toolbar,bd=5,width=8)
EntryVx.grid(row=1,column=1)
LabAccel=Label(toolbar,text="Ay")
LabAccel.grid(row=2,column=0)
EntryAccel=Entry(toolbar,bd=5,width=8)
EntryAccel.grid(row=2,column=1)
# ......................................................... Variables
delay=20 #milliseconds
rad=20
color="red"
x=rad
y=ch-rad
vx=4.0
vy=-7.5
ay=0.1
# ................................ Write variable values into entries
EntryVx.insert(0,'{:.2f}'.format(vx))
EntryAccel.insert(0,'{:.2f}'.format(ay))
# ......................................................... Main loop
while RunAll:
  # .............................................. Draw ball on canvas
  canvas.delete(ALL)
  canvas.create_oval(x-rad,y-rad,x+rad,y+rad,fill=color)
  canvas.update()
  # .................................................. Ball is moving
  if RunMotion:
    # ...................................................... Bouncing
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
    EntryVx.insert(0,'{:.2f}'.format(vx))
    EntryAccel.delete(0,'end')
    EntryAccel.insert(0,'{:.2f}'.format(ay))
    GetData=False
  # ................................................. Wait delay time
  canvas.after(delay)
  #-------------------------
root.destroy()
root.mainloop()
  