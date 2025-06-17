#!/usr/bin/env python3
from tkinter import Tk,Canvas,ALL
# .......................................... open Tkinter root window
root=Tk()
root.title("Gravity ball")
# ........................................... canvas width and height
cw=800
ch=400
# ......................................... add canvas to root window
canvas=Canvas(root,width=cw,height=ch,background='white')
canvas.grid(row=0,column=1)
# ......................................................... variables
delay=20 #milliseconds
rad=20
color="red"
x=rad
y=ch-rad
vx=4.0
vy=-7.5
ay=0.1
# ......................................................... main loop
while True:
  # ............................................. draw ball on canvas
  canvas.delete(ALL)
  canvas.create_oval(x-rad,y-rad,x+rad,y+rad,fill=color)
  canvas.update()
  # ..................... is the ball bouncing on the canvas borders?
  if (x+rad)>=cw:
    vx=-abs(vx)
  elif (y+rad)>=ch:
    vy=-abs(vy)
  elif x<=rad:
    vx=abs(vx)
  elif y<=rad:
    vy=abs(vy)
  # ......................... update position and velocity components
  x+=vx
  y+=vy+0.5*ay
  vy+=ay
  # ................................................. wait delay time
  canvas.after(delay)
  
