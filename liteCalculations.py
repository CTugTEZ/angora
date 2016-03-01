# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 00:07:03 2016
@author: ctugtez
"""

# This file makes calculations to use in fit alghoritm

import numpy as np
#from kepler import kepler
import scipy.optimize as optimize

aveAn = []
Ek = []
tanE = []
tanv = []
nuv = []

def f(x, ava, ecc):
    return x-ecc*np.sin(x)-ava



def liteCalcs(tzero,per,ecc,oc,epoch,weights):
    
    del aveAn[:]
    del Ek[:]
    del tanE[:]
    del tanv[:]
    del nuv[:]
    
    #Calculation of average anomaly
    for i in range (len(oc)):
        result = ((epoch[i]-tzero)/per)*2*np.pi
        aveAn.append(result)      

        result1 = optimize.newton(f,0.0,args=(aveAn[i],ecc))
        Ek.append(result1)

        result2 = np.tan(Ek[i]/2)
        tanE.append(result2)

        result3 = np.sqrt((1+ecc)/(1-ecc))*tanE[i]
        tanv.append(result3)

        result4 = 2*np.arctan(tanv[i])
        nuv.append(result4)
    #print epoch
    return nuv