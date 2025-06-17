#!/usr/bin/env python3
from numpy import sqrt
#
with open('roots.txt','w') as hnd:
  hnd.write('  n  square root  cube root\n\n')
  for n in range(21):
    hnd.write(f'{n:3d}{sqrt(n):11.6f}{n**(1/3):13.6f}\n')
  

