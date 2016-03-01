# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 15:55:35 2016

@author: ctugtez
"""

# Import relevant modules
import pymc
import numpy as np
import matplotlib.pyplot as pl

# Some data
n = 5 * np.ones(4, dtype=int)
x = np.array([-.86, -.3, -.05, .73])



# Priors on unknown parameters
alpha = pymc.Normal('alpha', mu=0, tau=.01)
beta = pymc.Normal('beta', mu=0, tau=.01)
charlie = pymc.Normal('charlie', mu=0, tau=.01)

# Arbitrary deterministic function of parameters
@pymc.deterministic
def theta(a=alpha, b=beta, c=charlie):
    """theta = logit^{-1}(a+b)"""
    y = pymc.invlogit(a*x**2 + b * x + c)
    return y

# Binomial likelihood for data
d = pymc.Binomial('d', n=n, p=theta, value=np.array([0., 1., 3., 5.]),
                  observed=True)