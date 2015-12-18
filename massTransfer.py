# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:03:47 2015

@author: ctugtez
"""

import numpy 
from kapteyn import kmpfit
import matplotlib.pyplot as plt
from plotting import fitPlot
from dataLoad import minType, method



def model(p,epoch):
    a, b, c = p #a (A) is number of represent change by mass transfer. b is change of period, c is T0 correction.
    y =  c + (b*epoch) + (a * epoch**2)
    return y
    
def residuals(p,data):
    x, y, weight = data
    return y - model(p,x)
    
    
def fitIt(tzero,period,oc,epoch,weight):

    paramsinitial = [0, 0, 0]
    
    fitobj = kmpfit.Fitter(residuals=residuals, data=(epoch,oc,weight))
    
    try:
        fitobj.fit(params0=paramsinitial)
    except Exception, mes:
        print "Something went wrong with fit: ", mes
        raise SystemExit
        
    print "Fit status: ", fitobj.message
    print "Best-fit parameters:      ", fitobj.params
    print "Covariance errors:        ", fitobj.xerror
    print "Standard errors           ", fitobj.stderr
    print "Chi^2 min:                ", fitobj.chi2_min
    print "Reduced Chi^2:            ", fitobj.rchi2_min
    print "Iterations:               ", fitobj.niter
    print "Number of function calls: ", fitobj.nfev
    print "Number of free pars.:     ", fitobj.nfree
    print "Degrees of freedom:       ", fitobj.dof
    print "Number of pegged pars.:   ", fitobj.npegged
    print "Covariance matrix:\n", fitobj.covar

    
    xmin = min(epoch)
    xmax = max(epoch)
    xlen = len(epoch)
    fitx = numpy.linspace(xmin,xmax,xlen)
    
    fity = model(fitobj.params, fitx)
    
    fitPlot(epoch, oc, minType, method,fitx, fity)

    


