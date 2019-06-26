import processing
from qgis.core import *

# Define queries to select male/female for gender specific trends

# Query females
query_f = '"SEX" = female'
selection_f = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query_f))
layer.setSelectedFeatures([k.id() for k in selection])

# Query males
query_m = '"SEX" = male'
selection_f = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query_m))
layer.setSelectedFeatures([k.id() for k in selection])
