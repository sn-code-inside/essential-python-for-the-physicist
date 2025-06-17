import math
# ......................................................... factorize
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
# ........................................................... FiboSeq
def FiboSeq(n):   # return Fibonacci sequence up to n
  result = []
  a,b = 0, 1
  while b < n:
    result.append(b)
    a, b = b, a+b
  return result

  
  
  



