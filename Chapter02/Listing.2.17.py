#!/usr/bin/env python3
answ=input('Type a number: ')
try:
  num=int(answ)
except ValueError:
  print('This is not an allowed number!')
  exit()
if num<0:
  print(f'{num:d} is negative!')
  exit()
fact=1
while num>1:
  fact*=num
  num-=1
print(fact)
  
  

