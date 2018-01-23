# -*- coding: UTF-8 -*-

#--------------------------------------------------------------------------#
#                                                                          #
# MapFinder Brasil                                                         #
# Copyright (C) 2018  Diego Benincasa                                      #
# Contact: diego@diegobenincasa.com                                        #
# Feel free to contact if you find any bugs or improvement possibilities.  #
#                                                                          #
#--------------------------------------------------------------------------#
#                                                                          #
# Licensed under the terms of GNU GPL 2                                    #
#                                                                          #
# This program is free software; you can redistribute it and/or modify     #
# it under the terms of the GNU General Public License as published by     #
# the Free Software Foundation; either version 2 of the License, or        #
# (at your option) any later version.                                      #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the             #
# GNU General Public License for more details.                             #
#                                                                          #
# You should have received a copy of the GNU General Public License along  #
# with this program; if not, write to the Free Software Foundation, Inc.,  #
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.              #
#                                                                          #
#--------------------------------------------------------------------------#


from PyQt4.QtGui import QAction, QIcon, QToolButton, QMenu
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import QMessageBox
from icons import resources_rc
from UI.interface import Interface
from auxiliar.auxiliar import Auxiliar
import math

class Main:
    def __init__(self, iface):
        '''Construtor'''
        self.iface = iface
        self.isOpen = False
        
    def initGui(self):
        #INICIAR VARIÁVEIS E SINAIS
        self.initVariables()
        self.initSignals()
#        self.openWindow()
        self.isOpen = True
        
    def unload(self):
        del self.dockWindow
        del self.toolbar
       
    def initVariables(self):
        #CRIAR ACTIONS
        self.a = QAction(QIcon(":/plugins/MapFinder/icons/main.png"), u'Buscar cartas', self.iface.mainWindow()) 
        self.a.setCheckable(True)

        self.toolbar = self.iface.addToolBar(u'MapFinder Brasil')
        self.toolbar.addAction(self.a)
        
        #OUTRAS VARIAVEIS
        self.msgBox = QMessageBox()
        self.canvas = self.iface.mapCanvas()
        self.auxiliar = Auxiliar(self.iface)
        self.dockWindow = Interface(self.canvas, self.auxiliar)

    def initSignals(self):
        self.a.triggered.connect(self.openWindow)
        self.dockWindow.closeEvent = self.closeDock
    
    def initPlugin(self):
        pass
    
    def openWindow(self, b = True):
        if(b):
            self.iface.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockWindow)
            self.isOpen = True
        else:
            self.dockWindow.boxButton.setChecked(False)
            self.dockWindow.geometryButton.setChecked(False)
            self.dockWindow.close()
            
    def closeDock(self, e):
        #del self.dockWindow
        self.isOpen = False
        self.a.setChecked(False)
        try:
            self.canvas.unsetMapTool(self.dockWindow.currentTool)
        except:
            pass
        try:
            self.canvas.scene().removeItem(self.dockWindow.myToolBox.rubberBand)
        except:
            pass
        try:
            self.canvas.scene().removeItem(self.dockWindow.myToolGeom.rubberBand)
        except:
            pass


    def closeWindow(self, e):
        pass

    def showMessage(self, text):
        self.msgBox.setIcon(QMessageBox.Critical)
        self.msgBox.setWindowTitle("Erro")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.setText(text)
        self.msgBox.exec_()
            
    def closeMsgBox(self, b):
        self.msgBox.close()
        
    