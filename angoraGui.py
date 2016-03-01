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
from massTransferMC import *
from liteLMFit import *
from liteMC import *
from liteCalculations import liteCalcs
from PyQt4.uic import loadUiType

class liteDialog(QtGui.QDialog):
    def __init__(self):
        super(liteDialog, self).__init__()
        uic.loadUi('liteDialog.ui',self)

    def dataTake(self):
        self.userTzero = self.userTzeroText.text()
        self.userPeriod = self.userPeriodText.text()
        self.userA = self.userAText.text()
        self.userEcc = self.userEccText.text()
        self.userOmega = self.userOmegaText.text()
        
        self.stateTzero = self.tzeroFix.isChecked()
        self.statePer = self.pfix.isChecked()
        self.stateA = self.afix.isChecked()
        self.stateEcc = self.efix.isChecked()
        self.statew = self.wfix.isChecked()
        
        self.tzeroMin = self.tzeroLimMin.text()
        self.tzeroMax = self.tzeroLimMax.text()
        self.perMin = self.perLimMin.text()
        self.perMax = self.perLimMax.text()
        self.aMin = self.aLimMin.text()
        self.aMax = self.aLimMax.text()
        self.eMin = self.eLimMin.text()
        self.eMax = self.eLimMax.text()
        self.wMin = self.wLimMin.text()
        self.wMax = self.wLimMax.text()
        
        self.close()
        
        
class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('angora-main.ui', self)
        
        #self.show()
        
    def openLiteDialog(self):
        self.dialog = liteDialog()
        self.dialog.exec_()
        
        
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

        self.globalTzero = tzero

        
        """ Calculation of Datas and plot """
        calcEpoch(tzero,period)
        plot(roundEpoch, oc, minType, method,self.path)
                
        
        for i in range(len(hjd)):
            #print hjd[i]

            self.dataTable.setItem(i,3, QTableWidgetItem(str(epoch[i])))
            self.dataTable.setItem(i,4, QTableWidgetItem(str(roundEpoch[i])))
            self.dataTable.setItem(i,5, QTableWidgetItem(str(oc[i])))

        
    def askSolve(self):
        
        #mass transfer & LM
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
            l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,l11, l12, fitx, fity = fitIt(tzero,period,npOC,npREpoch,weight)
            
            
            self.resultsText.appendPlainText("LM Fit results for Mass Transfer Effect")            
            self.resultsText.appendPlainText(str(l1[0]+"\t"+l1[1]))
            self.resultsText.appendPlainText(str(l2[0]+"\t"+str(l2[1][0])+", "+str(l2[1][1])+", "+str(l2[1][2])))
            self.resultsText.appendPlainText(str(l3[0]+"\t"+str(l3[1][0])+", "+str(l3[1][1])+", "+str(l3[1][2])))
            self.resultsText.appendPlainText(str(l4[0]+"\t"+str(l4[1][0])+", "+str(l4[1][1])+", "+str(l4[1][2])))
            self.resultsText.appendPlainText(str(l5[0]+"\t"+str(l5[1])))
            self.resultsText.appendPlainText(str(l6[0]+"\t"+str(l6[1])))
            self.resultsText.appendPlainText(str(l7[0]+"\t"+str(l7[1])))
            self.resultsText.appendPlainText(str(l8[0]+"\t"+str(l8[1])))
            self.resultsText.appendPlainText(str(l9[0]+"\t"+str(l9[1])))
            self.resultsText.appendPlainText(str(l10[0]+"\t"+str(l10[1])))
            self.resultsText.appendPlainText(str(l11[0]+"\t"+str(l11[1])))
            self.resultsText.appendPlainText(str(l12[0]+"\t"+str(l12[1][0])+"\n\t"+str(l12[1][1])+"\n\t"+str(l12[1][2])))
            self.resultsText.appendPlainText("")            
            self.resultsText.appendPlainText("Epoch"+"\t"+"Fit"+"\t"+"O-C"+"\t"+"Residuals")
            for i in range (len(fity)):
                self.resultsText.appendPlainText(str(fitx[i])+"\t"+str(fity[i])+"\t"+str(npOC[i])+"\t"+str(npOC[i]-fity[i]))
            #print str(deneme.results)
         
        #mass transfer & MCMC
        elif (self.massRBut.isChecked() and self.mcmcCheck.isChecked()):
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
                  
            m = massTransfer()
            
            npOC = np.asarray(oc)
            npREpoch = np.asarray(roundEpoch)
            npWeight = np.asarray(weight)
            m.fitMassMC(tzero,period,npOC,npREpoch,npWeight)
  
        #lite with LM
        elif (self.liteRBut.isChecked() and self.lmCheck.isChecked()):
            weight=[]
            npOC = np.asarray(oc)
            npREpoch = np.asarray(roundEpoch)
            
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
                    
            npWeight = np.asarray(weight)
            liteWindow = liteDialog()
            liteWindow.exec_()
            
            liteParTzero = float(liteWindow.userTzero)
            liteParPer =  float(liteWindow.userPeriod)
            liteParA = float(liteWindow.userA)
            liteParEcc = float(liteWindow.userEcc)
            liteParOmega = float(liteWindow.userOmega)
                   
            
            stateTzero = bool(liteWindow.stateTzero)
            stateP = bool(liteWindow.statePer)
            stateA = bool(liteWindow.stateA)
            stateE = bool(liteWindow.stateEcc)
            stateW = bool(liteWindow.statew)
            
            tzeroLimMin = float(liteWindow.tzeroMin)
            tzeroLimMax = float(liteWindow.tzeroMax)
            perLimMin = float(liteWindow.perMin)
            perLimMax = float(liteWindow.perMax)
            aLimMin = float(liteWindow.aMin)
            aLimMax = float(liteWindow.aMax)
            eLimMin = float(liteWindow.eMin)
            eLimMax = float(liteWindow.eMax)
            wLimMin = float(liteWindow.wMin)
            wLimMax = float(liteWindow.wMax)
                        
            limitations = (stateTzero, stateP, stateA, stateE, stateW, tzeroLimMin, tzeroLimMax, perLimMin, perLimMax, aLimMin, aLimMax, eLimMin, eLimMax, wLimMin, wLimMax)            
            #run liteCalculations.py
            #nuv = liteCalcs(liteParTzero, liteParPer, liteParA, liteParEcc, liteParOmega, npOC,npREpoch,weight)
            #print self.liteParTzero, self.liteParPer, self.liteParA, self.liteParEcc, self.liteParOmega
            #l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,l11, l12, fitx, fity = fitLiteLM(liteParA,liteParEcc,liteParOmega,liteParTzero,liteParPer, npOC,npREpoch,weight, limitations)
             
            l= Lite()             
            l.fitLiteLM(liteParA,liteParEcc,liteParOmega,liteParTzero,liteParPer,npOC,npREpoch,npWeight,limitations)
                         
             
            self.resultsText.appendPlainText("LM Fit results for Mass Transfer Effect")            
            self.resultsText.appendPlainText(str(l1[0]+"\t"+l1[1]))
            self.resultsText.appendPlainText(str(l2[0]+"\t"+str(l2[1][0])+", "+str(l2[1][1])+", "+str(l2[1][2])+", "+str(l2[1][3])+", "+str(l2[1][4])))
            self.resultsText.appendPlainText(str(l3[0]+"\t"+str(l3[1][0])+", "+str(l3[1][1])+", "+str(l3[1][2])+", "+str(l3[1][3])+", "+str(l3[1][4])))
            self.resultsText.appendPlainText(str(l4[0]+"\t"+str(l4[1][0])+", "+str(l4[1][1])+", "+str(l4[1][2])+", "+str(l4[1][3])+", "+str(l4[1][4])))
            self.resultsText.appendPlainText(str(l5[0]+"\t"+str(l5[1])))
            self.resultsText.appendPlainText(str(l6[0]+"\t"+str(l6[1])))
            self.resultsText.appendPlainText(str(l7[0]+"\t"+str(l7[1])))
            self.resultsText.appendPlainText(str(l8[0]+"\t"+str(l8[1])))
            self.resultsText.appendPlainText(str(l9[0]+"\t"+str(l9[1])))
            self.resultsText.appendPlainText(str(l10[0]+"\t"+str(l10[1])))
            self.resultsText.appendPlainText(str(l11[0]+"\t"+str(l11[1])))
            self.resultsText.appendPlainText(str(l12[0]+"\t"+str(l12[1][0])+"\n\t"+str(l12[1][1])+"\n\t"+str(l12[1][2])))
            self.resultsText.appendPlainText("")            
            self.resultsText.appendPlainText("Epoch"+"\t"+"Fit"+"\t"+"O-C"+"\t"+"Residuals")
            for i in range (len(fity)):
                self.resultsText.appendPlainText(str(fitx[i])+"\t"+str(fity[i])+"\t"+str(npOC[i])+"\t"+str(npOC[i]-fity[i]))
            #print str(deneme.results)
            
        #lite monte-carlo method    
        elif (self.liteRBut.isChecked() and self.mcmcCheck.isChecked()):
            weight = []
                        
            npOC = np.asarray(oc)
            npREpoch = np.asarray(roundEpoch)
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
                   
            npWeight = np.asarray(weight)       
            liteWindow = liteDialog()
            liteWindow.exec_()
            
            liteParTzero = float(liteWindow.userTzero)
            liteParPer =  float(liteWindow.userPeriod)
            liteParA = float(liteWindow.userA)
            liteParEcc = float(liteWindow.userEcc)
            liteParOmega = float(liteWindow.userOmega)
            
            stateTzero = bool(liteWindow.stateTzero)
            stateP = bool(liteWindow.statePer)
            stateA = bool(liteWindow.stateA)
            stateE = bool(liteWindow.stateEcc)
            stateW = bool(liteWindow.statew)
#            
            limitations = (stateTzero, stateP, stateA, stateE, stateW)            
            
            #run liteCalculations.py
            #nuv = liteCalcs(liteParTzero, liteParPer,liteParEcc,npOC,npREpoch,weight)
            
            l= Lite()             
            l.fitLiteLM(liteParA,liteParEcc,liteParOmega,liteParTzero,liteParPer,npOC,npREpoch,npWeight,limitations)
            
            
            
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
    main = MyWindow()
    
    main.show()
    sys.exit(app.exec_())