# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 14:30:31 2015

@author: ctugtez
"""


from plotting import fitPlot
from dataLoad import minType, method
from PyAstronomy import funcFit as fuf
import numpy as np
import matplotlib.pylab as plt
import pymc
from PyAstronomy import pyasl # Instantiate the solver


class massTransfer(fuf.OneDFit):
    """
        TBD
    """
    def __init__(self):
        fuf.OneDFit.__init__(self, ["a","b","c"])
         
    def evaluate(self, epoch):
        
        a = self["a"]
        b = self["b"]
        c = self["c"]
        
        y = a*epoch**2 + b*epoch + c    
        return y
        
    def fitMassMC(self,tzero,per,npoc,npepoch,weight):
    
        l = massTransfer()

        #l.parameterSummary()
        
#        l["a"] = 0
#        l["b"] = 0
#        l["c"]= 0

################## FIT MCMC #####################################
#        l.thaw(["a","b","c"]) #free parameters
#        l.fit(npepoch,npoc,yerr=weight)
#        
#        X0 = {"a":l["a"],"b":l["b"],"c":l["c"]}
#        Lims = {"a":[-1e-20,1e20],"b":[-1e-20,1e20], "c":[-1e-20,1e20]} 
#        steps = {"a":0.01, "b":0.01,"c":0.1}
#        
#        l.fitMCMC(npepoch, npoc, X0, Lims, steps, yerr=weight, \
#            iter=1000, burn=0, thin=1, \
#            dbfile="mcmcExample.tmp")
#------------------------------------------------------------------
        
        
        # specific limits for MCMC paramters
#        ppa = {}
#        ppa["a"] = pymc.Uniform("a", value=l["a"], lower=-1., \
#                        upper=1.0, doc="Amplitude")
#        ppa["ecc"] = pymc.Uniform("ecc", value=l["ecc"], lower=0., \
#                        upper=1.0, doc="Eccentricity")      
        # Use this for ppa
#        l.fitMCMC(npepoch, npoc, X0, Lims, steps, yerr=weight, \
#            pymcPars=ppa,iter=2500, burn=0, thin=1, \
#            dbfile="mcmcExample.tmp")


##################################################################
                        
######## AUTO FIT is WORKING #####################################                 
#        ranges = {"a":[-1e-20,1e20],"b":[-1e-20,1e20], "c":[-1e-20,1e20]}            
#        l.autoFitMCMC(npepoch, npoc, ranges, yerr=weight, iter=100000, picky=False)
##################################################################
 
######## emcee ################################################### 
        l.thaw(["a","b","c"]) #free parameters
        sampleArgs = {"iters":100000, "burn":200}
        priors = {"a":fuf.FuFPrior("limuniform", lower=-1e-20, upper=1e-20), \
                  "b":fuf.FuFPrior("limuniform", lower=-1e-20, upper=1e-20), \
                  "c":fuf.FuFPrior("limuniform", lower=-1e-20, upper=1e-20)}

        # Note that the filename should end in .emcee. Substitute this filename
        # in the following examples.
        l.fitEMCEE(npepoch, npoc, yerr=weight, sampleArgs=sampleArgs, \
                    dbfile="mcmcTA.emcee", priors=priors)
##################################################################
        
        l.parameterSummary()
        
        model = l.evaluate(npepoch)
        sepoch, fity = zip(*sorted(zip(npepoch, model)))
        
       
        fitPlot(npepoch, npoc, minType, method, sepoch,fity)
        #print l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,l11, l12
        #return l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,l11, l12, fitx, fity
