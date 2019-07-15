import os
import sys
import shutil 
import getpass
import warnings
import processing
import qgis.utils
from qgis.core import *
from sys import platform


print("\nSetting up required environment:\n")
try:
    ### Initiate global variable projectPath
    print("Initiating global variable projectPath")
    global projectPath
    projectPath = QgsProject.instance().fileName()
    ### Removes finalAssignment.gqz from project Path
    projectPath = projectPath[:-19]
    print("Your projectPath is: \"" + projectPath + "\"\n")

    global copyPath
    copyPath = os.path.join(projectPath, "scripts/")

    ### Determine whether user's OS is Linux or MacOS 
    if platform == "darwin" or platform == "linux" or platform == "linux2":
        
        ### Check if folder contiaining scripts already exist, if so delete it and make a new one
        if os.path.exists("/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins"):
            shutil.rmtree("/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
            os.makedirs("/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins", exist_ok = True)

        ### Try to copy the scripts so QGIS recognizes them
        try:
            shutil.copy(copyPath + "__init__.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
            shutil.copy(copyPath + "analysis.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
            shutil.copy(copyPath + "data_preprocessing.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
            shutil.copy(copyPath + "data_processing.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
            shutil.copy(copyPath + "visualization.py" , "/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins")

            if os.path.exists("/home/" + getpass.getuser() + "/.local/share/QGIS/QGIS3/profiles/default/python/plugins/analysis.py"):
                print("Your scripts were placed in the right directory and renewed.\n")
            else:
                raise EnvironmentError("Could not find your scripts.") 

        except:
            raise EnvironmentError("Could not place your scripts.") 

    ### Determine whether user's OS is Windows
    elif platform == "win32":

        ### Check if folder contiaining scripts already exist, if so delete it and make a new one
        if os.path.exists("C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins"):
            shutil.rmtree("C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
            os.makedirs("C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins", exist_ok = True)
        else:
            os.makedirs("C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins", exist_ok = True)
       
        ### Try to copy the scripts so QGIS recognizes them
        try:
            shutil.copy(copyPath + "__init__.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
            shutil.copy(copyPath + "analysis.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
            shutil.copy(copyPath + "data_preprocessing.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
            shutil.copy(copyPath + "data_processing.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins") 
            shutil.copy(copyPath + "data_visualization.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins") 
            
            if os.path.exists("C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/analysis.py"):
                print("Your scripts were placed in the right directory and renewed.\n")
            else:
                raise EnvironmentError("Could not find your scripts.") 

        except:
            raise EnvironmentError("Could not place your scripts.")


    print("Now importing custom modules.")
    try:
        from data_processing import data_processing
        from data_preprocessing import data_preprocessing
        from data_visualization import data_visualization
        print("Custom modules were succesfully imported.\n")
    except:
        raise ImportError("Custom modules could not be imported.")

    print("Setup successfully completed.\n")

except:
    raise EnvironmentError("Environment could not be set up. Please restart your QGIS session.")


# Bundling all preprocessing functions into one
def run_custom_preprocessing():
    ### handling error in case working_layer already exists in the QGIS project
    try:
        print("Preprocessing started.\n")
        prep = data_preprocessing()
        prep.csv_preprocessing(projectPath)
        prep.reproject_shapefiles(projectPath)
        prep.add_fields_to_shapefile(projectPath)
        prep.delete_empty_features()
        print("Preprocessing finished.\n")
    except:
        warnings.warn("working_layer already exists. Preprocessing skipped")
        print("WARNING: working_layer already exists. Preprocessing skipped\n")


# Bundling all processing functions into one
def run_custom_processing():
    ### Skip costly computations if shapefile already exists
    if os.path.exists(projectPath + "/data/shapefiles/working_layer.shp"):
        print("Processing started.")
        warnings.warn("Shapefile already exists. Calculating statistical measures skipped")
        print("WARNING: Shapefile already exists. Calculating statistical measures skipped\n")
        print("Linear regression modeling started.")
        try:
            pro = data_processing()
            pro.setup_processing(projectPath)
            pro.prepare_predictions() 
            pro.predict()
            print("Linear regression modeling finished.\n")
        except: 
           raise RuntimeError("Error encountered while computing regressions.")
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
            raise RuntimeError("Error encountered while processing data.")
    

# Bundling all visualization functions into one
def run_custom_visualization():
    print("Visualization started.")
    try:
        vis = data_visualization()
        vis.createBoxplots(projectPath)
        vis.createSpaceTimeCubeForAllOwls(projectPath)
        print("Visualization finished.\n")
    except:
        raise RuntimeError("Error encountered while visualizing data.")


run_custom_preprocessing()
run_custom_processing()
run_custom_visualization()