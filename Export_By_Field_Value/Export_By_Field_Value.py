####################################################################################
# Script Name: Export_By_Field_Value
# Version: 1.0
# Description: Export Shape File by its unique Attribute Value of required field
# Location: https://github.com/sahachandan/ArcPy/tree/master/Export_By_Field_Value
#
# Author: Chandan Saha
# Date: 07.04.2018
#####################################################################################

import arcpy, os

fieldName = ""    #Insert FIELD NAME by which attribute value you want to export Shape File.


# Creating Map Document Object from Current
mxd = arcpy.mapping.MapDocument("Current")

hasFound = False

if (fieldName == ""):
	print "'"'fieldName'"' Variable is Blank. Please Insert FIELD NAME!."

else:
	
	for lyr in arcpy.mapping.ListLayers(mxd,"*"):
	
		#Storing File Name in "featureName" Variable
		featureName = lyr.datasetName
		
		# Storing File Path in "featurePath" Variable
		featurePath = lyr.workspacePath
        
		#Created a variable which store the name of output folder
		folderName = fieldName + "_" + str(featureName)
		
		
		fieldObjList = arcpy.ListFields(lyr) 
		      
		for eachField in fieldObjList:
			if (eachField.aliasName != fieldName):
				continue
			else:
				with arcpy.da.SearchCursor(lyr, fieldName) as cursor:
					attributeValues = sorted({row[0] for row in cursor})
					
				
				arcpy.CreateFolder_management(featurePath, folderName)

				for c in attributeValues:
					arcpy.SelectLayerByAttribute_management(featureName, 'NEW_SELECTION', '"'+fieldName+'"'"=""'" +str(c)+"'")
					print str(c)
					arcpy.CopyFeatures_management(featureName, os.path.join (featurePath, folderName, str(c)), '#', '0', '0', '0')

				arcpy.SelectLayerByAttribute_management(featureName, "CLEAR_SELECTION")
				attributeValues[:] = []
				fieldObjList[:] = []
				hasFound = True
        
		if (hasFound == False):
			print ('"' + fieldName +'"' + ' Field not exist in ' + '"' + featureName + '"' + ' Feature! Insert correct FIELD NAME.')
	
		hasFound = False
del mxd

#End of Script