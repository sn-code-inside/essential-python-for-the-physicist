#!/usr/bin/env python3
tria=[]
tria.append([])
tria[0].append(1)
n=1
while n<=10:
  tria.append([])
  tria[n].append(1)
  j=0
  while j<(n-1):
    tria[n].append(tria[n-1][j]+tria[n-1][j+1])
    j+=1
  tria[n].append(1)
  n+=1
for i in range(n):
  print(tria[i])





