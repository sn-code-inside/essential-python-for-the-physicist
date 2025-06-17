#!/usr/bin/env python3
from tkinter import Tk,Canvas,E,LAST,N
import numpy as np
# ....................................................... Canvas Size
cw=800
ch=400
Ox=cw/2
Oy=ch/2
# ..................................... Create Root Window and Canvas
root=Tk()
root.title('Hyperbola Plot')
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ......................................................... Plot Axes
canvas.create_line(0,Oy,cw-1,Oy,fill='black',arrow=LAST,
                   arrowshape=(20,20,5))
canvas.create_line(Ox,ch-1,Ox,0,fill='black',arrow=LAST,
                   arrowshape=(20,20,5))
canvas.create_text(cw-20,Oy+11,text='x',font=('Times','16',
                                              'italic'))
canvas.create_text(Ox-15,15,text='y',font=('Times','16',
                                              'italic'))
# ........................................................... x-Ticks
dx=80
for x in range(dx,cw,dx):
  canvas.create_line(x,Oy,x,Oy+10)
  canvas.create_text(x,Oy+10,text=str(x-Ox),anchor=N)
# ........................................................... y-Ticks
dy=40
for y in range(dy,ch,dy):
  canvas.create_line(Ox-8,y,Ox,y)
  canvas.create_text(Ox-10,ch-y,text=str(y-Oy),anchor=E)
# ........................................................ Asymptotes
canvas.create_line(0,0,cw-1,ch-1,fill='red')
canvas.create_line(0,ch-1,cw-1,0,fill='red')
# ............................... Make Lists of Hyperbola Coordinates
a=80.0
b=40.0
y=-ch/2
hyp1=[]
hyp2=[]
while y<ch/2:
  x=(a/b)*np.sqrt(y*y+b*b)
  hyp1.append(Ox+x)
  hyp1.append(Oy-y)
  hyp2.append(Ox-x)
  hyp2.append(Oy-y)
  y+=2
# .................................................... Draw hyperbola
canvas.create_line(hyp1,fill='blue')
canvas.create_line(hyp2,fill='blue')
# ....................................................................
root.mainloop()
  
