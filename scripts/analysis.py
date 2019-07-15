import sys
import processing
from data_processing import data_processing
from data_preprocessing import data_preprocessing

def run_custom_preprocessing():
    prep = data_preprocessing()
    prep.csv_preprocessing(projectPath)
    prep.reproject_shapefiles(projectPath)
    prep.add_fields_to_shapefile(projectPath)
    prep.delete_empty_features()

def run_custom_processing():
    pro = data_processing()
    pro.setup_processing(projectPath)
    pro.calc_distance_differences()
    pro.calculate_height_speed_differences(projectPath)
    pro.prepare_predictions() 
    pro.predict()
    
run_custom_preprocessing()
run_custom_processing()