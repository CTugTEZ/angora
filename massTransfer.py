# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:03:47 2015

@author: ctugtez
"""

import numpy 
from kapteyn import kmpfit
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

    paramsinitial = (0, 0, 0)
    
    fitobj = kmpfit.Fitter(residuals=residuals, data=(epoch,oc,weight))
    
    try:
        fitobj.fit(params0=paramsinitial)
    except Exception, mes:
        print "Something went wrong with fit: ", mes
        raise SystemExit
    
    #results  
    l1= "Fit status: ", fitobj.message
    l2= "Best-fit parameters:      ", fitobj.params
    l3= "Covariance errors:        ", fitobj.xerror
    l4= "Standard errors           ", fitobj.stderr
    l5= "Chi^2 min:                ", fitobj.chi2_min
    l6= "Reduced Chi^2:            ", fitobj.rchi2_min
    l7= "Iterations:               ", fitobj.niter
    l8= "Number of function calls: ", fitobj.nfev
    l9= "Number of free pars.:     ", fitobj.nfree
    l10= "Degrees of freedom:       ", fitobj.dof
    l11= "Number of pegged pars.:   ", fitobj.npegged
    l12= "Covariance matrix:\n", fitobj.covar

    xmin = min(epoch)
    xmax = max(epoch)
    xlen = len(epoch)
    fitx = numpy.linspace(xmin,xmax,xlen)
    
    fity = model(fitobj.params, fitx)
    
    fitPlot(epoch, oc, minType, method,fitx, fity)
    return l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,l11, l12, fitx, fity
    
    

    


