# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:47:05 2015

@author: CTugTEZ
"""

import matplotlib.pyplot as plt

pvisEpoch = []
pvisCalc = []

pccdEpoch = []
pccdCalc = []

pphoEpoch = []
pphoCalc = []

svisEpoch = []
svisCalc = []

sccdEpoch = []
sccdCalc = []

sphoEpoch = []
sphoCalc = []


def plot(roundEpoch, oc, minType, method,path):
    plt.close()
    
    for i in range (len(minType)):
        if (minType[i] == 1) or (minType[i] == "p") or (minType[i] == "P"):
            if (method[i] == "vis"):
                pvisEpoch.append(roundEpoch[i])
                pvisCalc.append(oc[i])
            elif (method[i] == "pg") :
                pphoEpoch.append(roundEpoch[i])
                pphoCalc.append(oc[i])
            else:
                pccdEpoch.append(roundEpoch[i])
                pccdCalc.append(oc[i])  
                                    
        else:
            if (method[i] == "vis"):
                svisEpoch.append(roundEpoch[i])
                svisCalc.append(oc[i])                    
            elif (method[i] == "pg"):
                sccdEpoch.append(roundEpoch[i])
                sccdCalc.append(oc[i])                    
            else:
                sphoEpoch.append(roundEpoch[i])
                sphoCalc.append(oc[i])
                     
                     
         
    plt.plot(pvisEpoch, pvisCalc, 'b.',label="1. Visual")
    plt.plot(pccdEpoch, pccdCalc, 'b*',label="1. CCD")
    plt.plot(pphoEpoch, pphoCalc, 'b+',label="1. Photometric")
    plt.plot(svisEpoch, svisCalc, 'r.',label="2. Visual")
    plt.plot(sccdEpoch, sccdCalc, 'r*',label="2. CCD")
    plt.plot(sphoEpoch, sphoCalc, 'r+',label="2. Photometric")

    plt.legend(loc=0)   


    plt.grid()
    plt.xlabel("Epoch")
    plt.ylabel("O-C")
    plt.title("O-C Curve of "+path[:-4])
    plt.show()           
 
def fitPlot(roundEpoch, oc, minType, method,fitx, fity):
    plt.close()
    
    for i in range (len(minType)):
        if (minType[i] == 1) or (minType[i] == "p") or (minType[i] == "P"):
            if (method[i] == "vis"):
                pvisEpoch.append(roundEpoch[i])
                pvisCalc.append(oc[i])
            elif (method[i] == "pg") :
                pphoEpoch.append(roundEpoch[i])
                pphoCalc.append(oc[i])
            else:
                pccdEpoch.append(roundEpoch[i])
                pccdCalc.append(oc[i])  
                                    
        else:
            if (method[i] == "vis"):
                svisEpoch.append(roundEpoch[i])
                svisCalc.append(oc[i])                    
            elif (method[i] == "pg"):
                sccdEpoch.append(roundEpoch[i])
                sccdCalc.append(oc[i])                    
            else:
                sphoEpoch.append(roundEpoch[i])
                sphoCalc.append(oc[i])
                     
                     
         
    plt.plot(pvisEpoch, pvisCalc, 'b.',label="1. Visual")
    plt.plot(pccdEpoch, pccdCalc, 'b*',label="1. CCD")
    plt.plot(pphoEpoch, pphoCalc, 'b+',label="1. Photometric")
    plt.plot(svisEpoch, svisCalc, 'r.',label="2. Visual")
    plt.plot(sccdEpoch, sccdCalc, 'r*',label="2. CCD")
    plt.plot(sphoEpoch, sphoCalc, 'r+',label="2. Photometric")
    plt.plot(fitx, fity, "g-", label="Fit Curve")

    plt.legend(loc=0)   


    plt.grid()
    plt.xlabel("Epoch")
    plt.ylabel("O-C")
    #plt.title("O-C Curve of "+path[:-4])
   
    plt.show() 