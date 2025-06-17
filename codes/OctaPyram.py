#!/usr/bin/env python3
#
from vpython import *
#
scene.title='Octagonal Pyramid'
scene.width=1000
scene.height=600
scene.background=vector(1,1,1)
distant_light(direction=vec(1,2,1),color=vec(0.8,0.8,0.8))
distant_light(direction=vec(1,-2,1),color=vec(0.8,0.8,0.8))
#
col=vector(0.7,0.4,0)
pz=[]
px=[]
tria=[]
alpha=pi/4
yy=-1
for i in range(8):
  beta=i*alpha
  zz=cos(beta)
  xx=sin(beta)
  pz.append(zz)
  px.append(xx)
c=vertex(pos=vec(0,1.5,0),color=col)
d=vertex(pos=vec(0,-1,0),color=col)
d.normal=vec(0,-1,0)
for i in range(8):
  j=(i+1)%8
  al=vertex(pos=vec(px[i],yy,pz[i]),color=col)
  ab=vertex(pos=vec(px[i],yy,pz[i]),color=col)
  bl=vertex(pos=vec(px[j],yy,pz[j]),color=col)
  bb=vertex(pos=vec(px[j],yy,pz[j]),color=col)
  ab.normal=vec(0,-1,0)
  bb.normal=vec(0,-1,0)
  trb=triangle(v0=ab,v1=bb,v2=d)
  lnorm=((bl.pos-al.pos).cross(c.pos-bl.pos)).norm()
  al.normal=lnorm
  bl.normal=lnorm
  c.normal=lnorm
  trl=triangle(v0=al,v1=bl,v2=c)
  tria.append(trl)
  tria.append(trb)





