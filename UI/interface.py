# -*- coding: UTF-8 -*-
import os
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QMessageBox, QTreeWidgetItem, QFileDialog
from qgis.gui import QgsMapToolEmitPoint, QgsVertexMarker
from qgis.utils import iface
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsVectorLayer, QgsGeometry, QgsPoint, QgsRectangle, QgsMapLayer
from ..auxiliar.rectanglemaptool import RectangleMapTool # @UnresolvedImport
from ..auxiliar.geometrymaptool import GeometryMapTool # @UnresolvedImport
import math

GUI, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'window.ui'))

class Interface(QtGui.QDockWidget, GUI):
    def __init__(self, canvas, aux):
        super(Interface, self).__init__()
        self.setupUi(self)
        self.canvas = canvas
        self.auxiliar = aux
        self.initVariables()
        self.initSignals()
        self.widget().setMinimumSize(QSize(262,200))
        self.iface = iface
    
    def initVariables(self):
        self.myToolBox = RectangleMapTool(self.canvas)
        self.myToolGeom = GeometryMapTool(self.canvas)
        self.currentTool = self.canvas.mapTool()
        
    def initSignals(self):
        self.boxButton.clicked.connect(self.getFromBox)
        self.geometryButton.clicked.connect(self.getFromGeometry)
        self.myToolBox.boxCreated.connect(self.doWorkBox)
        self.myToolGeom.geometrySelected.connect(self.doWorkGeom)
        self.canvas.mapToolSet.connect(self.verifyTool)
        self.txtButton.clicked.connect(self.exportarCartasTxt)
        self.csvButton.clicked.connect(self.exportarCartasCsv)        
        
    def verifyTool(self, tool):
        if tool == self.myToolBox:
            self.geometryButton.setChecked(False)
        elif tool == self.myToolGeom:
            self.boxButton.setChecked(False)
        else:
            self.geometryButton.setChecked(False)
            self.boxButton.setChecked(False)
            self.canvas.setMapTool(tool)
    
    def getFromBox(self, state):
        if state:
            self.cartasList.clear()
            self.auxiliar.openFiles()
            self.geometryButton.setChecked(False)
            self.clearLayersSelections()
            self.canvas.setMapTool(self.myToolBox)
            self.canvas.scene().addItem(self.myToolBox.rubberBand)
        else:
            self.auxiliar.closeFiles()
            self.canvas.unsetMapTool(self.myToolBox)
            self.canvas.scene().removeItem(self.myToolBox.rubberBand)
            self.myToolBox.reset()
    
    def getFromGeometry(self, state):
        if state:
            self.cartasList.clear()
            self.auxiliar.openFiles()
            self.boxButton.setChecked(False)
            self.myToolBox.reset()
            self.canvas.setMapTool(self.myToolGeom)
        else:
            self.auxiliar.closeFiles()
            self.canvas.unsetMapTool(self.myToolGeom)
            self.clearLayersSelections()

    def clearLayersSelections(self):
        layers = self.iface.mapCanvas().layers()
        for l in layers:
            if l.type() == QgsMapLayer.VectorLayer:
                l.setSelectedFeatures([])

    def doWorkBox(self, r):
        if r is not None:
            sup_esq = self.getWGSPoint(QgsPoint(r.xMinimum(), r.yMaximum()))
            sup_dir = self.getWGSPoint(QgsPoint(r.xMaximum(), r.yMaximum()))
            inf_esq = self.getWGSPoint(QgsPoint(r.xMinimum(), r.yMinimum()))
            inf_dir = self.getWGSPoint(QgsPoint(r.xMaximum(), r.yMinimum()))
            
            carta_SupEsq = self.auxiliar.calculaCarta(sup_esq,25)
            carta_InfEsq = self.auxiliar.calculaCarta(inf_esq,25)
            carta_SupDir = self.auxiliar.calculaCarta(sup_dir,25)
            carta_InfDir = self.auxiliar.calculaCarta(inf_dir,25)
            
            folhas25 = {}
            folhas50 = {}
            folhas100 = {}
            folhas250 = {}
            
            centroide_SupEsq = carta_SupEsq[2].center()
            centroide_SupDir = carta_SupDir[2].center()
            centroide_InfEsq = carta_InfEsq[2].center()
            centroide_InfDir = carta_InfDir[2].center()
            
            nStepX = (centroide_SupDir.x() - centroide_SupEsq.x())/0.125
            nStepY = (centroide_SupDir.y() - centroide_InfDir.y())/0.125
            
            nStepX = int(nStepX)
            nStepY = int(nStepY)
            
            for j in range(nStepY+1):
                idxY = centroide_SupEsq.y() - j*0.125
                for i in range(nStepX+1):
                    idxX = centroide_SupEsq.x() + i*0.125
                    pt = QgsPoint(idxX, idxY)
                    carta25  = self.auxiliar.calculaCarta(pt, 25)
                    carta50  = self.auxiliar.calculaCarta(pt, 50)
                    carta100 = self.auxiliar.calculaCarta(pt, 100)
                    carta250 = self.auxiliar.calculaCarta(pt, 250)
                    
                    folhas25[carta25[0]] = carta25[1]
                    folhas50[carta50[0]] = carta50[1]
                    folhas100[carta100[0]] = carta100[1]
                    folhas250[carta250[0]] = carta250[1]
     
            self.fillListBox(folhas25, folhas50, folhas100, folhas250)
            #print folhas25, folhas50, folhas100, folhas250
    
    def doWorkGeom(self, g):
        r = g.boundingBox()
        
        if r is not None:
            sup_esq = QgsPoint(r.xMinimum(), r.yMaximum())
            sup_dir = QgsPoint(r.xMaximum(), r.yMaximum())
            inf_esq = QgsPoint(r.xMinimum(), r.yMinimum())
            inf_dir = QgsPoint(r.xMaximum(), r.yMinimum())
            
            carta_SupEsq = self.auxiliar.calculaCarta(sup_esq,25)
            carta_InfEsq = self.auxiliar.calculaCarta(inf_esq,25)
            carta_SupDir = self.auxiliar.calculaCarta(sup_dir,25)
            carta_InfDir = self.auxiliar.calculaCarta(inf_dir,25)
            
            folhas25 = {}
            folhas50 = {}
            folhas100 = {}
            folhas250 = {}
            
            centroide_SupEsq = carta_SupEsq[2].center()
            centroide_SupDir = carta_SupDir[2].center()
            centroide_InfEsq = carta_InfEsq[2].center()
            centroide_InfDir = carta_InfDir[2].center()
            
            nStepX = (centroide_SupDir.x() - centroide_SupEsq.x())/0.125
            nStepY = (centroide_SupDir.y() - centroide_InfDir.y())/0.125
            
            nStepX = int(nStepX)
            nStepY = int(nStepY)
            
            for j in range(nStepY+1):
                idxY = centroide_SupEsq.y() - j*0.125
                for i in range(nStepX+1):
                    idxX = centroide_SupEsq.x() + i*0.125
                    pt = QgsPoint(idxX, idxY)
                    box = QgsRectangle(idxX-0.125/2, idxY-0.125/2, idxX + 0.125/2, idxY+0.125/2)
                    
                    if g.intersects(box):
                        carta25  = self.auxiliar.calculaCarta(pt, 25)
                        carta50  = self.auxiliar.calculaCarta(pt, 50)
                        carta100 = self.auxiliar.calculaCarta(pt, 100)
                        carta250 = self.auxiliar.calculaCarta(pt, 250)
                        
                        folhas25[carta25[0]] = carta25[1]
                        folhas50[carta50[0]] = carta50[1]
                        folhas100[carta100[0]] = carta100[1]
                        folhas250[carta250[0]] = carta250[1]
            
            self.fillListBox(folhas25, folhas50, folhas100, folhas250)
#            print folhas25, folhas50, folhas100, folhas250
 
    def fillListBox(self, f25, f50, f100, f250):
        self.cartasList.clear()
        
        item25  = QTreeWidgetItem(['1:25.000',''])
        item50  = QTreeWidgetItem(['1:50.000',''])
        item100 = QTreeWidgetItem(['1:100.000',''])
        item250 = QTreeWidgetItem(['1:250.000',''])
        itemNotFound = QTreeWidgetItem([u'Não existentes',''])
        
        self.cartasList.addTopLevelItems([item25, item50, item100, item250, itemNotFound])  
        
        for c in f25.keys():
            if f25[c] != '':
                if f25[c][0] != '-':
                    item = QTreeWidgetItem([c, f25[c]])                                                                
                    item25.addChild(item)
                else:
                    item = QTreeWidgetItem([c,''])
                    itemNotFound.addChild(item)
            else:
                item = QTreeWidgetItem([c,''])
                itemNotFound.addChild(item)
        item25.setExpanded(True)
        
        for c in f50.keys():
            if f50[c] != '':
                if f50[c][0] != '-':
                    item = QTreeWidgetItem([c, f50[c]])                                                                
                    item50.addChild(item)
                else:
                    item = QTreeWidgetItem([c,''])
                    itemNotFound.addChild(item)
            else:
                item = QTreeWidgetItem([c,''])
                itemNotFound.addChild(item)
        item50.setExpanded(True)

        for c in f100.keys():
            if f100[c] != '':
                if f100[c][0] != '-':
                    item = QTreeWidgetItem([c, f100[c]])                                                                
                    item100.addChild(item)
                else:
                    item = QTreeWidgetItem([c,''])
                    itemNotFound.addChild(item)
            else:
                item = QTreeWidgetItem([c,''])
                itemNotFound.addChild(item)
        item100.setExpanded(True)
        
        for c in f250.keys():
            if f250[c] != '':
                if f250[c][0] != '-':
                    item = QTreeWidgetItem([c, f250[c]])
                    item250.addChild(item)
                else:
                    item = QTreeWidgetItem([c,''])
                    itemNotFound.addChild(item)
            else:
                item = QTreeWidgetItem([c,''])
                itemNotFound.addChild(item)
        item250.setExpanded(True)
        
        itemNotFound.setExpanded(True)
        
        if itemNotFound.childCount() == 0:
            self.cartasList.invisibleRootItem().removeChild(itemNotFound)
        
        self.cartasList.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        
#        self.cartasList.expandToDepth(0)

    def getWGSPoint(self, pt):
        crsSrc  = self.canvas.mapRenderer().destinationCrs()
        crsDest = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest)
        wgsPt = coordinateTransformer.transform(pt)
        return wgsPt
    
    def exportarCartasTxt(self):
        fileDlg = QFileDialog()
        filePath = fileDlg.getSaveFileName(None, u"Selecionar arquivo de saída", "", u"Arquivo texto (*.txt)")
        
        if filePath != "" and filePath[-4:].lower() != ".txt":
            filePath += ".txt"
        
        if filePath != "":
            csvFile = open(filePath, 'w')
        
        csvFile.write(u'*********************************************\n')
        csvFile.write(u'* Lista de cartas topográficas de interesse *\n')
        csvFile.write(u'*********************************************\n\n')
        
        itemCount = self.cartasList.invisibleRootItem().childCount()
        for i in range(itemCount):
            currentItem = self.cartasList.invisibleRootItem().child(i)
            if currentItem.text(0) == u"1:25.000":
                csvFile.write(u'1:25.000:\n')
                csvFile.write(u'---------\n\n')
                csvFile.write(u'{0:20} | {1:10}\n'.format(u'Nomenclatura', u'MI/MIR'))
                csvFile.write(u'------------           ------    \n\n')
                
                for j in range(currentItem.childCount()):
                    csvFile.write(u'{0:20} | {1:10}\n'.format(currentItem.child(j).text(0), currentItem.child(j).text(1)))
                
                csvFile.write(u'\n')
                csvFile.write(u'---------------------------------\n\n')
            
            elif currentItem.text(0) == u'1:50.000':
                csvFile.write(u'1:50.000:\n')
                csvFile.write(u'---------\n\n')
                csvFile.write(u'{0:20} | {1:10}\n'.format(u'Nomenclatura', u'MI/MIR'))
                csvFile.write(u'------------           ------    \n\n')
                
                for j in range(currentItem.childCount()):
                    csvFile.write(u'{0:20} | {1:10}\n'.format(currentItem.child(j).text(0), currentItem.child(j).text(1)))
                
                csvFile.write(u'\n')
                csvFile.write(u'---------------------------------\n\n')
            
            elif currentItem.text(0) == u'1:100.000':
                csvFile.write(u'1:100.000:\n')
                csvFile.write(u'----------\n\n')
                csvFile.write(u'{0:20} | {1:10}\n'.format(u'Nomenclatura', u'MI/MIR'))
                csvFile.write(u'------------           ------    \n\n')
                
                for j in range(currentItem.childCount()):
                    csvFile.write(u'{0:20} | {1:10}\n'.format(currentItem.child(j).text(0), currentItem.child(j).text(1)))
                    
                csvFile.write(u'\n')
                csvFile.write(u'---------------------------------\n\n')
            
            elif currentItem.text(0) == u'1:250.000':
                csvFile.write(u'1:250.000:\n')
                csvFile.write(u'----------\n\n')
                csvFile.write(u'{0:20} | {1:10}\n'.format(u'Nomenclatura', u'MI/MIR'))
                csvFile.write(u'------------           ------    \n\n')
                
                for j in range(currentItem.childCount()):
                    csvFile.write(u'{0:20} | {1:10}\n'.format(currentItem.child(j).text(0), currentItem.child(j).text(1)))
                    
        csvFile.close()
    
    def exportarCartasCsv(self):
        fileDlg = QFileDialog()
        filePath = fileDlg.getSaveFileName(None, u"Selecionar arquivo de saída", "", u"Arquivo CSV (*.csv)")
        
        if filePath != "" and filePath[-4:].lower() != ".csv":
            filePath += ".csv"
        
        if filePath != "":
            csvFile = open(filePath, 'w')
        
        csvFile.write(u'Escala;Nomenclatura;MI\n')
        
        itemCount = self.cartasList.invisibleRootItem().childCount()
        for i in range(itemCount):
            currentItem = self.cartasList.invisibleRootItem().child(i)
            for j in range(currentItem.childCount()):
                csvFile.write(u'{};{};{}\n'.format(currentItem.text(0),currentItem.child(j).text(0), currentItem.child(j).text(1)))
            
        csvFile.close()    
    
    def showMessage(self,text):
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setWindowTitle(u"Aviso")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.setText(text)
        self.msgBox.exec_()
    
    def closeMsgBox(self):
        self.msgBox.close()