# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:30:31 2015

@author: ctugtez
"""

from plotting import fitPlot
from dataLoad import minType, method
import numpy, pymc
import massTransferMC

def model(a,b,c,epoch):
    return a*epoch**2 + b*epoch + c
    
def fitMassMC(tzero,period,oc,epoch,weight):
    z = numpy.polyfit(epoch, oc, 2)   # the traditional chi-square fit
    print "The chi-square result: ",  z
    #priors
    sig = pymc.Uniform("sig", 0.0, 100.0, value=1.)
    
    a = pymc.Uniform("a", -10.0, 10.0, value= 0.0)
    b = pymc.Uniform("b", -10.0, 10.0, value= 0.0)
    c = pymc.Uniform("c", -10.0, 10.0, value= 0.0)

    #model
    @pymc.deterministic(plot=False)
    def mod_quadratic(x=epoch, a=a, b=b, c=c):
          return a*x**2 + b*x + c
    
    #likelihood
    quad_y = pymc.Normal("y", mu=mod_quadratic, tau=1.0/sig**2, value=oc, observed=True)
    
    quad_model = pymc.Model([quad_y, a, b, c])
    quadratic_mcmc = pymc.MCMC(quad_model)
    quadratic_mcmc.sample(1000000, 200)
    #pymc.Matplot.plot(quadratic_mcmc)
    
    a = quadratic_mcmc.trace('a')[:]
    b = quadratic_mcmc.trace('b')[:]
    c = quadratic_mcmc.trace('c')[:]
    
    print('Last value of a: {}, and the median value is {}'.format(a[-1], numpy.median(a)))
    print('Last value of b: {}, and the median value is {}'.format(b[-1], numpy.median(b)))
    print('Last value of c: {}, and the median value is {}'.format(c[-1], numpy.median(c)))
    
    print quadratic_mcmc.stats()
    
    xmin = min(epoch)
    xmax = max(epoch)
    xlen = len(epoch)
    fitx = numpy.linspace(xmin,xmax,xlen)
    
    fity = model(a[-1],b[-1],c[-1],fitx)
    
    fitPlot(epoch, oc, minType, method,fitx, fity)