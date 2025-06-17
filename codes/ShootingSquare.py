#!/usr/bin/env python3
#coding: utf8 
import os
from pylab import *
from numpy import *
from scipy import *
from scipy.integrate import *

xi0=10.0
nPointsWell=100
nPointsPlot=3*nPointsWell
nPoints=5*nPointsWell
norm=1.0
xiMaxPlot=(xi0*nPointsPlot)/nPointsWell
xiMax=(xi0*nPoints)/nPointsWell
DeltaXi=xi0/nPointsWell
EigvStep=0.0005
tolerance=1.0e-12;
nEigen=7
EigvStep=0.0005
tolerance=1.0e-12;

xi=np.linspace(0,xiMax,nPoints)

def dfdt(y,xi,params):
  psi,dpsidt=y    #    unpack y
  E,xi0=params    #    unpack parameters
  if xi<xi0:
    derivs=[dpsidt,-E*psi]
  else:
    derivs=[dpsidt,(1-E)*psi]
  return derivs

def SymmWell(params,xi,iEv,EigvStart,EigvStep,tolerance,dfdt,psi):
  # ................................................................ initialize
  eigv1=EigvStart
  params[0]=eigv1
  if iEv%2==0:
    y=[1.0,0.0]
  else:
    y=[0.0,1.0]
  psoln=odeint(dfdt,y,xi,args=(params,))
  # ........................................................ list wave function
  del psi[:]
  for i in range(len(xi)):
    psi.append(psoln[i,0])
  # ...........................................................................
  return EigvStart
  
# ................................................. evaluate and draw potential
x = linspace(0,xiMaxPlot,nPointsPlot)
# ................................................................... draw grid
grid(True)
# ...........................................................................
Eigv0=0.020379039544995717
EigvStep=5.0e-10
EigvStart=Eigv0-EigvStep;
plot([10.0,10.0],[-0.24,0.399],'black')
i=0
iEigv=0
while i<3:
  params=[EigvStart,xi0]
  psi=[]
  SymmWell(params,xi,iEigv,EigvStart,EigvStep,tolerance,dfdt,psi)
  NormFact=2.0*sqrt(simps(square(psi[:2*nPointsWell]),dx=DeltaXi,even='first'))
  while len(psi)>nPointsPlot:
    psi.pop()
  psi=[p/NormFact for p in psi]
  print(i,EigvStart)
  #----------------------------------------------
  plot(x,psi)
  EigvStart+=EigvStep
  i+=1
# ...........................................................................
text(27.5,0.25,'$W_0+\delta W$',fontsize=18,rotation=80)
text(27.0,-0.1,'$W_0-\delta W$',fontsize=18,rotation=-80)
text(28.0,0.01,'$W_0$',fontsize=18)
text(9.6,-0.28,'$\\xi_0$',fontsize=18)
ylabel(r'$\psi(\xi)$',fontsize=20)
xlabel(r'$\xi$',fontsize=20)
# .............................................................................
savefig('ShootingSquare01.eps', format='eps', dpi=1000)
# ...........................................................................
show() # show the plot

