#!/usr/bin/env python3
from tkinter import Tk,Canvas,E,LAST,N
import numpy as np
#
cw=800
ch=400
Ox=cw/2
Oy=7*ch/8
# ..................................... create root window and canvas
root=Tk()
root.title('Gaussian Plot')
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# .............................................................. axes
ar=(20,20,5)
canvas.create_line(0,Oy,cw-1,Oy,fill='black',arrow=LAST,arrowshape=ar)
canvas.create_line(Ox,Oy,Ox,0,fill='black',arrow=LAST,arrowshape=ar)
canvas.create_text(cw-20,Oy+11,text='x',font=('Times','16','italic'))
canvas.create_text(Ox-15,15,text='y',font=('Times','16','italic'))
# ........................................................... x-ticks
dx=80
xval=-4
while xval<9:
  xpos=Ox+xval*dx
  canvas.create_line(xpos,Oy,xpos,Oy+10)
  canvas.create_text(xpos,Oy+10,text=str(xval),anchor=N)
  xval+=1
# ........................................................... y-ticks
dy=300
yval=0.2
while yval<1.01:
  ypos=Oy-yval*dy
  canvas.create_line(Ox,ypos,Ox-10,ypos)
  canvas.create_text(Ox-20,ypos,text='{:.1f}'.format(yval),anchor=E)
  yval+=0.2
# ................................ make lists of Gaussian coordinates
GaussLin=[]
w2=4.0
x=-5.0
while x<=5.0:
  y=np.exp(-(x**2/w2))
  GaussLin.append(Ox+x*dx)
  GaussLin.append(Oy-y*dy)
  x+=0.1
# .................................................... draw hyperbola
canvas.create_line(GaussLin,fill='blue')
# ....................................................................
root.mainloop()
  
