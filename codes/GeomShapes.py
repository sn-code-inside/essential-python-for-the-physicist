#!/usr/bin/env python3
from tkinter import Tk,Canvas,ARC,CHORD,PIESLICE
from numpy import cos,sin,pi
#
cw=600
ch=500
root=Tk()
root.title('Geometric Shapes')
canvas=Canvas(root,width=cw,height=ch,background="#ffffff")
canvas.grid(row=0,column=0)
# ........................................................ rectangle
canvas.create_rectangle(40,10,150,100,fill='#00ff00')
canvas.create_text(95,120,text='This is a rectangle',\
  font=('Helvetica','14'))
# .......................................................... heptagon
Ox=270
Oy=60
r=50.0
Np=7
poly=[]
i=0
alpha=2.0*pi/Np
while i<Np:
  poly.append(Ox+r*sin(i*alpha))
  poly.append(Oy-r*cos(i*alpha))
  i+=1
canvas.create_polygon(poly,fill='#00ffff',outline='#000000')
canvas.create_text(270,120,text='This is a heptagon',\
  font=('Helvetica','14'))
# ........................................................... ellipse
canvas.create_oval(400,10,590,109,fill='red')
canvas.create_text(485,120,text='This is an ellipse',\
  font=('Helvetica','14'))
# ............................................................... arc
canvas.create_arc(10,150,150,300,start=20,extent=220,fill='#ffff00',\
  outline='#ffff00',style=PIESLICE)
canvas.create_text(80,300,text='SLICE',font=('Helvetica','12'))
canvas.create_arc(200,150,340,300,start=20,extent=220,fill='',\
  outline='#0000ff',style=CHORD)
canvas.create_text(270,300,text='CHORD',font=('Helvetica','12'))
canvas.create_arc(400,150,540,300,start=20,extent=220,outline='#ff0000'\
  ,style=ARC)
canvas.create_text(470,300,text='ARC',font=('Helvetica','12'))
# .............................................................. line
line=[]
i=0
dx=(cw-20)/6
dy=40
while i<7:
  line.append(10+i*dx)
  line.append(380+dy)
  dy=-dy
  i+=1
canvas.create_line(line,fill='blue')
canvas.create_text(300,440,text='This is a polyline',\
  font=('Helvetica','14'))
# ................................................... Greek letters
canvas.create_text(300,480,text=\
  'Greek letters: \
\u0393\u03B5\u03c9\u03BC\u03B5\u03C4\u03C1\u03B9\u03B1',\
  font=('Helvetica','12'))
#
root.mainloop()
  
