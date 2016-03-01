# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 01:09:25 2016

@author: ctugtez
"""

#LiTE LM Fit Code of ANGORA

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:03:47 2015

@author: ctugtez
"""

from plotting import fitPlot
from dataLoad import minType, method
from PyAstronomy import funcFit as fuf
import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import newton
import pymc

class Lite(fuf.OneDFit):
    """
        TBD
    """
    def __init__(self):
        fuf.OneDFit.__init__(self, ["a","ecc","w","t0","per"])
         
    def evaluate(self, epoch):
#        def f(x, ava, ecc):
#    
#            return x-ecc*np.sin(x)-ava
            
        def kepler(m,ecc,eps):
            e = np.deg2rad(m)
            delta = 1e-6
            while 1:
                delta = e - ecc*np.sin(e)-m
                e = e - delta/(1.0-ecc*np.cos(e))
                
                if np.abs(delta) <= eps:
                    break
#                kepler = e
#                inc = delta
                
                #np.abs(delta) >= 10**(-eps)
                
#                inc = kepler - ecc * np.sin(e)-m
#                kepler = kepler - inc/(1-ecc*np.cos(kepler))
#        
#                inc = kepler - ecc * np.sin(e)-m
#                kepler = kepler - inc/(1-ecc*np.cos(kepler))
            return e
            
        a = self["a"]
        b = self["ecc"]
        c = self["w"]
        d = self["t0"]
        e = self["per"]
       
        #aveAn, 
        nuv = []
        
        c = np.deg2rad(c)
        for i in range (len(epoch)):
            
            result = ((epoch[i]-d)/e)*2*np.pi
            #aveAn.append(result)      
    
#            result1 = kepler(aveAn[i],b,10)
#            #result1 = newton(f,0.5,args=(aveAn[i],b))
#            Ek.append(result1)
    
            result2 = 2*np.arctan(np.sqrt((1+b)/(1-b))*np.tan(kepler(result,b,10)/2))
            nuv.append(result2)
            
        #print aveAn, Ek, tanE, tanv, nuv
        
        y = (a/(np.sqrt(1-(b**2)*(np.cos(c)**2))))*((1-(b**2))/(1+(b*np.cos(nuv))))*((np.sin(nuv+c))+(b*np.sin(c)))
        
        return y
        
    def fitLiteLM(self,userA,ecc,w,tzero,per,npoc,npepoch,weight,limitations):
    
        l = Lite()

        #l.parameterSummary()
        
        l["a"] = userA
        l["ecc"] = ecc
        l["w"]=w
        l["t0"]=tzero
        l["per"]=per
        freedomPars = []
        
        if limitations[0] == False:
            freedomPars.append("t0")
        if limitations[1] == False:
            freedomPars.append("per")
        if limitations[2] == False:
            freedomPars.append("a")
        if limitations[3] == False:
            freedomPars.append("ecc")
        if limitations[4] == False:
            freedomPars.append("w")

################## FIT MCMC #####################################
#        l.thaw(freedomPars) #free parameters
#        l.fit(npepoch,npoc,yerr=weight)
#        
#        X0 = {"a":l["a"],"ecc":l["ecc"],"w":l["w"], "t0":l["t0"], "per":l["per"]}
#        Lims = {"a":[-10.,10.],"ecc":[-1.,1], "w":[-360.,360.], "t0":[0.,50000.], "per":[0.,100000.]} 
#        steps = {"a":0.01, "ecc":0.01,"w":0.1, "t0":200, "per":500}
#        
#        l.fitMCMC(npepoch, npoc, X0, Lims, steps, yerr=weight, \
#            iter=2500, burn=0, thin=1, \
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
#        ranges = {"a":[-10.,10.],"ecc":[0.,1], "w":[0.,360.], "t0":[0.,50000.], "per":[0.,50000.]}             
#        l.autoFitMCMC(npepoch, npoc, ranges, yerr=weight, iter=1000, picky=False)
##################################################################
 
######## emcee ################################################### 
        l.thaw(freedomPars) #free parameters
        sampleArgs = {"iters":1000, "burn":200}
        priors = {"a":fuf.FuFPrior("limuniform", lower=-10.0, upper=10.), \
                  "ecc":fuf.FuFPrior("limuniform", lower=-1.0, upper=1.), \
                  "w":fuf.FuFPrior("limuniform", lower=-360.0, upper=360.), \
                  "t0":fuf.FuFPrior("limuniform", lower=0.0, upper=50000.), \
                  "per":fuf.FuFPrior("limuniform", lower=0.0, upper=50000.)}

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