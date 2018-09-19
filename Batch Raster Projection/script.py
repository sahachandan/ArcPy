###########################################################################################
# Script Name: Batch Raster Projection (Script Tool Version)
# Description: Project all raster files from specific directory using projected shape file
#
# Author: Chandan Saha
# Date: 18.09.2018
###########################################################################################

import arcpy
import os

#Select Folder
myWorkspace = arcpy.GetParameterAsText(0)

#Raster Type
rasterType = arcpy.GetParameterAsText(1)

#Import Projected Shapefile
myShapeFile = arcpy.GetParameterAsText(2)

#Changing workspace
arcpy.env.workspace = myWorkspace

#Creating Spatial Reference object from Shape File
myProj = arcpy.Describe(myShapeFile).spatialReference

#Empty list
rastersList = []

#List of raster files in myWorkspace
allRaster = arcpy.ListRasters("*", rasterType)

#Appending full path of raster file in rastersList
for rasters in allRaster:
    rastersList.append(os.path.join(myWorkspace, rasters))

#Defining projection or reprojection
for rasters in rastersList:
    arcpy.DefineProjection_management(rasters, myProj)

#arcpy.AddMessage(rastersList)
#arcpy.AddMessage(myShapeFile)

del myProj, allRaster, rastersList

#End of script
