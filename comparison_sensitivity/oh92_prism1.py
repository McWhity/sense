"""
compare own results against references
from the Ulaby example codes provided
http://mrs.eecs.umich.edu/codes/Module10_5/Module10_5.html

for the Oh92 model (PRISM1)

matlab code and python code reproduce same results
graphical interface reproduce a different result!!!
Task: E-mail to Ulaby
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + os.sep + '..')

from sense.surface import Oh92
from sense.util import f2lam

import matplotlib.pyplot as plt
import numpy as np

plt.close('all')

eps = 30.8-40.j   # note that normally the imagionary part is supposed to be negative!

freq = 5.  # GH
s = 0.01  # m
ks = (2.*np.pi/f2lam(freq))*s
theta = np.deg2rad(np.arange(0.,71.) )

O = Oh92(eps, ks, theta)

O.plot()

plt.show()
