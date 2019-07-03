import processing
from qgis.core import *

def processing_setup():
    # setting path to reprojected shapefile from pre processing
    shpFile_lines = "/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/lines_32N.shp"
    shpFile_points = "/home/niklas/Uni/02_02_secondMaster/pythonGIS/project/EagleOwlsGenderDifference/movebank/eagle_owl/Eagle owl Reinhard Vohwinkel MPIO/points_32N.shp"

    # read shapfile
    layer_lines = QgsVectorLayer(shpFile_lines, "shape:", "ogr")
    layer_points = QgsVectorLayer(shpFile_points, "shape:", "ogr")

    # make layers only containing fe/-male eagle owls 
    layer_lines_m =  QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())
    layer_lines_f =  QgsVectorLayer(layer_lines.source(), layer_lines.name(), layer_lines.providerType())

    # build requests to filter for sexes
    request_m = QgsFeatureRequest().setFilterExpression(u'"sex" = \'m\'') 
    request_f = QgsFeatureRequest().setFilterExpression(u'"sex" = \'f\'') 

    # apply filters to layers
    layer_lines_m = layer_lines_m.getFeatures(request_m)
    layer_lines_f = layer_lines_f.getFeatures(request_f)

def calc_distance_differences():
    # initiate variables for sex-based distance trends 
    total_length_m = 0
    total_length_f = 0
    count_m = 0
    count_f = 0

    #calculate average distances travelled by sex 
    # male
    for feature in layer_lines_m:
        total_length_m += feature.geometry().length()
        count_m += 1
        
    avg_distance_m = total_length_m/count_m
    print(avg_distance_m)

    # female 
    for feature in layer_lines_f:
        total_length_f += feature.geometry().length()
        count_f += 1
        
    avg_distance_f = total_length_f/count_f
    print(avg_distance_f)

    # difference
    delta_distance = abs(round(avg_distance_f - avg_distance_m, 3))
    print("Difference between sex-based averages is: " + str(delta_distance) + " km")

def calc_height_differences():
    # initiate variables for sex-based height trends 
    total_height_m = 0
    totel_height_f = 0
    count_m = 0
    count_f = 0

    #calculate average height by sex 
    # male
    for feature in layer_points_m:
        total_height_m += feature.getField("height")
        count_m += 1
        
    avg_height_m = total_height_m/count_m
    print(avg_height_m)

    # female 
    for feature in layer_lines_f:
        total_height_f += feature.getField("height")
        count_f += 1
        
    avg_height_f = total_height_f/count_f
    print(avg_height_f)

    # difference
    delta_height = abs(round(avg_height_f - avg_height_m, 3))
    print("Difference between sex-based averages is: " + str(delta_height) + " m")