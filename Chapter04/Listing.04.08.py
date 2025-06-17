#!/usr/bin/env python3
import numpy as np
from scipy.integrate import simpson
# ........................................... Generate x and y values
xx=np.linspace(-5.0,5.0,31)
y=np.exp(-xx**2)
# ....................... Evaluate Definite Integral and Print Result
integ=simpson(y,x=xx)
print(integ)
print(np.sqrt(np.pi))
