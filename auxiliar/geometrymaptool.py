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

from qgis.gui import QgsMapToolIdentifyFeature, QgsMapToolIdentify, QgsMapMouseEvent
from qgis.core import QgsRectangle, QgsGeometry, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsMapLayer
from qgis.utils import iface
from PyQt4.QtCore import pyqtSignal

class GeometryMapTool(QgsMapToolIdentifyFeature):
    
    geometrySelected = pyqtSignal(QgsGeometry)
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.iface = iface
        QgsMapToolIdentifyFeature.__init__(self,self.canvas)
    
    def canvasReleaseEvent(self, event):
        event.snapPoint(QgsMapMouseEvent.SnapProjectConfig)
        found_features = self.identify(event.x(), event.y(), QgsMapToolIdentify.ActiveLayer, self.VectorLayer)
    
        layers = self.iface.mapCanvas().layers()
        for l in layers:
            if l.type() == QgsMapLayer.VectorLayer:
                l.setSelectedFeatures([])
    
        if len(found_features) > 0:
            feature = found_features[0].mFeature
            layer = found_features[0].mLayer
            layer.setSelectedFeatures([feature.id()])
            geometry = feature.geometry()
            transformer = QgsCoordinateTransform(layer.crs(), QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId))
            geometry.transform(transformer)
             
            self.geometrySelected.emit(geometry)
    
        