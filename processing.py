import processing
from qgis.core import *

shpFile = "C:/Users/Basti/Desktop/owls/lines_32N.shp"
layer = QgsVectorLayer(shpFile, "shape:", "ogr")

layer_m =  QgsVectorLayer(layer.source(), layer.name(), layer.providerType())
layer_f =  QgsVectorLayer(layer.source(), layer.name(), layer.providerType())

request_m = QgsFeatureRequest().setFilterExpression(u'"sex" = \'m\'') 
layer_m = layer_m.getFeatures(request_m)

request_f = QgsFeatureRequest().setFilterExpression(u'"sex" = \'f\'') 
layer_f = layer_f.getFeatures(request_f)


total_length_m = 0
count_m = 0

for feature in layer_m:
    total_length_m += feature.geometry().length()
    count_m += 1
    
avg_distance_m = total_length_m/count_m
print(avg_distance_m)

for feature in layer_f:
    print("f")
