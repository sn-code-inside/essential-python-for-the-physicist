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
# ......................................................... Variables
delay=20 #milliseconds
rad=20
color='red'
x=rad
y=rad
vx=4.0
vy=7.5
ay=-0.2
mass=10
ener=mass*(0.5*(vx**2+vy**2)-ay*y)
# ................................................ Create root window
root=Tk()
root.title('Gravity Euler')
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
nr=0
StartButton=Button(toolbar,text='Start',command=StartStop,width=7)
StartButton.grid(row=nr,column=0)
CloseButton=Button(toolbar, text='Close', command=StopAll)
CloseButton.grid(row=nr,column=1)
nr+=1
# ........................................ Toolbar labels and entries
LabVx=Label(toolbar,text='Vx')
LabVx.grid(row=nr,column=0)
EntryVx=Entry(toolbar,bd=5,width=8)
EntryVx.grid(row=nr,column=1)
nr+=1
LabAccel=Label(toolbar,text='Ay')
LabAccel.grid(row=nr,column=0)
EntryAccel=Entry(toolbar,bd=5,width=8)
EntryAccel.grid(row=nr,column=1)
nr+=1
# ...................................................... Energy label
EnerLab0=Label(toolbar,text='Energy:',font=('Helvetica',11))
EnerLab0.grid(row=nr,column=0)
EnerLab=Label(toolbar,text='{:8.3f}'.format(ener),font=('Helvetica',11))
EnerLab.grid(row=nr,column=1,sticky=W)
nr+=1
# ................................ Write variable values into entries
EntryVx.insert(0,'{:.2f}'.format(vx))
EntryAccel.insert(0,'{:.2f}'.format(ay))
# ......................................................... Main loop
count=0
while RunAll:
  # .............................................. Draw ball on canvas
  canvas.delete(ALL)
  canvas.create_oval(x-rad,ch-(y+rad),x+rad,ch-(y-rad),fill=color)
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
    # ................. Update position and velocity, Euler algorithm
    x+=vx
    y+=vy
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
  # .................................................... Write energy
  count+=1
  if count >=10:
    count=0
    ener=mass*(0.5*(vx**2+vy**2)-ay*y)
    EnerLab['text']='{:8.3f}'.format(ener)
  # ................................................. Wait delay time
  canvas.after(delay)
  #-------------------------
root.destroy()
  
