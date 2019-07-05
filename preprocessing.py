import os
import csv
import qgis.utils
import numpy as np
from osgeo import ogr
from qgis.core import *

class preprocessing():
    def csv_preprocessing(self):
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

        self.reduced_data = data[:,[0,3,4,8,10,]]  #Drop all columns except for declared indices
        self.reduced_data = np.delete(self.reduced_data,[4,18] ,axis=0, )  # Drop rows with empty fields
        
    def fields_to_shapefile(self):
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
        #processing.run('qgis:reprojectlayer', parameter_points)

        ## Parsing SHP file and accessing attributes
        relativeShapeFilePath = "data/shapefiles/lines_32N.shp"
        shpFile = os.path.join(projectPath, relativeShapeFilePath)

        layer = QgsVectorLayer(shpFile, "shape:", "ogr")
        self.layerCopy =  QgsVectorLayer(layer.source(), layer.name(), layer.providerType())

        #####
        # Adding sex field
        #####
        nAttributes = 0
        # First add the required field
        caps = self.layerCopy.dataProvider().capabilities()

        for feature in self.layerCopy.getFeatures():
                nAttributes = len(list(feature))
                break
        if(nAttributes < 2):
            if caps & QgsVectorDataProvider.AddAttributes:
                # We require a String field
                res = self.layerCopy.dataProvider().addAttributes(
                    [QgsField("sex", QVariant.String)])

        # Update to propagate the changes
        self.layerCopy.updateFields()


        # Initiate a variable to hold the attribute values
        updates = {}
        for feature in self.layerCopy.getFeatures():
            for entry in self.reduced_data:
                animalID = feature["name"][15:19]
                if animalID == entry[0]:
                    updates[feature.id()] = {1: str(entry[4])}
        self.layerCopy.dataProvider().changeAttributeValues(updates)
        self.layerCopy.updateFields()

        QgsProject.instance().addMapLayer(self.layerCopy)

        #####
        # Adding deploy_on field
        #####
        nAttributes = 0
        # First add the required field 
        caps = self.layerCopy.dataProvider().capabilities()

        for feature in self.layerCopy.getFeatures():
                nAttributes = len(list(feature))
                break
        if(nAttributes < 3):
            if caps & QgsVectorDataProvider.AddAttributes:
                # We require a String field
                res = self.layerCopy.dataProvider().addAttributes(
                    [QgsField("deploy_on", QVariant.String)])

        # Update to propagate the changes  
        self.layerCopy.updateFields()


        # Initiate a variable to hold the attribute values
        updates = {}
        for feature in self.layerCopy.getFeatures():
            for entry in self.reduced_data:
                animalID = feature["name"][15:19]
                if animalID == entry[0]:
                    updates[feature.id()] = {2: str(entry[1])[:-13]}
        self.layerCopy.dataProvider().changeAttributeValues(updates)
        self.layerCopy.updateFields()

        QgsProject.instance().addMapLayer(self.layerCopy)

        #####
        # Adding deploy_off field
        #####
        nAttributes = 0
        # First add the required field 
        caps = self.layerCopy.dataProvider().capabilities()

        for feature in self.layerCopy.getFeatures():
                nAttributes = len(list(feature))
                break
        if(nAttributes < 4):
            if caps & QgsVectorDataProvider.AddAttributes:
                # We require a String field
                res = self.layerCopy.dataProvider().addAttributes(
                    [QgsField("deploy_off", QVariant.String)])

        # Update to propagate the changes  
        self.layerCopy.updateFields()


        # Initiate a variable to hold the attribute values
        updates = {}
        for feature in self.layerCopy.getFeatures():
            for entry in self.reduced_data:
                animalID = feature["name"][15:19]
                if animalID == entry[0]:
                    updates[feature.id()] = {3: str(entry[2])[:-13]}
        self.layerCopy.dataProvider().changeAttributeValues(updates)
        self.layerCopy.updateFields()

        ######
        # Adding yearly_distance field
        #####
        nAttributes = 0
        # First add the required field 
        caps = self.layerCopy.dataProvider().capabilities()

        for feature in self.layerCopy.getFeatures():
                nAttributes = len(list(feature))
                break
        if(nAttributes < 5):
            if caps & QgsVectorDataProvider.AddAttributes:
                # We require a String field
                res = self.layerCopy.dataProvider().addAttributes(
                    [QgsField("yearly_distance", QVariant.Double)])

        # Update to propagate the changes  
        self.layerCopy.updateFields()


        # Initiate a variable to hold the attribute values
        updates = {}
        for feature in self.layerCopy.getFeatures():
            for entry in self.reduced_data:
                animalID = feature["name"][15:19]
                if animalID == entry[0]:
                    updates[feature.id()] = {4: 0.0}
        self.layerCopy.dataProvider().changeAttributeValues(updates)
        self.layerCopy.updateFields()

        QgsProject.instance().addMapLayer(self.layerCopy)
        
    def delete_empty_features(self):
        caps = self.layerCopy.dataProvider().capabilities()
        deleteFeaturesIds = []
        for feat in self.layerCopy.getFeatures():
            attr = feat.attributes()
            if not attr[1] or not attr[2] or not attr[3]:
                if caps & self.layerCopy.dataProvider().DeleteFeatures:
                    deleteFeaturesIds.append(feat.id())
                
        self.layerCopy.dataProvider().deleteFeatures(deleteFeaturesIds)
        QgsProject.instance().addMapLayer(self.layerCopy)
        
preprocessing = preprocessing()
preprocessing.csv_preprocessing()
preprocessing.fields_to_shapefile()
preprocessing.delete_empty_features()