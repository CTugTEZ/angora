# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:45:11 2015

@author: ctugtez
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

import random

class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        hBoxLayout1 = QtGui.QHBoxLayout()
        hBoxLayout2 = QtGui.QHBoxLayout()
        hBoxLayout3 = QtGui.QHBoxLayout()
        hBoxLayoutB = QtGui.QHBoxLayout()
        
        vBoxLayout1 = QtGui.QVBoxLayout()
        
        hBoxLayout1r = QtGui.QHBoxLayout()
        hBoxLayout2r = QtGui.QHBoxLayout()
        hBoxLayout3r = QtGui.QHBoxLayout()
        
        vBoxLayout2 = QtGui.QVBoxLayout()
        
        #frames
        topleft = QtGui.QFrame(self)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
        
        topleft1 = QtGui.QFrame(self)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
        
        topleft2 = QtGui.QFrame(self)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
        
        topleft3 = QtGui.QFrame(self)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
        
        
 
        topright = QtGui.QFrame(self)
        topright.setFrameShape(QtGui.QFrame.StyledPanel)
        topright1 = QtGui.QFrame(self)
        topright.setFrameShape(QtGui.QFrame.StyledPanel)
        topright2 = QtGui.QFrame(self)
        topright.setFrameShape(QtGui.QFrame.StyledPanel)
        topright3 = QtGui.QFrame(self)
        topright.setFrameShape(QtGui.QFrame.StyledPanel)

        bottom = QtGui.QFrame(self)
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        
        
        #buttons 
        loadBut = QtGui.QPushButton(topleft)
        loadBut.setText("Choose File")

        calcPlotBut = QtGui.QPushButton(topleft)
        calcPlotBut.setText("Calculate and Plot")
        calcPlotBut.clicked.connect(self.plot)
        
        #labels        
        tzeroLbl = QtGui.QLabel(topleft)
        tzeroLbl.setText("T0:")
        
        periodLbl = QtGui.QLabel(topleft)
        periodLbl.setText("Period:")
        
        #textlines
        fileText = QtGui.QLineEdit(self)  
        tzeroText = QtGui.QLineEdit(self)
        periodText = QtGui.QLineEdit(self)      
        
        #table
        dataTable = QtGui.QTableWidget(self)
        
        #plot
        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Just some button connected to `plot` method
      
       
        
        
        # set the layout
        layout = QtGui.QGridLayout()
                
        hBoxLayout1.addWidget(loadBut)
        hBoxLayout1.addWidget(fileText)
        topleft1.setFixedSize(300,50)
        topleft1.setLayout(hBoxLayout1)
        
        hBoxLayout2.addWidget(tzeroLbl)
        hBoxLayout2.addWidget(tzeroText)
        topleft2.setFixedSize(300,50)
        topleft2.setLayout(hBoxLayout2)
        
        hBoxLayout3.addWidget(periodLbl)
        hBoxLayout3.addWidget(periodText)
        topleft3.setFixedSize(300,50)
        topleft3.setLayout(hBoxLayout3)
        
        vBoxLayout1.addWidget(topleft1)
        vBoxLayout1.addWidget(topleft2)
        vBoxLayout1.addWidget(topleft3)
        topleft.setFixedSize(320,150)
        topleft.setLayout(vBoxLayout1)
        
        
        hBoxLayout1r.addWidget(calcPlotBut)
        topright1.setFixedSize(400,50)
        topright1.setLayout(hBoxLayout1r)
        
        hBoxLayout2r.addWidget(self.toolbar)
        topright2.setFixedSize(400,50)
        topright2.setLayout(hBoxLayout2r)
        
        hBoxLayout3r.addWidget(self.canvas)
        topright3.setFixedSize(400,200)
        topright3.setLayout(hBoxLayout3r)
        
        vBoxLayout2.addWidget(topright1)
        vBoxLayout2.addWidget(topright2)
        vBoxLayout2.addWidget(topright3)
        topright.setFixedSize(600,500)
        topright.setLayout(vBoxLayout2)
        
        hBoxLayoutB.addWidget(dataTable)
        bottom.setFixedSize(900,100)        
        bottom.setLayout(hBoxLayoutB)
        

#        hBoxLayout.addWidget(periodLbl)
#        hBoxLayout.addWidget(periodText)
#        
#        topleft3.setFixedSize(300,50)
#        topleft3.setLayout(hBoxLayout)
        
#        layout.addWidget(calcPlotBut,2,3)
#        
#        layout.addWidget(dataTable,3,0)
        
        layout.addWidget(topleft,0,0)
        layout.addWidget(topright,0,1)
        layout.addWidget(bottom)

        
        
        self.setGeometry(0, 0, 900, 600)
        self.setLayout(layout)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())