import processing
from qgis.core import *
from datetime import datetime


class data_processing():
    def processing_setup(self):
        # setting path to reprojected shapefile from pre processing
        shpFile_lines = "/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/lines_32N.shp"
        shpFile_points = "/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/points_32N.shp"

        # read shapfile
        layer_lines = QgsVectorLayer(shpFile_lines, "shape:", "ogr")
        layer_points = QgsVectorLayer(shpFile_points, "shape:", "ogr")

        # make layers only containing fe/-male eagle owls 
        self.layer_m =  QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())
        self.layer_f =  QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())
        
        self.points_m = QgsVectorLayer(layer_points.source(), layer_points.name(), layer_points.providerType())
        self.points_f = QgsVectorLayer(layer_points.source(), layer_points.name(), layer_points.providerType())

        # build requests to filter for sexes
        request_m = QgsFeatureRequest().setFilterExpression(u'"sex" = \'m\'') 
        request_f = QgsFeatureRequest().setFilterExpression(u'"sex" = \'f\'') 

        # apply filters to layers
        self.layer_m = self.layer_m.getFeatures(request_m)
        self.layer_f = self.layer_f.getFeatures(request_f)

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
                
        if count_f > 0:
            avg_distance_f = total_length_f/count_f
            print("Die Durchschnittliche Distanz der Weibchen pro Jahr ist: " + str(avg_distance_f))
        else:
            avg_distance_f = 0

        # difference
        delta_distance = abs(round(avg_distance_f-avg_distance_m, 3))
        print("Difference between sex-based averages is: " +str(delta_distance) + "km")        

pro = data_processing()
pro.processing_setup()
pro.calc_distance_differences()
