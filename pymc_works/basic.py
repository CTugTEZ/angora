# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 15:56:05 2016

@author: ctugtez
"""

import pymc
import mymodel

S = pymc.MCMC(mymodel, db='pickle')
S.sample(iter=10000, burn=5000, thin=2)
print S.theta.y
pymc.Matplot.plot(S)