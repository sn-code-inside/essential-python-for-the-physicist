#!/usr/bin/env python3
from tkinter import Tk,Canvas,ALL
# .......................................... open Tkinter root window
root=Tk()
root.title("Framed ball")
# ........................................... canvas width and height
cw=800
ch=640
# ......................................... add canvas to root window
canvas=Canvas(root,width=cw,height=ch,background='white')
canvas.grid(row=0,column=0)
# ......................................................... variables
delay=20 #milliseconds
rad=20
color="red"
x=rad
y=ch-rad
vx=4.0
vy=-5.0
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
  y+=vy
  # ................................................. wait delay time
  canvas.after(delay)
  
