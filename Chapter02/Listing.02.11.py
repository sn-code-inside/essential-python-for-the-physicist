#!/usr/bin/env python3
import numpy as np
from struct import unpack,calcsize
# ...................................................................
num=[]
lognum=[]
FieldSize=calcsize('=id')
with open('logar.bin','rb') as hnd:
  while True:
    buff=hnd.read(FieldSize)
    if len(buff)<FieldSize:
      break
    n,logn=unpack('=id',buff)
    num.append(n)
    lognum.append(logn)
    print(f'{n:5d} {logn:22.16f}')
with open('logar.txt','w') as hnd:
  for i,x in enumerate(lognum):
    hnd.write(f'{num[i]:5d}{x:22.16f}\n')
