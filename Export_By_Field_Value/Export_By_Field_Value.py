import arcpy, os

fieldName = ""    #Please Insert FIELD NAME by which attribute value you want to export Shape File.

found = False

if (fieldName == ""):
	print "'"'fieldName'"' Variable is Blank. Please Insert FIELD NAME!."

else:
	mxd = arcpy.mapping.MapDocument("Current")

	for lyr in arcpy.mapping.ListLayers(mxd,"*"):
                featureName = lyr.datasetName
		featurePath = lyr.workspacePath
                fieldObjList = arcpy.ListFields(lyr)
                
		for eachField in fieldObjList:
			if (eachField.aliasName == fieldName):
				with arcpy.da.SearchCursor(lyr, fieldName) as cursor:
					attributeValues = sorted({row[0] for row in cursor})

				arcpy.CreateFolder_management(featurePath, fieldName)

				for c in attributeValues:
					arcpy.SelectLayerByAttribute_management(featureName, 'NEW_SELECTION', '"'+fieldName+'"'"=""'" +str(c)+"'")
					arcpy.CopyFeatures_management(featureName, os.path.join (featurePath, fieldName, str(c)), '#', '0', '0', '0')
	
				found = True
				
	arcpy.SelectLayerByAttribute_management(featureName, "CLEAR_SELECTION")
	attributeValues[:] = []			
        del mxd
        
        if (found == False):
                print ('"' + fieldName +'"' + ' not exist in ' + featureName + ' feature! Insert correct FIELD NAME.')
