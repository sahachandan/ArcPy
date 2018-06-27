import arcpy
import random

pointFeature = arcpy.GetParameterAsText(0)
polygonFeature = arcpy.GetParameterAsText(1)
floorIdField = arcpy.GetParameterAsText(2)
gisSpaceField = arcpy.GetParameterAsText(3)
cadDesignField = arcpy.GetParameterAsText(4)
updateField = [gisSpaceField, cadDesignField]

tempField = "Temp_{}".format(random.randint(1, 9999))
arcpy.AddField_management(pointFeature, tempField, "TEXT", "", "", "30")

tempValue = 0

with arcpy.da.UpdateCursor(pointFeature, tempField) as tempcursor:
	for templ in tempcursor:
		templ[0] = tempValue
		tempValue += 1
		tempcursor.updateRow(templ)

pointcursor = arcpy.SearchCursor(pointFeature)

i = 0

for row in pointcursor:

	#arcpy.SelectLayerByAttribute_management(pointFeature, 'NEW_SELECTION', '"{}" ='.format(tempField) + str(i))
	arcpy.SelectLayerByAttribute_management(pointFeature, 'NEW_SELECTION', "{} = '{}'".format(tempField, i))
	
	floorID= (str(row.getValue(floorIdField)))
	
	arcpy.SelectLayerByLocation_management(polygonFeature, 'INTERSECT', pointFeature, '#', 'NEW_SELECTION')
	
	polygoncursor = arcpy.SearchCursor(polygonFeature)
	for poly in polygoncursor:
		if(str(poly.getValue(floorIdField)) == floorID):
			gisID = (poly.getValue(updateField[0]))
			cadID = (poly.getValue(updateField[1]))
	
	ucursor = arcpy.da.UpdateCursor(pointFeature, updateField)
	for u in ucursor:
		u[0] = gisID
		u[1] = cadID
		ucursor.updateRow(u)
	i+=1
	del ucursor, polygoncursor

arcpy.SelectLayerByAttribute_management(pointFeature, "CLEAR_SELECTION")
arcpy.SelectLayerByAttribute_management(polygonFeature, "CLEAR_SELECTION")

del tempcursor, pointcursor

arcpy.DeleteField_management(pointFeature, tempField)
