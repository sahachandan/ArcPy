########################################################################################
# Script Name: Split_Tool_Replacer
# Description: Same like Split(Analysis) Tool, but doesn't need Advance License to run!
# Link: https://github.com/sahachandan/ArcPy/tree/master/Split_Tool_Replacer
#
# Author: Chandan Saha
# Date: 18.04.2018
########################################################################################

#Importing Modules
import arcpy, os


#Setting other essential path
inputFeature = arcpy.GetParameterAsText(0)
splitFeature = arcpy.GetParameterAsText(1)
splitField = arcpy.GetParameterAsText(2)
targetWorkspace = arcpy.GetParameterAsText(3)

lyrName = "cstemp"
myLayer = arcpy.MakeFeatureLayer_management(splitFeature, lyrName)

with arcpy.da.SearchCursor(myLayer, splitField) as cursor:
	attributeValues = sorted({row[0] for row in cursor})

for c in attributeValues:
	arcpy.SelectLayerByAttribute_management(myLayer, 'NEW_SELECTION', '"'+ splitField +'"'"=""'" +str(c)+"'")
	arcpy.Clip_analysis(inputFeature, myLayer ,os.path.join(targetWorkspace, str(c)), '#')

del inputFeature, splitFeature, splitField, targetWorkspace, lyrName, myLayer, cursor, attributeValues