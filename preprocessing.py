import os
import csv
import numpy as np
from osgeo import ogr
import processing

#csvPath = "./eagle_owl_csv/eagle_owl.csv"
csvPath = "/Users/user/Desktop/eagle_owl/eagle_owl.csv"

##Preprocess CSV
with open(csvPath) as csvfile:
    data = np.array(list(csv.reader(csvfile, delimiter=",")))


reduced_data = data[:,[1,3,8,10,]]  #Drop all columns except for declared indices
reduced_data = np.delete(reduced_data,[4,18] ,axis=0, )  # Drop rows with empty fields

# Reproject data to UTM 32N
# Define reprojection parameters
parameter = {'INPUT': '/Users/user/Desktop/eagle_owl/eagle_owl_shp/lines.shp', 'TARGET_CRS': 'EPSG:4647',
                 'OUTPUT': '/Users/user/Desktop/eagle_owl/eagle_owl_shp/lines_32N.shp'}

# Run reprojection
processing.run('qgis:reprojectlayer', parameter)


##Parsing SHP file and accessing attributes
#shpFile = "./eagle_owl_shp/lines.shp"
shpFile = "/Users/user/Desktop/eagle_owl/eagle_owl_shp/lines.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
file = driver.Open(shpFile, 0)
layer = file.GetLayer(0)
print(layer.GetFeatureCount())