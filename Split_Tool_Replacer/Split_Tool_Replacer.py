##This Script needs ArcMap Advance License to run successfully

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