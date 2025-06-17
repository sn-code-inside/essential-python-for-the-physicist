#!/usr/bin/env python3
#
from vpython import *
#
scene.width=600
scene.height=600
scene.background=vector(1,1,1)
distant_light(direction=vec(1,0,1),color=vec(1,1,1))
distant_light(direction=vec(-1,0,1),color=vec(1,1,1))
#
alpha=pi/6
h=cos(alpha)/2
xx=sin(alpha)
a=vertex(pos=vec(0,h,0),color=vec(1,0,0))
b=vertex(pos=vec(-xx,-h,0),color=vec(0,1,0))
c=vertex(pos=vec(xx,-h,0),color=vec(0,0,1))
T=triangle(v0=a,v1=b,v2=c)
  






