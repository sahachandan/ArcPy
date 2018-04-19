########################################################################################
# Script Name: Split_Tool_Replacer
# Description: Same like Split(Analysis) Tool, but doesn't need Advance License to run!
# Link: https://github.com/sahachandan/ArcPy/tree/master/Split_Tool_Replacer
#
# Author: Chandan Saha
# Date Created: 18.04.2018
# Last Date Modified: 20.04.2018
########################################################################################

#Importing Modules
import arcpy, os

#Setting up required parameters
inputFeature = arcpy.GetParameterAsText(0)
splitFeature = arcpy.GetParameterAsText(1)
splitField = arcpy.GetParameterAsText(2)
targetWorkspace = arcpy.GetParameterAsText(3)

lyrName = "cstemp"

#Making Feature Layer of Split Feature
myLayer = arcpy.MakeFeatureLayer_management(splitFeature, lyrName)

#Storing unique field value in a list from user defined Split Field
with arcpy.da.SearchCursor(myLayer, splitField) as cursor:
	attributeValues = sorted({row[0] for row in cursor})


for c in attributeValues:
	#Make Selection in Table
	arcpy.SelectLayerByAttribute_management(myLayer, 'NEW_SELECTION', '"'+ splitField +'"'"=""'" +str(c)+"'")
	
	#Validating Attribute Value for exporting
	validatedAtrbName = arcpy.ValidateFieldName(str(c))
	
	#Clipping Input Feature
	arcpy.Clip_analysis(inputFeature, myLayer ,os.path.join(targetWorkspace, validatedAtrbName), '#')

del myLayer, cursor, attributeValues

#Script End