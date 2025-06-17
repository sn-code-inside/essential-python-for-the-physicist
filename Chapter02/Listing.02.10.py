#!/usr/bin/env python3
import numpy as np
from struct import pack
# ...................................................................
n=1
with open('logar.bin','wb') as hnd:
  while n<=20:
    buff=pack('=id',n,np.log(float(n)))
    hnd.write(buff)
    n+=1

