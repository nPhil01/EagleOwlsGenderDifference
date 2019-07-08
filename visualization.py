import ogr, os
import time, datetime
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

projectPath = QgsProject.instance().fileName()
projectPath = projectPath[:-19]
relativeShapeFilePath = "data/shapefiles/lines_32N.shp"
shpFile = os.path.join(projectPath, relativeShapeFilePath)
layer = QgsVectorLayer(shpFile, "working_layer", "ogr")

femaleSpeed = []
maleSpeed = []
for feat in layer.getFeatures():
    if(feat["sex"]=="f"):
        femaleSpeed.append(float(feat["avg_speed"]))
    if(feat["sex"]=="m"):
        maleSpeed.append(float(feat["avg_speed"]))

print(femaleSpeed)
print(maleSpeed)

data = [maleSpeed, femaleSpeed]
fig7, ax7 = plt.subplots()
ax7.set_title('Average Speed of Male and Female')
ax7.boxplot(data)
plt.xticks([1,2], ["Male", "Female"])

plt.show()