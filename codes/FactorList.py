#!/usr/bin/env python3
#
def factorial(n):
  fact=1
  while n>1:
    fact*=n
    n-=1
  return fact
for i in range(1,11):
  print(f'{i:2d}{factorial(i):10d}')
