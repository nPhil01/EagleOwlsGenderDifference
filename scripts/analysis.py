import os
import sys
import shutil 
import getpass
import processing
import qgis.utils
from qgis.core import *
from sys import platform


### Initiate global variable projectPath
print("Initiating global variable projectPath")
global projectPath
projectPath = QgsProject.instance().fileName()
### Removes finalAssignment.gqz from project Path
projectPath = projectPath[:-19]
print("Your projectPath is: \"" + projectPath + "\"")

global copyPath
copyPath = os.path.join(projectPath, "scripts/")

### Determine users OS
if platform == "darwin" or platform == "linux" or platform == "linux2":
    
    ### Check if folder contiaining scripts already exist, if so delete it and make a new one
    if os.path.exists("/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins"):
        shutil.rmtree("/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
    os.makedirs("/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins", exist_ok = True)

    ### Try to copy the scripts so QGIS recognizes them
    try:
        shutil.copy(copyPath + "__init__.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "setup.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "analysis.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "data_preprocessing.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "data_processing.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "visualization.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")

        if os.path.exists("/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins/setup.py"):
            print("Your scripts were placed in the right directory and renewed.")
        else:
            print("Could not place your scripts. [SCRIPT NOT FOUND IN DESTINATION ERROR]")

    except:
        print("Could not place your scripts. [COPY ERROR]")  


elif platform == "win32":

    ### Check if folder contiaining scripts already exist, if so delete it and make a new one
    if os.path.exists("C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins"):
        shutil.rmtree("C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
    os.makedirs("C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins", exist_ok = True)

    ### Try to copy the scripts so QGIS recognizes them
    try:
        shutil.copy(copyPath + "__init__.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "setup.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "analysis.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "data_preprocessing.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "data_processing.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins") 
        shutil.copy(copyPath + "data_visualization.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins") 
        
        if os.path.exists("C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/setup.py"):
            print("Your scripts were placed in the right directory and renewed.")
        else:
            print("Could not place your scripts. [SCRIPT NOT FOUND IN DESTINATION ERROR]")

    except:
        print("Could not place your scripts. [COPY ERROR]")

print("Now importing custom modules.")
try:
    from data_processing import data_processing
    from data_preprocessing import data_preprocessing
    from data_visualization import data_visualization
    print("Custom modules were succesfully imported.\n")
except:
    print("Custom modules could not be imported. [IMPORT ERROR]")


# Bundeling all preprocessing functions into one
def run_custom_preprocessing():
    ### handling error in case working_layer already exists in the QGIS project
    try:
        print("Preprocessing started.")
        prep = data_preprocessing()
        prep.csv_preprocessing(projectPath)
        prep.reproject_shapefiles(projectPath)
        prep.add_fields_to_shapefile(projectPath)
        prep.delete_empty_features()
        print("Preprocessing finished.\n")
    except:
        print("WARNING: working_layer already exists. Preprocessing skipped\n")

# Bundeling all rocessing functions into one
def run_custom_processing():
    ### Skip costly computations if shapefile already exists
    if os.path.exists(projectPath + "/data/shapefiles/working_layer.shp"):
        print("Processing started.")
        print("WARNING: Shapefile already exists. Calculating statistical measures skipped")
        print("Linear regression modeling started.")
        try:
            pro = data_processing()
            pro.setup_processing(projectPath)
            pro.prepare_predictions() 
            pro.predict()
            print("Linear regression modeling finished.\n")
        except: 
            print("ERROR: Error in Regression.\n")
    else:
        print("Processing started.")
        try:
            pro = data_processing()
            pro.setup_processing(projectPath)
            pro.calc_distance_differences()
            pro.calculate_height_speed_differences(projectPath)
            pro.prepare_predictions() 
            pro.predict()
            pro.export_layer(projectPath)
            print("Processing finished.\n")
        except:
            print("ERROR: Error in Processing.\n")
    
def run_custom_visualization():
    print("Visualization started.")
    try:
        vis = data_visualization()
        vis.createBoxplots(projectPath)
        vis.createSpaceTimeCubeForAllOwls(projectPath)
        print("Visualization finished.\n")
    except:
        print("ERROR: Error in Visualization.\n")


run_custom_preprocessing()
run_custom_processing()
run_custom_visualization()