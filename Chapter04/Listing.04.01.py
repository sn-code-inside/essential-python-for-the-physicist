#!/usr/bin/env python3
import numpy  as np
#
A=np.array([[3.0,-2.0,-1.0],[2.0,-2.0,4.0],[-1.0,0.5,-1.5]])
b=np.array([2.0,0.0,-1.0])
x=np.linalg.solve(A,b)
print('x =',x)
bb=np.dot(A,x)
print('bb =',bb)


