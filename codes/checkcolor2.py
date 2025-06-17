#!/usr/bin/env python3
from tkinter import Tk,Canvas
from sys import argv
#
script,col=argv
colstring="#"+col
root=Tk()
root.title('Check Color')
canvas=Canvas(root,width=200,height=200,background=colstring)
canvas.grid(row=0,column=0)
#
root.mainloop()
  
