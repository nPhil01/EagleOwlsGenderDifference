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
femaleHeight = []
maleHeight = []
femaleDis = []
maleDis = []

for feat in layer.getFeatures():
    if(feat["sex"]=="f"):
        femaleSpeed.append(float(feat["avg_speed"]))
        femaleHeight.append(float(feat["avg_height"]))
        femaleDis.append(float(feat["yearly_dis"]))
    if(feat["sex"]=="m"):
        maleSpeed.append(float(feat["avg_speed"]))
        maleHeight.append(float(feat["avg_height"]))
        maleDis.append(float(feat["yearly_dis"]))

data = [maleSpeed, femaleSpeed]
fig1, ax1 = plt.subplots()
ax1.set_title('Average Speed of Male and Female')
ax1.boxplot(data)
plt.xticks([1,2], ["Male", "Female"])

data = [maleDis, femaleDis]
fig2, ax2 = plt.subplots()
ax2.set_title('Average Distance travelled per year of Male and Female')
ax2.boxplot(data)
plt.xticks([1,2], ["Male", "Female"])

data = [maleHeight, femaleHeight]
fig3, ax3 = plt.subplots()
ax3.set_title('Average Height of Male and Female')
ax3.boxplot(data)
plt.xticks([1,2], ["Male", "Female"])

plt.show()