# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:26:41 2015

@author: CTugTEZ
"""
import numpy as np
from dataLoad import hjd, minType, method

epoch=[]
roundEpoch=[]
oc=[]

def calcEpoch(T0,P):
    #print T, T0, P

    del epoch[:]
    del roundEpoch[:]
    del oc[:]

    """Epoch Calculation"""
    for i in range(len(hjd)):
        result = (hjd[i]-T0)/P
        epoch.append(result)

    """Round Epoch Calculation"""
    for i in range(len(hjd)):
        if (minType[i] == 1 or minType[i] == "p" or minType[i] == "P"):
            roundEpoch.append(np.round(epoch[i]))
        else:
            roundEpoch.append(np.floor(epoch[i])+0.5)

    """O-C Calculation"""
    for i in range(len(hjd)):
        oc.append(hjd[i] - (T0 + (roundEpoch[i]*P)))


    
