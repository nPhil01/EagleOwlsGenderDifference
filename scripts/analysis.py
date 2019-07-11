#from data_preprocessing import data_preprocessing
from data_processing import data_processing
import sys


#setup.init()
global projectPath
projectPath = QgsProject.instance().fileName()
### Removes finalAssignment.gqz from project Path
projectPath = projectPath[:-19]

pro = data_processing()
pro.setup_processing(projectPath)
pro.calc_distance_differences()
pro.prepare_predictions() 
pro.predict()
pro.calculate_height_speed_differences(projectPath)