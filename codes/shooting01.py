#!/usr/bin/env python3
#coding: utf8 
import os
from pylab import *
from numpy import *
from scipy import *
from scipy.integrate import *

nPoints=500
nPointsPlot=200
xiMax=10.0
xiMaxPlot=(xiMax*nPointsPlot)/nPoints
DeltaXi=xiMax/float(nPoints)
DeltaXi2=DeltaXi**2
nEigen=7
EigvStep=0.005
tolerance=1.0e-12;

xi=np.linspace(0,xiMax,nPoints)

def dfdt(y,xi,params):
  psi,dpsidt=y    #    unpack y
  E,A,B=params    #    unpack parameters
  derivs=[dpsidt,(A*xi*xi-B*E)*psi]
  return derivs

def SymmWell(params,xi,iEv,EigvStart,EigvStep,tolerance,dfdt,psi):
  # ................................................................ initialize
  params[0]=EigvStart
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
#y = 0.5*x**2 # potential. Why 0.5 ??????
#plot(x,y) # x^2
# ................................................................... draw grid
grid(True)
# ...........................................................................
EigvStart=0.495;
#plot([0,xiMaxPlot],[0.5,0.5],'black')
i=0
iEigv=0
while i<3:
  params=[EigvStart,1.0,2.0]
  psi=[]
  SymmWell(params,xi,iEigv,EigvStart,EigvStep,tolerance,dfdt,psi)
  while len(psi)>nPointsPlot:
    psi.pop()
  psi=[p*2.0 for p in psi]
  print(i,EigvStart)
  #----------------------------------------------
  #psi=[x+EigvStart for x in psi]
  plot(x,psi)
  EigvStart+=0.005
  i+=1
# ...........................................................................
text(3.3,3.0,'$E=0.495$',fontsize=14,rotation=50)
text(3.4,-2.1,'$E=0.505$',fontsize=14,rotation=-55)
text(3.5,0.2,'$E=0.5$',fontsize=14)
#text(2.2,4.0,'Potential',fontsize=14)
# ...........................................................................
show() # show the plot

