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

from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
from qgis.core import QgsPoint, QgsRectangle, QGis
from PyQt4.QtCore import pyqtSignal, Qt, SIGNAL

class RectangleMapTool(QgsMapToolEmitPoint):
    
  boxCreated = pyqtSignal(QgsRectangle)
    
  def __init__(self, canvas):
      self.canvas = canvas
      QgsMapToolEmitPoint.__init__(self, self.canvas)
      self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
      self.rubberBand.setBorderColor(Qt.red)
      self.rubberBand.setBrushStyle(Qt.Dense6Pattern)
      self.rubberBand.setColor(Qt.red)
      self.rubberBand.setWidth(1)
      self.reset()

  def reset(self):
      self.startPoint = self.endPoint = None
      self.isEmittingPoint = False
      self.rubberBand.reset(QGis.Polygon)
      
  def canvasPressEvent(self, e):
      self.startPoint = self.toMapCoordinates(e.pos())
      self.endPoint = self.startPoint
      self.isEmittingPoint = True
      self.showRect(self.startPoint, self.endPoint)

  def canvasReleaseEvent(self, e):
      self.isEmittingPoint = False
      r = self.rectangle()
      if r is not None:
        self.boxCreated.emit(r)

  def canvasMoveEvent(self, e):
      if not self.isEmittingPoint:
        return

      self.endPoint = self.toMapCoordinates(e.pos())
      self.showRect(self.startPoint, self.endPoint)

  def showRect(self, startPoint, endPoint):
      self.rubberBand.reset(QGis.Polygon)
      if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
        return

      point1 = QgsPoint(startPoint.x(), startPoint.y())
      point2 = QgsPoint(startPoint.x(), endPoint.y())
      point3 = QgsPoint(endPoint.x(), endPoint.y())
      point4 = QgsPoint(endPoint.x(), startPoint.y())

      self.rubberBand.addPoint(point1, False)
      self.rubberBand.addPoint(point2, False)
      self.rubberBand.addPoint(point3, False)
      self.rubberBand.addPoint(point4, True)    # true to update canvas
      self.rubberBand.show()

  def rectangle(self):
      if self.startPoint is None or self.endPoint is None:
        return None
      elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
        return None

      return QgsRectangle(self.startPoint, self.endPoint)

#  def deactivate(self):
#      super(RectangleMapTool, self).deactivate()
#      self.emit(SIGNAL("deactivated()"))

#  def activate(self):
#      super(RectangleMapTool, self).activate()
#      self.rubberBand.setBorderColor(Qt.red)
#      self.rubberBand.setBrushStyle(Qt.Dense6Pattern)
#      self.rubberBand.setColor(Qt.red)
#      self.rubberBand.setWidth(1)
#      self.emit(SIGNAL("activated()"))
      
      