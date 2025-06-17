#!/usr/bin/env python3
import numpy as np
from struct import unpack,calcsize
# ...................................................................
with open('StringsInBin.bin', 'rb') as hnd:
  # ....................................................... read text
  buff=hnd.read(calcsize('=25s'))
  text=buff.decode().rstrip(chr(0))
  print(text,len(text))
  hnd.seek(calcsize('=25s'))
  buff=hnd.read(calcsize('=25s'))
  text=buff.decode().rstrip(chr(0))
  print(text,len(text))
  hnd.seek(50)
  buff=hnd.read(calcsize('=25s'))
  text=buff.decode().rstrip(chr(0))
  print(text)
  # ................................................ read binary data
  hnd.seek(3*calcsize('=25s'))
  while True:
    buff1=hnd.read(calcsize('=id'))
    if len(buff1)<calcsize('=id'):
      break
    n,sqn=unpack('=id',buff1)
    print(f'{n:5d} {sqn:22.17f} ')
