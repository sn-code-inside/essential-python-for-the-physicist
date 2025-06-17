#!/usr/bin/env python3
import numpy as np
from scipy.integrate import odeint,simpson
import matplotlib.pyplot as plt
# ................................................. select plot fonts
plt.rcParams.update({"text.usetex":True,"font.family":"serif",\
  "font.serif": ["Times"]})
# ...................................................................
xi0=10.0
nPointsWell=100
nPointsPlot=3*nPointsWell
nPoints=5*nPointsWell
scale=0.2
xiMaxPlot=(xi0*nPointsPlot)/nPointsWell
xiMax=(xi0*nPoints)/nPointsWell
EigvStep=0.03
DeltaXi=xi0/nPointsWell
tol=1.0e-12;
params=[0,xi0]
# ...................................................................
WaveFun=np.array([])
# ...................................................................
xi=np.linspace(0,xiMax,nPoints)
# .................................. derivatives of the wave function
def dfdxi(y,xi,params):
  psi,dpsidxi=y    #    unpack y
  E,xi0=params    #    unpack parameters
  if xi<xi0:
    derivs=[dpsidxi,-E*psi]
  else:
    derivs=[dpsidxi,(1-E)*psi]
  return derivs
# ...............................................--..................
def SymmWell(params,xi,iEv,EigvStart,EigvStep,tol,dfdxi,psi):
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
    if eigv2>1.0:
      return -1
    params[0]=eigv2
    psoln=odeint(dfdxi,y,xi,args=(params,))
    PsiEnd2=psoln[-1,0]
    if (PsiEnd1*PsiEnd2)<0.0:
      break
    PsiEnd1=PsiEnd2
    eigv1=eigv2
  # ............................... logarithmic search for eigenvalue
  while True:
    eigvmid=(eigv1+eigv2)/2.0
    if abs(eigv1-eigv2)<tol:
      break
    params[0]=eigvmid
    psoln=odeint(dfdxi,y,xi,args=(params,))
    PsiEndMid=psoln[-1,0]
    if (PsiEndMid*PsiEnd1)>0 :
      PsiEnd1=PsiEndMid
      eigv1=eigvmid
    else:
      PsiEnd2=PsiEndMid
      eigv2=eigvmid
  # .............................................. list wave function
  for i in range(len(xi)):
    psi.append(psoln[i,0])
  # .................................................................
  return eigvmid
# .................................................. ................
x=np.linspace(-xiMaxPlot,xiMaxPlot,(2*nPointsPlot)+1)
# ......................................................... draw grid
plt.grid(True)
# .................................................................
eigv=[]
EigvStart=0.0;
i=0
while True:
  params=[EigvStart,xi0]
  psi=[]
  eigv.append(SymmWell(params,xi,i,EigvStart,EigvStep,tol,dfdxi,psi))
  if eigv[i]>0:
    print(i,eigv[i])
  else:
    break
  # .................................. truncate diverging tail of psi
  while len(psi)>5:
    if abs(psi[-2])>abs(psi[-1]):
      break
    psi.pop()
  # .................................................... normalize psi
  NormFact=np.sqrt(2.0*simpson(np.square(psi),dx=DeltaXi,even='first'))
  # .......................................... truncate to plot length
  del psi[(nPointsPlot+1):]
  if len(psi)<(nPointsPlot+1):
    while len(psi)<(nPointsPlot+1):
      psi.append(0.0)
  normpsi=[i*(scale/NormFact) for i in psi]
  psineg=list(reversed(normpsi))
  if i%2==1:  # ..................... odd functions are antisymmetric
    for k in range(len(psineg)):
      psineg[k]=-psineg[k]
  # .................................................. form whole psi
  psineg.pop()
  psi=psineg+normpsi
  #----------------------------------------------
  EnerShift=eigv[i]
  psi=[x+EnerShift for x in psi]
  plt.plot([-xiMaxPlot,xiMaxPlot],[EnerShift,EnerShift],'black',\
    linewidth=0.5)
  plt.plot(x,psi)
  # ................................................. next eigenvalue
  EigvStart=eigv[i]+EigvStep
  i+=1
# .................................................. plot square well
plt.plot([-xiMaxPlot,-xi0],[1.0,1.0],color='black')
plt.plot([-xi0,-xi0],[1.0,0.0],color='black')
plt.plot([xi0,xi0],[0.0,1.0],color='black')
plt.plot([xi0,xiMaxPlot],[1.0,1.0],color='black')
plt.ylim(0.0,1.1)
plt.ylabel(r'Energy/$V_0$',fontsize=18)
plt.xlabel(r'$x\;\frac{\sqrt{2mV_0}}{\hbar}$',fontsize=24)
plt.tight_layout()
# -------------------------------------------------------------------
plt.savefig('SquareWell00.pdf', format='pdf')
plt.show() # show the plot
