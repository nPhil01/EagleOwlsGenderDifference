import os
import csv
import qgis.utils
import numpy as np
from osgeo import ogr
from qgis.core import *

## Make relative paths available
# Takes path of the finalAssignment qgis project
projectPath =  QgsProject.instance().fileName()
# Removes finalAssignment.gqz from project Path
projectPath = projectPath[:-19]
relativeFilePath = "data/csv/eagle_owl.csv"
csvPath = os.path.join(projectPath, relativeFilePath)


## Preprocess CSV
with open(csvPath) as csvfile:
    data = np.array(list(csv.reader(csvfile, delimiter=",")))

reduced_data = data[:,[0,3,4,8,10,]]  #Drop all columns except for declared indices
reduced_data = np.delete(reduced_data,[4,18] ,axis=0, )  # Drop rows with empty fields

## Reproject data to UTM 32N
## Define reprojection parameters
lines_path = os.path.join(projectPath, "data/shapefiles/lines.shp")
lines_out_path = os.path.join(projectPath, "data/shapefiles/lines_32N.shp")
parameter_lines = {'INPUT': lines_path, 'TARGET_CRS': 'EPSG:4647', 'OUTPUT': lines_out_path}

points_path = os.path.join(projectPath, "data/shapefiles/points.shp")
points_out_path = os.path.join(projectPath, "data/shapefiles/points_32N.shp")
parameter_points = {'INPUT': points_path, 'TARGET_CRS': 'EPSG:4647','OUTPUT': points_out_path}

## Run reprojection
processing.run('qgis:reprojectlayer', parameter_lines)
processing.run('qgis:reprojectlayer', parameter_points)

## Parsing SHP file and accessing attributes
relativeShapeFilePath = "data/shapefiles/lines.shp"
shpFile = os.path.join(projectPath, relativeFilePath)

#shpFile = "/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/lines_32N.shp"
layer = QgsVectorLayer(shpFile, "shape:", "ogr")
layerCopy =  QgsVectorLayer(layer.source(), layer.name(), layer.providerType())

#####
# Adding sex field
#####
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
    for entry in reduced_data:
        animalID = feature["name"][15:19]
        if animalID == entry[0]:
            updates[feature.id()] = {1: str(entry[4])}
layerCopy.dataProvider().changeAttributeValues(updates)
layerCopy.updateFields()

QgsProject.instance().addMapLayer(layerCopy)

#####
# Adding deploy_on field
#####
nAttributes = 0
# First add the required field 
caps = layerCopy.dataProvider().capabilities()

for feature in layerCopy.getFeatures():
        nAttributes = len(list(feature))
        break
if(nAttributes < 3):
    if caps & QgsVectorDataProvider.AddAttributes:
        # We require a String field
        res = layerCopy.dataProvider().addAttributes(
            [QgsField("deploy_on", QVariant.String)])

# Update to propagate the changes  
layerCopy.updateFields()


# Initiate a variable to hold the attribute values
updates = {}
for feature in layerCopy.getFeatures():
    for entry in reduced_data:
        animalID = feature["name"][15:19]
        if animalID == entry[0]:
            updates[feature.id()] = {2: str(entry[1])[:-13]}
layerCopy.dataProvider().changeAttributeValues(updates)
layerCopy.updateFields()

QgsProject.instance().addMapLayer(layerCopy)

#####
# Adding deploy_off field
#####
nAttributes = 0
# First add the required field 
caps = layerCopy.dataProvider().capabilities()

for feature in layerCopy.getFeatures():
        nAttributes = len(list(feature))
        break
if(nAttributes < 4):
    if caps & QgsVectorDataProvider.AddAttributes:
        # We require a String field
        res = layerCopy.dataProvider().addAttributes(
            [QgsField("deploy_off", QVariant.String)])

# Update to propagate the changes  
layerCopy.updateFields()


# Initiate a variable to hold the attribute values
updates = {}
for feature in layerCopy.getFeatures():
    for entry in reduced_data:
        animalID = feature["name"][15:19]
        if animalID == entry[0]:
            updates[feature.id()] = {3: str(entry[2])[:-13]}
layerCopy.dataProvider().changeAttributeValues(updates)
layerCopy.updateFields()

QgsProject.instance().addMapLayer(layerCopy)
