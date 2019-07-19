import os
import ogr
import time
import datetime
import qgis.utils
from qgis.core import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Class used implement the advanced visualization
class data_visualization():

    # Function used to create boxplots of statistical measures
    def createBoxplots(self, projectPath):

        print("Creating boxplots.")
        try:
            relativeShapeFilePath = "./data/shapefiles/lines_32N.shp"
            shpFile = os.path.join(projectPath, relativeShapeFilePath)
            self.layer = QgsVectorLayer(shpFile, "working_layer", "ogr")

            # Create empty arrays for displaying differences between females and males
            femaleSpeed = []
            maleSpeed = []
            femaleHeight = []
            maleHeight = []
            femaleDis = []
            maleDis = []
            # color code = male:blue; female:red
            colors = ['blue', 'red']

            # Filling arrays
            for feat in self.layer.getFeatures():
                if (feat["sex"] == "f"):
                    femaleSpeed.append(float(feat["avg_speed"]))
                    femaleHeight.append(float(feat["avg_height"]))
                    femaleDis.append(float(feat["yearly_dis"]) / 1000)
                if (feat["sex"] == "m"):
                    maleSpeed.append(float(feat["avg_speed"]))
                    maleHeight.append(float(feat["avg_height"]))
                    maleDis.append(float(feat["yearly_dis"]) / 1000)

            # Create plot for average speed
            data = [maleSpeed, femaleSpeed]
            fig1, ax1 = plt.subplots()
            ax1.set_title('Average travelled Speed of Male and Female')
            ax1.set_ylabel('Speed [km/h]')
            ax1.yaxis.grid(True)

            # Add patch_artist=True option to ax.boxplot() to get fill color
            bp = ax1.boxplot(data, patch_artist=True, whis=100)

            # Change outline color, fill color and linewidth of the boxes
            for box in bp['boxes']:
                # Change outline color
                box.set(color='#7570b3', linewidth=2)
                # Change fill color
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)

            # Change color and linewidth of the whiskers
            for whisker in bp['whiskers']:
                whisker.set(color='#7570b3', linewidth=1)

            # Change color and linewidth of the caps
            for cap in bp['caps']:
                cap.set(color='#7570b3', linewidth=1)

            # Change color and linewidth of the medians
            for median in bp['medians']:
                median.set(color='#b2df8a', linewidth=1)

            # Change the style of fliers and their fill
            for flier in bp['fliers']:
                flier.set(marker='o', color='#e7298a', alpha=0.5)

            ax1.set_facecolor('xkcd:ivory')
            plt.xticks([1, 2], ["Male", "Female"])

            # Create plot for average distance
            data = [maleDis, femaleDis]
            fig2, ax2 = plt.subplots()
            ax2.set_title('Average travelled Distance of Male and Female')
            ax2.set_ylabel('Distance [km]')
            ax2.yaxis.grid(True)

            # Add patch_artist=True option to ax.boxplot() to get fill color
            bp = ax2.boxplot(data, patch_artist=True)

            # Change outline color, fill color and linewidth of the boxes
            for box in bp['boxes']:
                # Change outline color
                box.set(color='#7570b3', linewidth=2)
                # Change fill color
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)

            # Change color and linewidth of the whiskers
            for whisker in bp['whiskers']:
                whisker.set(color='#7570b3', linewidth=1)

            # Change color and linewidth of the caps
            for cap in bp['caps']:
                cap.set(color='#7570b3', linewidth=1)

            # Change color and linewidth of the medians
            for median in bp['medians']:
                median.set(color='#b2df8a', linewidth=1)

            # Change the style of fliers and their fill
            for flier in bp['fliers']:
                flier.set(marker='o', color='#e7298a', alpha=0.5)
            ax2.set_facecolor('xkcd:ivory')
            plt.xticks([1, 2], ["Male", "Female"])

            # Create plot for average height
            data = [maleHeight, femaleHeight]
            fig3, ax3 = plt.subplots()
            ax3.set_title('Average travelled Height of Male and Female')
            ax3.set_ylabel('Height [m]')
            ax3.yaxis.grid(True)

            # Add patch_artist=True option to ax.boxplot() to get fill color
            bp = ax3.boxplot(data, patch_artist=True)

            # Change outline color, fill color and linewidth of the boxes
            for box in bp['boxes']:
                # Change outline color
                box.set(color='#7570b3', linewidth=2)
                # Change fill color
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)

            # Change color and linewidth of the whiskers
            for whisker in bp['whiskers']:
                whisker.set(color='#7570b3', linewidth=1)

            # Change color and linewidth of the caps
            for cap in bp['caps']:
                cap.set(color='#7570b3', linewidth=1)

            # Change color and linewidth of the medians
            for median in bp['medians']:
                median.set(color='#b2df8a', linewidth=1)

            # Change the style of fliers and their fill
            for flier in bp['fliers']:
                flier.set(marker='o', color='#e7298a', alpha=0.5)

            plt.xticks([1, 2], ["Male", "Female"])
            ax3.set_facecolor('xkcd:ivory')
            plt.show()

            print("DONE: Creating boxplots.")

        except:
            raise RuntimeError("Error encountered during creation of boxplots.")

    # Function used to build Space-Time Cubes for owl tracks
    def createSpaceTimeCubeForAllOwls(self, projectPath):
        '''
        creates space time cube for two owls from shapefile with specified ID

        Based on:
        Author: Nimrod Gavish
        Maintainer: ngavish
        Owners: 0342120
        Plugin home page: https://github.com/Nimrod51/GPX-To-SpaceTimeCube
        Tracker: Browse and report bugs
        Code repository: https://github.com/Nimrod51/GPX-To-SpaceTimeCube
        Latest stable version: 0.2
        '''

        print("Creating space-time cubes.")
        try:
            relativeFilePath = "data/shapefiles/points.shp"
            in_path = os.path.join(projectPath, relativeFilePath)

            # Read shapefile Layer
            driver = ogr.GetDriverByName('ESRI Shapefile')

            # Open shaepfileLayer
            data_source = driver.Open(in_path, 0)

            # Plot parameters
            mpl.rcParams['legend.fontsize'] = 10

            # Create self.layer from data source
            if data_source is None:
                print ("Could not open " + in_path)
            else:
                print ("Opened " + in_path)
                self.layer = data_source.GetLayer()

            schema = []
            ldefn = self.layer.GetLayerDefn()
            for n in range(ldefn.GetFieldCount()):
                fdefn = ldefn.GetFieldDefn(n)
                schema.append(fdefn.name)

            try:
                timeIndex = schema.index('timestamp')
            except ValueError:
                print ("No time field found")

            try:
                idIndex = schema.index('ind_ident')
            except ValueError:
                print ("No id field found")

            idArray = []
            try:
                animalId = ""
                for feat in self.layer:
                    if (animalId != feat.GetField(idIndex)):
                        animalId = feat.GetField(idIndex)
                        idArray.append(animalId)
            except:
                print("no animal ID")
            self.layer.ResetReading()


            try:
                for id in idArray:
                    if (id == "Eagle Owl eobs 4044, 5159 / DEW A1822"):
                        fig = plt.figure(id)
                        ax = fig.gca(projection='3d')
                        print(id)
                        x = []  # Latitude
                        y = []  # Latitude
                        z = []  # Time in minutes since start
                        elapsedTime = []  # Time in seconds since epoch
                        DTArray = []  # Array of python strings
                        DateTimeArray = []  # Python datetime object of each point
                        try:
                            for feat in self.layer:
                                if (id == feat.GetField(idIndex)):
                                    # Get time and spatial data from shp dynamically and plot

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
                        self.layer.ResetReading()
                        # Create sub title for plot
                        title = DateTimeArray[0].strftime("%Y/%m/%d") + " " + DTArray[0] + " to " + DateTimeArray[
                            -1].strftime(
                            "%Y/%m/%d") + " " + DTArray[-1]

                        # Extract elapsed time in minutes
                        z.append(0)  # First item in elapsedTime array should be 0
                        for i in range(1, len(elapsedTime)):
                            z.append((elapsedTime[i] - elapsedTime[0]) / 86400)

                        # Plot X,Y,Z
                        ax.plot(x, y, z, color='red')

                        # Labels & Plot
                        ax.set_xlabel('Longitude')
                        ax.set_ylabel('Latitude')
                        ax.set_zlabel('Time (Days)')
                        ax.legend()
                        plt.axis("equal")
                        fig.suptitle('Space Time Cube for id: 4044, 5159 / DEW A1822', fontsize=12, fontweight='bold')
                        plt.title(title, loc='center')

                    if (id == "Eagle Owl eobs1751 / DEW 25879"):
                        fig = plt.figure(id)
                        ax = fig.gca(projection='3d')
                        print(id)
                        x = []  # Latitude
                        y = []  # Latitude
                        z = []  # Time in minutes since start
                        elapsedTime = []  # Time in seconds since epoch
                        DTArray = []  # Array of python strings
                        DateTimeArray = []  # Python datetime object of each point
                        try:
                            for feat in self.layer:
                                if (id == feat.GetField(idIndex)):
                                    # Get time and spatial data from shp dynamically and plot

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
                        self.layer.ResetReading()
                        # Create sub title for plot
                        title = DateTimeArray[0].strftime("%Y/%m/%d") + " " + DTArray[0] + " to " + DateTimeArray[
                            -1].strftime(
                            "%Y/%m/%d") + " " + DTArray[-1]

                        # Extract elapsed time in minutes
                        z.append(0)  # First item in elapsedTime array should be 0
                        for i in range(1, len(elapsedTime)):
                            z.append((elapsedTime[i] - elapsedTime[0]) / 86400)

                        # Plot X,Y,Z
                        ax.plot(x, y, z, color='blue')

                        # Labels & Plot
                        ax.set_xlabel('Longitude')
                        ax.set_ylabel('Latitude')
                        ax.set_zlabel('Time (Days)')
                        ax.legend()
                        plt.axis("equal")
                        fig.suptitle('Space Time Cube for id: 1751 / DEW 25879', fontsize=12, fontweight='bold')
                        plt.title(title, loc='center')

                plt.show()
            except:
                raise RuntimeError("Error encountered during creation of space-time cubes.")
        except:
            raise RuntimeError("Error encountered during creation of space-time cubes.")