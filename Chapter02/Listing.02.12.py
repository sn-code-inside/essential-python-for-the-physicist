#!/usr/bin/env python3
import numpy as np
from struct import pack
# ...................................................................
i=1
with open('StringsInBin.bin', 'wb') as hnd:
  # ...................................................... write text
  buff=pack('=25s',bytes('This is a comment'.encode()))
  hnd.write(buff)
  hnd.seek(25)
  buff=pack('=25s',bytes('This is another comment'.encode()))
  hnd.write(buff)
  hnd.seek(50)
  buff=pack('=25s',bytes('    n           ln(n)'.encode()))
  hnd.write(buff)
  hnd.seek(50)
  # ............................................... write binary data
  hnd.seek(75)
  while i<=20:
    sqrti=np.sqrt(float(i))
    buff=pack('=id',i,sqrti)
    hnd.write(buff)
    i+=1
