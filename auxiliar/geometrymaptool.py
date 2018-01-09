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
    found_features = self.identify(event.x(), event.y(), QgsMapToolIdentify.TopDownStopAtFirst, self.VectorLayer)
    
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
    
        