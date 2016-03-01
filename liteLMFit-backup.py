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

class Lite(fuf.OneDFit):
    """
        TBD
    """
    def __init__(self):
        fuf.OneDFit.__init__(self, ["a","ecc","w","t0","per"])
    
    def kepler(m,ecc,eps):
        e = m
        delta = 0.05
        while np.abs(delta) >= 10**(-eps):
            delta = e - ecc*np.sin(e)-m
            e = e - delta/(1-ecc*np.cos(e))
            kepler = e
            inc = delta
            
            inc = kepler - ecc * np.sin(e)-m
            kepler = kepler - inc/(1-ecc*np.cos(kepler))
    
        return kepler
        
    def f(x, ava, ecc):
        return x-ecc*np.sin(x)-ava    
        
    def evaluate(self, epoch):
        def f(x, ava, ecc):
            return x-ecc*np.sin(x)-ava
        a = self["a"]
        b = self["ecc"]
        c = self["w"]
        d = self["t0"]
        e = self["per"]
       
        aveAn, Ek, tanE, tanv, nuv = [],[],[],[],[]
       
        c = np.deg2rad(c)
        for i in range (len(epoch)):
            result = ((epoch[i]-d)/e)*2*np.pi
            aveAn.append(result)      
    
            #result1 = Lite.kepler(aveAn[i],b,10)
            result1 = newton(f,0.5,args=(aveAn[i],b))
            Ek.append(result1)
    
            result2 = np.tan(Ek[i]/2)
            tanE.append(result2)
    
            result3 = np.sqrt((1+b)/(1-b))*tanE[i]
            tanv.append(result3)
         
            result4 = 2*np.arctan(tanv[i])
            nuv.append(result4)
            
        #print aveAn, Ek, tanE, tanv, nuv
        
        y = (a/(np.sqrt(1-(b**2)*(np.cos(c)**2))))*((1-(b**2))/(1+(b*np.cos(nuv))))*((np.sin(nuv+c))+(b*np.sin(c)))
        
        return y
        
    def fitLiteLM(self,userA,ecc,w,tzero,per,npoc,npepoch,weight, limitations):
    
        l = Lite()

        l.parameterSummary()
        
        l["a"] = userA
        l["ecc"] = ecc
        l["w"]=w
        l["t0"]=tzero
        l["per"]=per
        
        
        l.thaw(["a","ecc","w"]) #free parameters
        
        
        l.fit(npepoch, npoc)
        
        l.parameterSummary()
        
        model = l.evaluate(npepoch)
        
        sepoch, fity = zip(*sorted(zip(npepoch, model)))
        
        plt.plot(sepoch, npoc, 'b.')
        plt.plot(sepoch, fity, 'r--')
        plt.show()
        
        
        
#        xmin = min(npepoch)
#        xmax = max(npepoch)
#        xlen = len(npepoch)
#        fitx = np.linspace(xmin,xmax,xlen)
#        
#        fity = model(fitobj.params, npepoch)
        #k = [0.0227,0.62,0.139626340159546]
        #fity = model(k,nuv)
        
        #print list(epoch)
        #print list(oc)
#        sepoch, fity = zip(*sorted(zip(npepoch, fity)))
#        
#        fitPlot(npepoch, npoc, minType, method, sepoch,fity)
        #print l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,l11, l12
        #return l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,l11, l12, fitx, fity