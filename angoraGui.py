# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 01:26:17 2015

@author: CTugTEZ
"""

import sys
from PyQt4 import QtGui, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import * 
from dataLoad import *
from calcs import *
from plotting import *
from massTransfer import *

        
class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('angora-main.ui', self)
        self.show()
        
    def dataLoadGui(self):
        
        self.dataPathLine.setText(QFileDialog.getOpenFileName())
        self.path = self.dataPathLine.text()
        self.path = self.path.split("/")      
        self.path = str(self.path[-1])
        
        DataLoad(self.path)
        
        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(6)
        self.dataTable.setRowCount(len(hjd))
        baslik="HJD;Minimum type;Method;Epoch;Rounded Epoch;O-C"
        self.dataTable.setHorizontalHeaderLabels(baslik.split(";"))
        self.dataTable.setSortingEnabled(True)
            
   
        """ Writing to table """
        for i in range(len(hjd)):
            #print hjd[i]
            self.dataTable.setItem(i,0, QTableWidgetItem(str(hjd[i])))
            self.dataTable.setItem(i,1, QTableWidgetItem(str(minType[i])))
            self.dataTable.setItem(i,2, QTableWidgetItem(str(method[i])))
            
            
            
    def calcPlot(self):
        tzero = float(self.t0Text.text())
        period = float(self.periodText.text())


        
        """ Calculation of Datas and plot """
        calcEpoch(tzero,period)
        plot(roundEpoch, oc, minType, method,self.path)
        
        
        
        for i in range(len(hjd)):
            #print hjd[i]

            self.dataTable.setItem(i,3, QTableWidgetItem(str(epoch[i])))
            self.dataTable.setItem(i,4, QTableWidgetItem(str(roundEpoch[i])))
            self.dataTable.setItem(i,5, QTableWidgetItem(str(oc[i])))
        
    def askSolve(self):
        if (self.massRBut.isChecked() and self.lmCheck.isChecked()):
            weight = []
            
            tzero = float(self.t0Text.text())
            period = float(self.periodText.text())
            ccdW = float(self.ccdWLine.text())
            pgW = float(self.pgWLine.text())
            visW = float(self.visWLine.text())

            for i in range(len(method)):
                if (method[i] == "vis"):
                    weight.append(visW)
                elif (method[i] == "pg"):
                    weight.append(pgW)
                else:
                    weight.append(ccdW)
                   
            
            npOC = np.asarray(oc)
            npREpoch = np.asarray(roundEpoch)
            fitIt(tzero,period,npOC,npREpoch,weight)
         
        elif (self.massRBut.isChecked() and self.mcmcCheck.isChecked()):
            print "bye"
        elif (self.liteRBut.isChecked() and self.lmCheck.isChecked()):
            print "bye"
        elif (self.liteRBut.isChecked() and self.mcmcCheck.isChecked()):
            print "bye"
        elif (self.magneticRBut.isChecked() and self.lmCheck.isChecked()):
            print "bye"
        elif (self.magneticRBut.isChecked() and self.mcmcCheck.isChecked()):
            print "bye"
        elif (self.apsidalRBut.isChecked() and self.lmCheck.isChecked()):
            print "bye"
        elif (self.apsidalRBut.isChecked() and self.mcmcCheck.isChecked()):
            print "bye"
        else:
            QtGui.QMessageBox.warning(self,"Solving Problem","Please select an effect and method!")




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())