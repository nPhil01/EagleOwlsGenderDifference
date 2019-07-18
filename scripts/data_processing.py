import os
import csv
import matplotlib
import qgis.utils
import numpy as np
from osgeo import ogr
from qgis.core import *
from numpy import vstack
from datetime import datetime
import matplotlib.pyplot as plt
#change background-color of plots inside axis
plt.rcParams['axes.facecolor'] = 'ivory'

# Class implementing the prepocessing part of the project
class data_processing():

    def __init__(self):

        # Set global variable data_array to make it accessible to all functions of the class processing
        self.data_array = np.empty([1, 1])


    # Function used to set up layers and requests
    def setup_processing(self, projectPath):

        print("Setting up the processing.")
        try:
            # Setting path to reprojected shapefile from pre processing
            shpFile_lines = os.path.join(projectPath, "data/shapefiles/lines_32N.shp")
            shpFile_points = os.path.join(projectPath, "data/shapefiles/points_32N.shp")

            # Read shapfile
            layer_lines = QgsVectorLayer(shpFile_lines, "shape:", "ogr")
            layer_points = QgsVectorLayer(shpFile_points, "shape:", "ogr")

            # Make layers only containing fe-/male eagle owls
            self.layer_m = QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())
            self.layer_f = QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())
            self.layer_n = QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())

            self.points = QgsVectorLayer(layer_points.source(), layer_points.name(), layer_points.providerType())

            # Build requests to filter for sexes and minimum speed
            request_m = QgsFeatureRequest().setFilterExpression(u'"sex" = \'m\'')
            request_f = QgsFeatureRequest().setFilterExpression(u'"sex" = \'f\'')

            request_points = QgsFeatureRequest().setFilterExpression(u'"speed" > \'5\'')

            # Apply filters to layers
            self.layer_m = self.layer_m.getFeatures(request_m)
            self.layer_f = self.layer_f.getFeatures(request_f)

            self.points = self.points.getFeatures(request_points)

            print("DONE: Setting up the processing.")

        except:
            raise EnvironmentError("Error encountered during set up of the processing.")


    # Function used to calculate average distance traveled yearly and calculate distances between sexes
    def calc_distance_differences(self):

        print("Calculating distance differences.")
        
        try:
            # Initiate variables for sex-based trends
            total_length_m = 0
            total_length_f = 0
            count_m = 0
            count_f = 0

            # Calculate average distances travelled by sex
            # Male
            for feature in self.layer_m:
                attr = feature.attributes()
                # Deploy on and off must be set
                if attr[2] and attr[3]:
                    deploy_on_str = attr[2][:-13]
                    deploy_off_str = attr[3][:-13]
                    deploy_on = datetime.strptime(deploy_on_str, '%Y-%m-%d')
                    deploy_off = datetime.strptime(deploy_off_str, '%Y-%m-%d')
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

                    # Adding entry to field with yearly_distance
                    updates = {}
                    updates[feature.id()] = {4: feat_length_year}
                    self.layer_n.dataProvider().changeAttributeValues(updates)
                    self.layer_n.updateFields()

                    # Female
            for feature in self.layer_f:
                attr = feature.attributes()
                # Deploy on and off must be set
                if attr[2] and attr[3]:
                    deploy_on_str = attr[2][:-13]
                    deploy_off_str = attr[3][:-13]
                    deploy_on = datetime.strptime(deploy_on_str, '%Y-%m-%d')
                    deploy_off = datetime.strptime(deploy_off_str, '%Y-%m-%d')
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

                    # Adding entry to field with yearly_distance
                    updates = {}
                    updates[feature.id()] = {4: feat_length_year}
                    self.layer_n.dataProvider().changeAttributeValues(updates)
                    self.layer_n.updateFields()


            # Printing average per male owl
            if count_m > 0:
                avg_distance_m = total_length_m/count_m
                print("Average yearly distance per male eagle owl is: " + str(round(avg_distance_m, 3)) + " m")
            else:
                avg_distance_m = 0

            # Printing average per female owl
            if count_f > 0:
                avg_distance_f = total_length_f/count_f
                print("Average yearly distance per female eagle owl is: " + str(round(avg_distance_f, 3)) + " m")
            else:
                avg_distance_f = 0

            # Difference
            # Dynamically determine leading sex
            distance_sex = ""
            if avg_distance_f < avg_distance_m:
                distance_sex = "males"
            else:
                distance_sex = "females"
            # Calculate difference
            delta_distance = abs(round(avg_distance_f-avg_distance_m, 3))
            print("Distance difference between sex-based averages is: " + str(round(delta_distance/1000, 3)) + " km, with " + str(distance_sex) + " being in the lead")
        
            print("DONE: Calculating distance differences.")

        except:
            raise EnvironmentError("Error encountered during calculation of distance differences.")


    # Function used to calculate differences in speed and height
    def calculate_height_speed_differences(self, projectPath):

        print("Calculating height and speed differences.")
        try:
            # Define path to CSV within folder structure
            relativeFilePath = "data/csv/eagle_owl.csv"
            # Append file path and project path
            csvPath = os.path.join(projectPath, relativeFilePath)

            # Initiate variables for sex-based height and speed trends
            total_height_m = 0
            total_height_f = 0
            total_speed_m = 0
            total_speed_f = 0
            count_m = 0
            count_f = 0
            index = 0

            # Count numbers of feature in neutral layer
            for feat in self.layer_n.getFeatures():
                index += 1

            # Build numpy array
            owls = np.zeros((index, 4), dtype=int)

            # Reset index
            index = 0
            # Enter names of owls into numpy array
            for feat in self.layer_n.getFeatures():
                owls[index, 0] = feat["name"][15:19]
                index += 1

            # Calculate average height by sex
            ## Male
            for feature in self.points:
                with open(csvPath) as csvfile:
                    data = np.array(list(csv.reader(csvfile, delimiter=",")))

                # Drop all columns except for declared indices
                reduced_data = data[:,[0,3,4,8,10,]]
                reduced_data = np.delete(reduced_data,[4,18] ,axis=0, )
                # Drop rows with empty fields
                for entry in reduced_data:
                    animalID = feature["ind_ident"][15:19]

                    ## Male
                    if animalID == entry[0] and str(entry[4]) == 'm':
                        # Sum height and speed by adding the current one to prior total
                        total_height_m += feature["height"]
                        total_speed_m += feature["speed"]

                        # Initiate variables to keep height and speed per owl
                        feature_height = feature["height"]
                        feature_speed = feature["speed"]

                        # Save values in array
                        for owl in owls:
                            if str(owl[0]) == animalID:
                                owl[1] += feature_height
                                owl[2] += feature_speed
                                owl[3] += 1
                                
                        updates = {}
                        updates[feature.id()] = {5: feature_height}
                        updates[feature.id()] = {6: feature_speed}
                        self.layer_n.dataProvider().changeAttributeValues(updates)
                        self.layer_n.updateFields()

                        count_m += 1

                    ## Female
                    if animalID == entry[0] and str(entry[4]) == 'f':
                        # Sum height and speed by adding the current one to prior total
                        total_height_f += feature["height"]
                        total_speed_f += feature["speed"]

                        # Initiate variables to keep height and speed per owl
                        feature_height = feature["height"]
                        feature_speed = feature["speed"]

                        # Save values in array
                        for owl in owls:
                            if str(owl[0]) == animalID:
                                owl[1] += feature_height
                                owl[2] += feature_speed
                                owl[3] += 1
                                
                        updates = {}
                        updates[feature.id()] = {5: feature_height}
                        updates[feature.id()] = {6: feature_speed}
                        self.layer_n.dataProvider().changeAttributeValues(updates)
                        self.layer_n.updateFields()

                        count_f += 1

            # Update values for average height in layer
            updates = {}
            for feature in self.layer_n.getFeatures():
                for owl in owls:
                    avg_h = owl[1]/owl[3]
                    animalID = feature["name"][15:19]
                    if animalID == str(owl[0]):
                        updates[feature.id()] = {5: str(avg_h)}
            self.layer_n.dataProvider().changeAttributeValues(updates)
            self.layer_n.updateFields()

            # Update values for average speed in layer
            updates = {}
            for feature in self.layer_n.getFeatures():
                for owl in owls:
                    avg_s = owl[2]/owl[3]
                    animalID = feature["name"][15:19]
                    if animalID == str(owl[0]):
                        updates[feature.id()] = {6: str(avg_s)}
            self.layer_n.dataProvider().changeAttributeValues(updates)
            self.layer_n.updateFields()

            # Print average heights 
            if count_m > 0:
                avg_height_m = total_height_m/count_m
                print("Average male flight height: " + str(round(avg_height_m, 3)) + " m")
            if count_f > 0:
                avg_height_f = total_height_f/count_f
                print("Average female flight height: " + str(round(avg_height_f, 3)) + " m")
            else:
                avg_height_m = 0
                avg_speed_m = 0

            # Difference height
            # Dynamically determine leading sex
            height_sex = ""
            if avg_height_f < avg_height_m:
                height_sex = "males"
            else:
                height_sex = "females"
            # Calculate difference in height between sexes
            delta_height = abs(round(avg_height_f - avg_height_m, 3))
            print("Height difference between sex-based averages is: " + str(delta_height) + " m, with " + str(height_sex) + " being in the lead")


            # Print average speed
            if count_m > 0:
                avg_speed_m = total_speed_m/count_m
                print("Average male speed: " + str(round(avg_speed_m, 3)) + " km/h")
            if count_f > 0:
                avg_speed_f = total_speed_f/count_f
                print("Average female speed: " + str(round(avg_speed_f, 3)) + " km/h")
            else:
                avg_height_f = 0
                avg_speed_f = 0

            # Difference speed
            # Dynamically determine leading sex
            speed_sex = ""
            if avg_speed_f < avg_speed_m:
                speed_sex = "males"
            else:
                speed_sex = "females"
            # Calculate difference in height between sexes
            delta_speed = abs(round(avg_speed_f - avg_speed_m, 3))
            print("Speed difference between sex-based averages is: " + str(delta_speed) + " km/h, with " + str(speed_sex) + " being in the lead")

            print("DONE:Calculating height and speed differences.")

        except:
            raise RuntimeError("Error encountered during calculation of height and speed differences.")


    # Function used to populate data arrays, merge them and make predictions
    def prepare_predictions(self):

        print("Preparing predictions.")
        try:
            # Initiate arrays with length equal to number of features
            ID_array = np.arange(self.layer_n.featureCount())
            sex_array = np.empty(self.layer_n.featureCount())
            distance_array = np.empty(self.layer_n.featureCount())
            height_array = np.empty(self.layer_n.featureCount())
            speed_array =np.empty(self.layer_n.featureCount())

            index = 0

            # Fill arrays with attributes
            for feature in self.layer_n.getFeatures():
                attributes = feature.attributes()

                if attributes[1] in ["m"]:
                    sex_array[index] = 0

                if attributes[1] in ["f"]:
                    sex_array[index] = 1

                attributes[4] = (round(float(attributes[4])/1000, 3))

                distance_array[index] =  attributes[4]
                height_array[index] = attributes[5]
                speed_array[index] = attributes[6]

                index += 1

            # Build array containing all statistical data
            self.data_array = vstack((ID_array, sex_array, distance_array, height_array, speed_array))
            ################################
            #  ID0       ID1      ID2      #
            #  sex0      sex1     sex2     #
            #  dis0      dis1     dis2     #
            #  height0   height1  height2  #
            #  speed0    speed1   speed1   #
            ################################


            # Bring data_array into horizontal data format
            self.data_array = np.transpose(self.data_array)
            #########################################
            #  ID0    sex0   dis0  height0  speed0  #
            #  ID1    sex1   dis1  height1  speed1  #
            #  ID2    sex2   dis2  height2  speed2  #
            #########################################

            print("DONE: Preparing predictions.")

        except:
            raise RuntimeError("Error encountered during preparation of predictions.")


    # Function used to calculate linear regression model
    # Source: https://devarea.com/linear-regression-with-numpy/
    def getlinear(self, x, y):

        # Closure function used to calculate regression line
        def inner(x1):
            return m * x1 + b

        # Calculating slope
        m = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) * np.sum(x))
        # Calculating bias
        b = (np.sum(y) - m *np.sum(x)) / len(x)
        return inner


    # Function used to make predicitions and plot them
    def make_predictions(self, x_array, y_array, sex_array, title, x_lab, y_lab, plotID):

        print("Making predicitons.")
        try:
            # Calculate regression line
            predict = self.getlinear(x_array, y_array)

            # Use plotID for multiple plots in different popups
            plt.figure(plotID)
            # Set plot attributes
            plt.suptitle(title)
            plt.ylabel(y_lab)
            plt.xlabel(x_lab)
            # Color code: male = blue, female = red
            colors = ["blue", "red"]

            # Make color coded scatter plot
            plt.scatter(x_array, y_array, c = sex_array, cmap = matplotlib.colors.ListedColormap(colors))
            # Plot everything
            plt.plot(x_array, predict(x_array))

            # Show plot
            plt.show()

        except:
            
            raise RuntimeError("Error encountered during making of predictions.")


    # Auxilliary function used to call make_predicitons() with different parameters
    def predict(self):
        
        print("Predicting.")
        try:
            # Distance
            self.make_predictions(self.data_array[:,0], self.data_array[:,2], self.data_array[:,1], "Average travelled Distance", "ID", "Distance [km]", 1)
            # Height
            self.make_predictions(self.data_array[:,0], self.data_array[:,3], self.data_array[:,1], "Average travelled Height", "ID", "Height [m]", 2)
            # Speed
            self.make_predictions(self.data_array[:,0], self.data_array[:,4], self.data_array[:,1], "Average travelled Speed", "ID", "Speed [km/h]", 3)

            print("DONE: Predicting.")

        except:
            raise RuntimeError("Error encountered during predicting.")
        
    # Function used to export the complete working_layer to data/shapefiles/working_layer
    def export_layer(self, projectPath):
        
        print("Exporting layer.")
        try:
            export_path = os.path.join(projectPath, "data/shapefiles/working_layer.shp")
            layer_writer = QgsVectorFileWriter.writeAsVectorFormat(self.layer_n, export_path, "utf-8", self.layer_n.crs(), "ESRI Shapefile")
        
            print("Layer successfully exported.")
        
        except:
            raise RuntimeError("Error encountered during layer export.")