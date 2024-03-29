import os
import csv
import qgis.utils
import processing
import numpy as np
from osgeo import ogr
from qgis.core import *
from qgis.PyQt.QtCore import *

# Class implementing the prepocessing part of the project
class data_preprocessing():

    # Function used to build relative path and read and pre-process csv file
    def csv_preprocessing(self, projectPath):

        print("Preprocessing CSV file.")
        try: 
            # Path to local csv file
            relativeFilePath = "data/csv/eagle_owl.csv" 
            # Concatenate both to form full path
            csvPath = os.path.join(projectPath, relativeFilePath)

            # Preprocess CSV
            with open(csvPath) as csvfile:
                data = np.array(list(csv.reader(csvfile, delimiter=",")))
            # Drop all columns except for declared indices
            self.reduced_data = data[:,[0,3,4,8,10,]]  
            # Drop rows with empty fields
            self.reduced_data = np.delete(self.reduced_data,[4,18] ,axis=0,)  
            
            print("DONE: Preprocessing CSV file.")
        
        except:
            raise RuntimeError("Error encountered during preprocessing of CSV file.")
    

    # Function used to reproject provided shapefiles to UTM 32N 
    # Allows for proper distance calculations
    def reproject_shapefiles(self, projectPath):
        
        print("Reprojecting shapefiles.")
        try:
            # Reproject data to UTM 32N
            # Define reprojection parameters
            lines_path = os.path.join(projectPath, "data/shapefiles/lines.shp")
            lines_out_path = os.path.join(projectPath, "data/shapefiles/lines_32N.shp")
            parameter_lines = {'INPUT': lines_path, 'TARGET_CRS': 'EPSG:4647', 'OUTPUT': lines_out_path}

            points_path = os.path.join(projectPath, "data/shapefiles/points.shp")
            points_out_path = os.path.join(projectPath, "data/shapefiles/points_32N.shp")
            parameter_points = {'INPUT': points_path, 'TARGET_CRS': 'EPSG:4647','OUTPUT': points_out_path}
        
            # Run reprojection using parameters already defined
            processing.run('qgis:reprojectlayer', parameter_lines)
            processing.run('qgis:reprojectlayer', parameter_points)
            
            print("DONE: Reprojecting shapefiles.")
        
        except:
            raise RuntimeError("Error encountered while reprojecting shapefiles.")


    # Function for adding a new column in a shapefile and filling it with data from the csv file.
    def add_fields_with_value(self, fieldName, fieldIndex, entryIndex): 
        nAttributes = 0
        # First add the required field
        caps = self.layerCopy.dataProvider().capabilities()

        for feature in self.layerCopy.getFeatures():
                nAttributes = len(list(feature))
                break
        if(nAttributes <= fieldIndex):
            if caps & QgsVectorDataProvider.AddAttributes:
                # We require a String field
                res = self.layerCopy.dataProvider().addAttributes(
                    [QgsField(fieldName, QVariant.String)])

        # Update to propagate the changes
        self.layerCopy.updateFields()

        # Initiate a variable to hold the attribute values
        updates = {}
        for feature in self.layerCopy.getFeatures():
            for entry in self.reduced_data:
                animalID = feature["name"][15:19]
                if animalID == entry[0]:
                    updates[feature.id()] = {fieldIndex: str(entry[entryIndex])}
        self.layerCopy.dataProvider().changeAttributeValues(updates)
        self.layerCopy.updateFields()

    # Function for creating an empty column in the shapefile.
    def add_empty_fields(self, fieldName, fieldIndex):
        nAttributes = 0
        # First add the required field 
        caps = self.layerCopy.dataProvider().capabilities()

        for feature in self.layerCopy.getFeatures():
                nAttributes = len(list(feature))
                break
        if(nAttributes <= fieldIndex):
            if caps & QgsVectorDataProvider.AddAttributes:
                # We require a String field
                res = self.layerCopy.dataProvider().addAttributes(
                    [QgsField(fieldName, QVariant.String)])

        # Update to propagate the changes  
        self.layerCopy.updateFields()


    # Function used to add fields to shapefile to enter computated measures
    def add_fields_to_shapefile(self, projectPath):
        
        print("Adding fields to shapefile.")
        try:
            # Parsing SHP file and accessing attributes
            relativeShapeFilePath = "data/shapefiles/lines_32N.shp"
            shpFile = os.path.join(projectPath, relativeShapeFilePath)
            layer = QgsVectorLayer(shpFile, "working_layer", "ogr")
            self.layerCopy =  QgsVectorLayer(layer.source(), layer.name(), layer.providerType())

            # Adding sex field
            self.add_fields_with_value("sex", 1, 4)
            # Adding deploy_on field
            self.add_fields_with_value("deploy_on", 2, 1)
            # Adding deploy_off field
            self.add_fields_with_value("deploy_off", 3, 2)
            # Adding yearly distance field
            self.add_empty_fields("yearly_distance", 4)
            # Adding average height field
            self.add_empty_fields("avg_height", 5)
            # Adding average speed field
            self.add_empty_fields("avg_speed", 6)


            # Add shapefile to project as new layer with edited fields
            QgsProject.instance().addMapLayer(self.layerCopy)

            print("DONE: Adding fields to shapefile.")
        
        except:
            raise RuntimeError("Error encountered while adding fields to shapefile.")


    # Function used to delete entries with missing fields from shapefile
    def delete_empty_features(self):
        
        print("Deleting empty features.")
        try:
            caps = self.layerCopy.dataProvider().capabilities()
            deleteFeaturesIds = []
            for feat in self.layerCopy.getFeatures():
                attr = feat.attributes()
                if not attr[1] or not attr[2] or not attr[3]:
                    if caps & self.layerCopy.dataProvider().DeleteFeatures:
                        deleteFeaturesIds.append(feat.id())
                    
            self.layerCopy.dataProvider().deleteFeatures(deleteFeaturesIds)
            QgsProject.instance().addMapLayer(self.layerCopy)
            
            print("DONE: Deleting empty Features.")
        
        except:
            raise RuntimeError("Error encountered while deleting empty features.")