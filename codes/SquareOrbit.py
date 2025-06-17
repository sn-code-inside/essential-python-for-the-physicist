#!/usr/bin/env python3
from tkinter import *
# ..................................... Global Settings and Constants
RunAll=True
GetData=RunMotion=False
ButtWidth=9
tau=20                          # milliseconds
# ................................................. Canvas Parameters
cw=600
ch=300
rad=20
# ..................................... Initial Position and Velocity
RIGHT,UP,LEFT,DOWN=range(4)
x=rad
y=ch-rad
vel=1.0
direction=RIGHT
# ......................................................... StartStop
def StartStop():
  global RunMotion
  RunMotion=not RunMotion
  StartButton['text']='Stop' if RunMotion else 'Restart'
  EntrySpeed['state']=DISABLED if RunMotion else NORMAL
  CloseButton['state']=DISABLED if RunMotion else NORMAL
# .......................................................... ReadData
def ReadData(*arg):
  global GetData
  GetData=True
# ........................................................... StopAll   
def StopAll():
  global RunAll
  RunAll=False
# .............................................................. circ
def circ(x,y):
  global rad
  return [x+rad,y+rad,x-rad,y-rad]
# ............................ Create Root Window, Canvas and Toolbar
root=Tk()
root.title('Square Orbit')
root.bind('<Return>',ReadData)
canvas=Canvas(root,width=cw,height=ch,background='white')
canvas.grid(row=0,column=0)
canvas.update()
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
# .......................................,,................ Add Entry
Label(toolbar,text='speed (px/cycle)').grid(row=nr,column=0)
EntrySpeed=Entry(toolbar,bd=5,width=8)
EntrySpeed.grid(row=nr,column=1)
EntrySpeed.insert(0,f'{vel:.2f}')
nr+=1
# .................................................... Animation Loop
while RunAll:
  # ....................................................... Draw Body
  canvas.delete(ALL)
  canvas.create_oval(circ(x,y),fill='red')
  canvas.update()
  if RunMotion:
    # ..................................................... Move Body
    if direction==RIGHT:
      x+=vel
      if x>cw-rad:
        x=cw-rad
        direction=UP
    elif direction==UP:
      y-=vel
      if y<rad:
        y=rad
        direction=LEFT
    elif direction==LEFT:
      x-=vel
      if x<rad:
        x=rad
        direction=DOWN
    elif direction==DOWN:
      y+=vel
      if y>ch-rad:
        y=ch-rad
        direction=RIGHT
    # .................................................... Read Entry
  elif GetData:
    try:
      vel=float(EntrySpeed.get())
    except ValueError:
      pass
    EntrySpeed.delete(0,'end')
    EntrySpeed.insert(0,f'{vel:.2f}')
    GetData=False
  # .............................................................
  canvas.after(tau)
  #------------------------------------------------------------------
root.destroy()
  
