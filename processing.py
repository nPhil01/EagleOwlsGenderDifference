import os
import csv
import qgis.utils
import numpy as np
from numpy import vstack
import matplotlib as plt
import matplotlib.pyplot
from osgeo import ogr
from qgis.core import *
from datetime import datetime


class data_processing():
    
    def processing_setup(self):
        ## Make relative paths available
        # Takes path of the finalAssignment qgis project
        projectPath =  QgsProject.instance().fileName()
        # Removes finalAssignment.gqz from project Path
        projectPath = projectPath[:-19]

        # setting path to reprojected shapefile from pre processing
        shpFile_lines = os.path.join(projectPath, "data/shapefiles/lines_32N.shp")
        shpFile_points = os.path.join(projectPath, "data/shapefiles/points_32N.shp")

        # read shapfile
        layer_lines = QgsVectorLayer(shpFile_lines, "shape:", "ogr")
        layer_points = QgsVectorLayer(shpFile_points, "shape:", "ogr")

        # make layers only containing fe-/male eagle owls 
        self.layer_m = QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())
        self.layer_f = QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())
        self.layer_n = QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())
        
        self.points = QgsVectorLayer(layer_points.source(), layer_points.name(), layer_points.providerType())

        # build requests to filter for sexes
        request_m = QgsFeatureRequest().setFilterExpression(u'"sex" = \'m\'') 
        request_f = QgsFeatureRequest().setFilterExpression(u'"sex" = \'f\'') 
        
        request_points = QgsFeatureRequest().setFilterExpression(u'"speed" > \'5\'')

        # apply filters to layers
        self.layer_m = self.layer_m.getFeatures(request_m)
        self.layer_f = self.layer_f.getFeatures(request_f)
        
        self.points = self.points.getFeatures(request_points)


    def calc_distance_differences(self):
        # initiate variables for sex-based trends 
        total_length_m = 0
        total_length_f = 0
        count_m = 0
        count_f = 0

        #calculate average distances travelled by sex 
        # male
        for feature in self.layer_m:
            attr = feature.attributes()
            # Deploy on and off must be set
            if attr[2] and attr[3]:
                deploy_on = datetime.strptime(attr[2], '%Y-%m-%d')
                deploy_off = datetime.strptime(attr[3], '%Y-%m-%d')
                # Calculating the number of days of logging
                days = deploy_off - deploy_on
                days = str(days)
                if days[1] == ' ':
                    days = int(days[:1])
                elif days[2] == ' ':
                    days = int(days[:2])
                elif days[3] == ' ':
                    days = int(days[:3])
                elif days[4] == ' ':
                    days = int(days[:4])
                
                # Calculating the distance for a year (365 days)
                feat_length = feature.geometry().length()
                percentage = 100/(100/365*days)
                feat_length_year = feat_length * percentage
                total_length_m += feat_length_year
                count_m += 1

                #adding entry to field with yearly_distance
                updates = {}
                updates[feature.id()] = {4: feat_length_year}
                self.layer_n.dataProvider().changeAttributeValues(updates)
                self.layer_n.updateFields()
                        
        
        if count_m > 0:
            avg_distance_m = total_length_m/count_m
            print("Die Durchschnittliche Distanz der Männchen pro Jahr ist: " + str(avg_distance_m))
        else:
            avg_distance_m = 0

        # female 
        for feature in self.layer_f:
            attr = feature.attributes()
            # Deploy on and off must be set
            if attr[2] and attr[3]:
                deploy_on = datetime.strptime(attr[2], '%Y-%m-%d')
                deploy_off = datetime.strptime(attr[3], '%Y-%m-%d')
                # Calculating the number of days of logging
                days = deploy_off - deploy_on
                days = str(days)
                if days[1] == ' ':
                    days = int(days[:1])
                elif days[2] == ' ':
                    days = int(days[:2])
                elif days[3] == ' ':
                    days = int(days[:3])
                elif days[4] == ' ':
                    days = int(days[:4])
                
                # Calculating the distance for a year (365 days)
                feat_length = feature.geometry().length()
                percentage = 100/(100/365*days)
                feat_length_year = feat_length * percentage
                total_length_f += feat_length_year
                count_f += 1

                #adding entry to field with yearly_distance
                updates = {}
                updates[feature.id()] = {4: feat_length_year}
                self.layer_n.dataProvider().changeAttributeValues(updates)
                self.layer_n.updateFields()
                
        if count_f > 0:
            avg_distance_f = total_length_f/count_f
            print("Die Durchschnittliche Distanz der Weibchen pro Jahr ist: " + str(avg_distance_f))
        else:
            avg_distance_f = 0

        # difference
        delta_distance = abs(round(avg_distance_f-avg_distance_m, 3))
        print("Distance difference between sex-based averages is: " +str(delta_distance) + "km")


    def calc_height_speed_differences(self):

        ## Make relative paths available
        # Takes path of the finalAssignment qgis project
        projectPath =  QgsProject.instance().fileName()
        # Removes finalAssignment.gqz from project Path
        projectPath = projectPath[:-19]
        relativeFilePath = "data/csv/eagle_owl.csv"
        csvPath = os.path.join(projectPath, relativeFilePath)

        # initiate variables for sex-based height trends 
        total_height_m = 0
        total_height_f = 0
        total_speed_m = 0
        total_speed_f = 0
        count_m = 0
        count_f = 0
        
        #calculate average height by sex 
        # male
        for feature in self.points:
            with open(csvPath) as csvfile:
                data = np.array(list(csv.reader(csvfile, delimiter=",")))
                
            reduced_data = data[:,[0,3,4,8,10,]]  # Drop all columns except for declared indices
            reduced_data = np.delete(reduced_data,[4,18] ,axis=0, )  # Drop rows with empty fields
            for entry in reduced_data:
                animalID = feature["ind_ident"][15:19]
                # male
                if animalID == entry[0] and str(entry[4]) == 'm':
                    total_height_m += feature["height"]
                    total_speed_m += feature["speed"]

                    feature_height = feature["height"]
                    feature_speed = feature["speed"]

                    #adding entry to field with height and speed
                    updates = {}
                   
                   ######### Hier müssten die Werte zu layerCopy/working_layer weitergegeben werden
                   ######### Ziel: Alle werte in einer Tabelle
                    updates[feature.id()] = {5: feature_height}
                    updates[feature.id()] = {6: feature_speed}
                    self.layer_n.dataProvider().changeAttributeValues(updates)
                    self.layer_n.updateFields()
                    
                    count_m += 1
                    print("male: " + str(count_m))
                    
                if animalID == entry[0] and str(entry[4]) == 'f':
                    total_height_f += feature["height"]
                    total_speed_f += feature["speed"]

                    feature_height = feature["height"]
                    feature_speed = feature["speed"]

                    #adding entry to field with height and speed
                    updates = {}

                    ######### Hier müssten die Werte zu layerCopy/working_layer weitergegeben werden
                    ######### Ziel: Alle werte in einer Tabelle
                    updates[feature.id()] = {5: feature_height}
                    updates[feature.id()] = {6: feature_speed}
                    self.layer_n.dataProvider().changeAttributeValues(updates)
                    self.layer_n.updateFields()

                    count_f += 1
                    print("female: " + str(count_f))
            
        if count_m > 0:
            avg_height_m = total_height_m/count_m
            print("male height: " + str(avg_height_m))
            avg_speed_m = total_speed_m/count_m
            print("male speed: " + str(avg_speed_m))
        else:
            avg_height_m = 0
            avg_speed_m = 0
        
        if count_f > 0:
            avg_height_f = total_height_f/count_f
            print("female height: " + str(avg_height_f))
            avg_speed_f = total_speed_f/count_f
            print("female speed: " + str(avg_speed_f))
        else:
            avg_height_f = 0
            avg_speed_f = 0
        
        # difference
        delta_height = abs(round(avg_height_f - avg_height_m, 3))
        delta_speed = abs(round(avg_speed_f - avg_speed_m, 3))
        print("Height difference between sex-based averages is: " + str(delta_height) + " m") 
        print("Speed difference between sex-based averages is: " + str(delta_speed) + " km/h")


    # Function used to populate data arrays, merge them and make predictions 
    def make_predictions(self):
        ### Initiate arrays with length equal to number of features
        ID_array = np.arange(self.layer_n.featureCount())
        sex_array = np.empty(self.layer_n.featureCount())
        distance_array = np.empty(self.layer_n.featureCount())
        height_array = np.empty(self.layer_n.featureCount())
        speed_array =np.empty(self.layer_n.featureCount())
        
        index = 0

        ### Fill arrays with attributes
        for feature in self.layer_n.getFeatures():
            attributes = feature.attributes()
            
            sex_array[index] =  attributes[1]
            distance_array[index] = attributes[4]
            height_array[index] = attributes[5]
            speed_array[index] = attributes[6]
            
            index += 1
         
        ### Build array containing all statistical data
        data_array = vstack((ID_array, sex_array, distance_array, height_array, speed_array))
        ################################
        #  ID0       ID1      ID2      #
        #  sex0      sex1     sex2     #
        #  dis0      dis1     dis2     #
        #  height0   height1  height2  #
        #  speed0    speed1   speed1   #
        ################################

        ### Bring data_array into horizontal data format
        data_array = np.transpose(data_array)


pro = data_processing()
pro.processing_setup()
pro.calc_distance_differences()
pro.make_predictions() 
#pro.calc_height_speed_differences()