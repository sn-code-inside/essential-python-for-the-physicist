#!/usr/bin/env python3
from math import sqrt
#
num=[]
hnd=open('numdata.txt','r')
while True:
  buff=hnd.readline()
  if not buff:
    break
  try:
    num.append(float(buff.strip()))
  except ValueError:
    pass
hnd.close()
#
hnd=open('sqrtdata.txt','w')
for x in num:
  hnd.write(f'{x:6.2f}{sqrt(x):12.4f}\n')
hnd.close()
