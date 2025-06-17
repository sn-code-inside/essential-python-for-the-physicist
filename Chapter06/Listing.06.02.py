#!/usr/bin/env python3
from tkinter import Tk,Canvas
# ..................................... Create Root Window and Canvas
root=Tk()
root.title('Rainbow')
canvas=Canvas(root,width=800,height=150,background="#ffffff")
canvas.grid(row=0,column=0)
# ...................................................... Rainbow Loop
for i in range(0,800):
  ColString="#"
  if i<256:
    r=255;g=i;b=0;
  elif i<512:
    r=511-i;g=255;b=i-256;
  else:
    r=0;g=767-i;b=255;
    if i>672:
      r=(i-672)*2
    if g<0:
      g=0
  # ................................ Build Color String and Draw Line
  ColString+=f'{r:02x}'+f'{g:02x}'+f'{b:02x}'
  line=[i,0,i,150]
  canvas.create_line(line,fill=ColString)
# .................................................... Enter mainloop
root.mainloop()
  
