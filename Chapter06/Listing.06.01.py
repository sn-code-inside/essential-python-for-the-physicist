#!/usr/bin/env python3
from tkinter import Tk,Canvas
#
col=input('Type a color string: ')
colstring="#"+col
root=Tk()
root.title('Check Color')
canvas=Canvas(root,width=200,height=200,background=colstring)
canvas.grid(row=0,column=0)
root.mainloop()
