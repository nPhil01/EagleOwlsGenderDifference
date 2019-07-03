import os
import csv
import qgis.utils
import numpy as np
from osgeo import ogr
from qgis.core import *

#import processing

#csvPath = "./eagle_owl_csv/eagle_owl.csv"
csvPath = "/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO-reference-data.csv"

##Preprocess CSV
with open(csvPath) as csvfile:
    data = np.array(list(csv.reader(csvfile, delimiter=",")))


reduced_data = data[:,[0,3,8,10,]]  #Drop all columns except for declared indices
reduced_data = np.delete(reduced_data,[4,18] ,axis=0, )  # Drop rows with empty fields

## Reproject data to UTM 32N
## Define reprojection parameters
parameter_lines = {'INPUT': '/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/lines.shp', 'TARGET_CRS': 'EPSG:4647',
    	    'OUTPUT': '/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/lines_32N.shp'}
parameter_points = {'INPUT': '/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/points.shp', 'TARGET_CRS': 'EPSG:4647',
    	    'OUTPUT': '/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/points_32N.shp'}

## Run reprojection
processing.run('qgis:reprojectlayer', parameter_lines)
processing.run('qgis:reprojectlayer', parameter_points)

##Parsing SHP file and accessing attributes
#shpFile = "./eagle_owl_shp/lines.shp"
shpFile = "/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/lines_32N.shp"
layer = QgsVectorLayer(shpFile, "shape:", "ogr")
layerCopy =  QgsVectorLayer(layer.source(), layer.name(), layer.providerType())
nAttributes = 0
# First add the required field 
caps = layerCopy.dataProvider().capabilities()

for feature in layerCopy.getFeatures():
        nAttributes = len(list(feature))
        break
if(nAttributes < 2):
    if caps & QgsVectorDataProvider.AddAttributes:
        # We require a String field
        res = layerCopy.dataProvider().addAttributes(
            [QgsField("sex", QVariant.String)])

# Update to propagate the changes  
layerCopy.updateFields()


# Initiate a variable to hold the attribute values
updates = {}
for feature in layerCopy.getFeatures():
    print(len(list(feature)))
    for entry in reduced_data:
        animalID = feature["name"][15:19]
        if animalID == entry[0]:
            updates[feature.id()] = {1: str(entry[3])}
            print(feature.id(), (entry[3]))
layerCopy.dataProvider().changeAttributeValues(updates)
layerCopy.updateFields()

QgsProject.instance().addMapLayer(layerCopy)