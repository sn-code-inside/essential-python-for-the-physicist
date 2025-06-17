#!/usr/bin/env python3
import numpy as np
from struct import pack,unpack,calcsize
# ...................................................................
i=1
print(calcsize('id'))
with open("test.bin", "wb") as hnd, open('test.txt','wt') as hnd2:
  while i<=20:
    sqrti=np.sqrt(float(i))
    buff=pack('=id',i,sqrti)
    hnd.write(buff)
    hnd2.write('{:2d},{:22.17f}\n '.format(i,sqrti))
    i+=1
with open("test.bin", "rb") as hnd1:
  while True:
    buff1=hnd1.read(12)
    if len(buff1)<12:
      break
    n,sqn=unpack('=id',buff1)
    print('{:5d} {:22.17f} '.format(n,sqn))
    #print('{:5d} '.format(n))
