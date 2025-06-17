123456789098765432#!/usr/bin/env python3
import math as mt
import time
# ......................................... Inout Number to Factorize
num=input('Type a number: ')
start=time.time()
# ............................ Covert String to Integer, Count Digits
n=int(num)
print('digits: {:d}'.format(len(num)))
# ........................................... Limit to Largest Factor
sqnf=mt.ceil(mt.sqrt(float(n)))
# ...................................... Create Empty List of Factors
factors=[]
# ........................................... Check if Divisible by 2
while n%2==0:
  factors.append(2)
  n=n//2
  sqnf=mt.ceil(mt.sqrt(float(n)))
# ................................. Check if Divisible by Odd Numbers
i=3
while i<=sqnf:
  while n%i==0:
    factors.append(i)
    n=n//i
    sqnf=mt.ceil(mt.sqrt(float(n)))
  i+=2
#  ...................................................... Last Factor
if n!=1:
  factors.append(n)
# ..................................................... Print Results
print(factors)
elapsed=time.time()-start
print(f'elapsed time: {elapsed:f} s\n')
