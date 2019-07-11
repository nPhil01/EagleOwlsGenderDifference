import os
import qgis.utils
import getpass
from qgis.core import *
from sys import platform
import shutil 

def init():
    global projectPath
    projectPath = QgsProject.instance().fileName()
    ### Removes finalAssignment.gqz from project Path
    projectPath = projectPath[:-19]
    global copyPath
    copyPath = os.path.join(projectPath, "scripts/")

    if platform == "linux" or platform == "linux2":
        copyfile(copyPath, "/home/USER/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
    elif platform == "darwin":
        copyfile(copyPath, "/home/USER/.local/share/QGIS/QGIS3/profiles/default/python/plugins")
    elif platform == "win32":
        shutil.copy(copyPath + "setup.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "data_preprocessing.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
        shutil.copy(copyPath + "data_processing.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
        #shutil.copy(copyPath + "data_visualization.py" , "C:/Users/" + getpass.getuser() + "/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins")
        
init()