#!/usr/bin/env python3
from math import sqrt
#
num=[]
with open('numdata.txt','r') as hnd:
  while True:
    buff=hnd.readline()
    if not buff:
      break
    try:
      num.append(float(buff.strip()))
    except ValueError:
      pass
#
with open('sqrtdata.txt','w') as hnd:
  for x in num:
    hnd.write(f'{x:6.2f}{sqrt(x):12.4f}\n')
