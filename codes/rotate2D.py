#!/usr/bin/env python3
import numpy as np
#
answ1=input('Type the x and y components separated by whitespaces: ')
answ2=input('Type the rotation angle in degrees: ')
sx,sy=answ1.split()
vx=float(sx)
vy=float(sy)
alphadeg=float(answ2)
alpha=np.radians(alphadeg)
ca=np.cos(alpha)
sa=np.sin(alpha)
RotMat=np.array([[ca,-sa],[sa,ca]])
vv=np.array([vx,vy])
ww=np.dot(RotMat,vv)
print(ww)


