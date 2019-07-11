from preprocessing import preprocessing
from processing import processing
import sys

sys.path.append('~/scripts')

def main():
    
    print("Hello")

    prep = preprocessing()
    prep.reproject_shapefiles()
    prep.csv_preprocessing()
    prep.add_fields_to_shapefile()
    prep.delete_empty_features()

    pro = data_processing()
    pro.processing_setup()
    pro.calc_distance_differences()
    pro.prepare_predictions() 
    pro.predict()
    pro.calc_height_speed_differences()