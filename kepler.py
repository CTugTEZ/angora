# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 20:01:35 2014

   solves the equation e - ecc*sin(e) = m for e given an m
   returns a value of e given
   m  -  the 'mean anomaly' in orbit theory
   ecc - the eccentricity of the orbit
   eps - the precision parameter - solution will be
         within 10^-eps of the true value.
         don't set eps above 14, as convergence can't be guaranteed


@author: CTT
"""
import numpy as np

 
def kepler(aveAn, ecc, eps):
 
    
    for i in range(len(aveAn)):
        e = aveAn[i] #first guess
        delta = 0.05 #set delta equal to a dummy value
        
#        while abs(delta) >= 10**(-eps):
#    
#            delta = e - ecc * np.sin(e) - aveAn[i]
#            e = e - delta / (1-ecc*np.cos(e))
            
    #return e