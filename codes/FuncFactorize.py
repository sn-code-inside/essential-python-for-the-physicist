#!/usr/bin/env python3
import math
# ................................................... Define Function
def factorize(n):
  sqnf=int(math.ceil(math.sqrt(float(n))))
  factors = []
  while n%2==0:
    factors.append(2)
    n=n//2
  i=3
  while i<=sqnf:
    while n%i==0:
      factors.append(i)
      n=n//i
      sqnf=int(math.ceil(math.sqrt(float(n))))
    i+=2
  if n!=1:
    factors.append(n)
  return factors
# ............................................. Function-Calling Loop
for i in range(2,21):
  fact=factorize(i)
  if len(fact)==1:
    print(i,'is prime')
  else:
    print(i,fact)
  
  
  
