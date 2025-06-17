#!/usr/bin/env python3
import numpy as np
from scipy.integrate import odeint,simpson
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
# .................................................. Numerical Values
nPoints=500
nPointsPlot=200
xiMax=10.0
xiMaxPlot=(xiMax*nPointsPlot)/nPoints
DeltaXi=xiMax/float(nPoints)
scale=4.0
nEigen=8
EigvStep=0.005
tolerance=1.0e-12;
# ................................................. List of xi Values
xi=np.linspace(0,xiMax,nPoints)
# ......................................... Function Called by odeint
def dfdxi(y,xi,params):
  psi,dpsidt=y    #    unpack y
  E,=params       #    unpack parameters
  derivs=[dpsidt,(xi*xi-2.0*E)*psi]
  return derivs
# ................................................. Function SymmWell
def SymmWell(params,xi,iEv,EigvStart,EigvStep,tolerance,dfdxi,psi):
  # ...................................................... initialize
  eigv1=EigvStart
  params[0]=eigv1
  if iEv%2==0:
    y=[1.0,0.0]
  else:
    y=[0.0,1.0]
  psoln=odeint(dfdxi,y,xi,args=(params,))
  PsiEnd1=psoln[-1,0]
  # ............................................. search for interval
  while True:
    eigv2=eigv1+EigvStep
    params[0]=eigv2
    psoln=odeint(dfdxi,y,xi,args=(params,))
    PsiEnd2=psoln[-1,0]
    if (PsiEnd1*PsiEnd2)<0.0:
      break
    PsiEnd1=PsiEnd2
    eigv1=eigv2
  # ............................... Logarithmic Search for Eigenvalue
  while True:
    eigvmid=(eigv1+eigv2)/2.0
    params[0]=eigvmid
    if abs(eigv1-eigv2)<tolerance:
      break
    psoln=odeint(dfdxi,y,xi,args=(params,))
    PsiEndMid=psoln[-1,0]
    if (PsiEndMid*PsiEnd1)>0 :
      PsiEnd1=PsiEndMid
      eigv1=eigvmid
    else:
      PsiEnd2=PsiEndMid
      eigv2=eigvmid
  # .............................................. List Wave Function
  del psi[:]
  for i in range(len(xi)):
    psi.append(psoln[i,0])
  # ............................................... Return Eigenvalue
  return eigvmid
# ....................................... Evaluate and Draw Potential
x = np.linspace(-xiMaxPlot,xiMaxPlot,(2*nPointsPlot)+1)
y = 0.5*x**2 # potential.
plt.plot(x,y) # x^2
# ......................................................... Draw Grid
plt.grid(True)
# ...................................................................
eigv=[]
EigvStart=0.0;
i=0
while i<nEigen:
  params=[EigvStart]
  psi=[]
  eigv.append(SymmWell(params,xi,i,EigvStart,EigvStep,tolerance,\
    dfdxi,psi))
  print(i,eigv[i])
  # .................................. Truncate Diverging Tail of psi
  while len(psi)>5:
    if abs(psi[-2])>abs(psi[-1]):
      break
    psi.pop()
  # ................................................... Normalize psi
  NormFact=np.sqrt(2.0*simpson(np.square(psi),even='first'))
  # ......................................... Truncate to Plot Length
  del psi[(nPointsPlot+1):]
  if len(psi)<(nPointsPlot+1):
    while len(psi)<(nPointsPlot+1):
      psi.append(0.0)
  normpsi=[i*(scale/NormFact) for i in psi]
  psineg=list(reversed(normpsi))
  if i%2==1:  # ..................... Odd Functions Are Antisymmetric
    for k in range(len(psineg)):
      psineg[k]=-psineg[k]
  # .................................................. Form Whole psi
  psineg.pop()
  psi=psineg+normpsi
  #----------------------------------------------
  EnerShift=eigv[i]
  psi=[x+EnerShift for x in psi]
  plt.plot([-xiMaxPlot,xiMaxPlot],[EnerShift,EnerShift],'black')
  plt.plot(x,psi)
  # ................................................. Next Eigenvalue
  EigvStart=eigv[i]+EigvStep
  i+=1
# ...................................................................
plt.ylabel(r'$W=E/(\hbar\omega)$',fontsize=16)
plt.xlabel(r'$\displaystyle\xi=\sqrt{\frac{\omega m}{\hbar}}\,x$',\
  fontsize=16)
plt.tight_layout()
# ....................................................................
plt.savefig('QuantOscill00.pdf', format='pdf', dpi=1000)
plt.show()

