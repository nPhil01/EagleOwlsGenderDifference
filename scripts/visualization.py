import ogr, os
import time, datetime
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class visualizaiton():

    def createBoxplots():
        projectPath = QgsProject.instance().fileName()
        projectPath = projectPath[:-19]
        relativeShapeFilePath = "./data/shapefiles/lines_32N.shp"
        shpFile = os.path.join(projectPath, relativeShapeFilePath)
        layer = QgsVectorLayer(shpFile, "working_layer", "ogr")

        #create empty arrays for displaying differences between females and males
        femaleSpeed = []
        maleSpeed = []
        femaleHeight = []
        maleHeight = []
        femaleDis = []
        maleDis = []

        #filling arrays
        for feat in layer.getFeatures():
            if(feat["sex"]=="f"):
                femaleSpeed.append(float(feat["avg_speed"]))
                femaleHeight.append(float(feat["avg_height"]))
                femaleDis.append(float(feat["yearly_dis"])/1000)
            if(feat["sex"]=="m"):
                maleSpeed.append(float(feat["avg_speed"]))
                maleHeight.append(float(feat["avg_height"]))
                maleDis.append(float(feat["yearly_dis"])/1000)

        #create plot for average speed
        data = [maleSpeed, femaleSpeed]
        fig1, ax1 = plt.subplots()
        ax1.set_title('Average Speed of Male and Female')
        ax1.set_ylabel('Average Speed [km/h]')
        ax1.boxplot(data, whis = 100)
        plt.xticks([1,2], ["Male", "Female"])

        #create plot for average distance
        data = [maleDis, femaleDis]
        fig2, ax2 = plt.subplots()
        ax2.set_title('Average Distance travelled per year of Male and Female')
        ax2.set_ylabel('Average distance travelled [km]')
        ax2.boxplot(data)
        plt.xticks([1,2], ["Male", "Female"])

        #create plot for average height
        data = [maleHeight, femaleHeight]
        fig3, ax3 = plt.subplots()
        ax3.set_title('Average Height of Male and Female')
        ax3.set_ylabel('Average Height [m]')
        ax3.boxplot(data)
        plt.xticks([1,2], ["Male", "Female"])

        plt.show()

    def createSpaceTimeCubeForAllOwls():
        '''
        creates space time cube for all owls from shapefile

        Based on:
        Author: Nimrod Gavish
        Maintainer: ngavish
        Owners: 0342120
        Tags: 3d , gpx , matplotlib
        Plugin home page: https://github.com/Nimrod51/GPX-To-SpaceTimeCube
        Tracker:Browse and report bugs
        Code repository: https://github.com/Nimrod51/GPX-To-SpaceTimeCube
        Latest stable version: 0.2
        '''

        # takes path of the finalAssignment qgis project
        projectPath = QgsProject.instance().fileName()
        # removes finalAssignment.gqz from project Path
        projectPath = projectPath[:-20]
        relativeFilePath = "data/shapefiles/points.shp"
        in_path = os.path.join(projectPath, relativeFilePath)

        # read shapefile Layer
        driver = ogr.GetDriverByName('ESRI Shapefile')
        data_source = driver.Open(in_path, 0)

        # Open shaepfileLayer
        data_source = driver.Open(in_path, 0)

        # Plot parameters
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # Create layer from data source
        if data_source is None:
            print ("Could not open " + in_path)
        else:
            print ("Opened " + in_path)
            layer = data_source.GetLayer()  # (4)  # 0 - waypoints, 1 - routes, 2 - tracks, 3 - route points, 4 - track points

        # Get time and spatial data from GPX dynamically and plot
        x = []  # Latitude
        y = []  # Latitude
        z = []  ##Time in minutes since start
        elapsedTime = []  # Time in seconds since epoch
        DTArray = []  ##Array of python strings
        DateTimeArray = []  # Python datetime object of each point
        schema = []

        ldefn = layer.GetLayerDefn()
        for n in range(ldefn.GetFieldCount()):
            fdefn = ldefn.GetFieldDefn(n)
            schema.append(fdefn.name)

        try:
            timeIndex = schema.index('timestamp')
        except ValueError:
            print ("No time field found")

        try:
            for feat in layer:
                pt = feat.geometry()
                x.append(pt.GetX())
                y.append(pt.GetY())
                dateTime = feat.GetField(timeIndex)

                try:
                    DT = datetime.datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    DT = datetime.datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S.%f+00")
                DateTimeArray.append(DT)
                SSE = time.mktime(DT.timetuple())  # Seconds since epoch
                elapsedTime.append(SSE)
                DTArray.append(DT.strftime("%H:%M:%S"))

        except TypeError:
            print ("Time field does contain none or invalid dates")

        # Create sub title for plot
        title = DateTimeArray[0].strftime("%Y/%m/%d") + " " + DTArray[0] + " to " + DateTimeArray[-1].strftime(
            "%Y/%m/%d") + " " + DTArray[-1]

        # Extract elapsed time in minutes
        z.append(0)  # First item in elapsedTime array should be 0
        for i in range(1, len(elapsedTime)):
            z.append((elapsedTime[i] - elapsedTime[0]) / 86400)

        # Plot X,Y,Z
        ax.plot(x, y, z)

        # Labels & Plot
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_zlabel('Time (Days)')
        ax.legend()
        plt.axis("equal")
        fig.suptitle('Space Time Cube', fontsize=12, fontweight='bold')
        plt.title(title, loc='center')
        plt.show()

        # Optionally save the image
        # plt.savefig("C:/Output/SpaceTimePlot.jpg", dpi=100, format="jpg")

        ##Optionally animate image
        # for angle in range(0, 360):
        #    ax.view_init(30, angle)
        #    plt.draw()
        #    plt.pause(.001)

        print ("DONE")


visualizaiton.createBoxplots()
visualizaiton.createSpaceTimeCubeForAllOwls()