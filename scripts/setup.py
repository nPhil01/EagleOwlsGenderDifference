import os
import shutil 
import getpass
import qgis.utils
from qgis.core import *
from sys import platform

class setup():

    def initiate(self):
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

setu = setup()
setu.initiate()