# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 12:30:02 2015

@author: CTugTEZ

ANGORA: DESCRIPTION: ANGORA (Analyzing the Period Changes of Eclipsing Binary Stars), 
Çift yıldızların ışık eğrilerinden elde edilen minimum zamanlarının analizini i
çeren bir paket programdır. 

"""


#This is data file loading page. File includes minimum times, observers, filters and methods.

import numpy as np
    
hjd = []
minType = []
method = []
    
def DataLoad(path):

    all_data = np.genfromtxt(path, delimiter='\t', dtype=None, names=('HJD', 'Min Type', 'Method'))
    
    lenData = len(all_data)
    
    del hjd[:]
    del minType[:]
    del method[:]

    
    for i in range(0,lenData,1):
        hjd.append(all_data[i][0])
        minType.append(all_data[i][1])
        method.append(all_data[i][2])
        
        



    #print hjd