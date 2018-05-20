import arcpy
import random

pointFeature = "point"
polygonFeature = "Polygon"
matchField = "FLOOR_ID"
updateField = ["GIS_SPACEI", "CAD_Design"]

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
	
	floorID= (str(row.getValue(matchField)))
	
	arcpy.SelectLayerByLocation_management(polygonFeature, 'INTERSECT', pointFeature, '#', 'NEW_SELECTION', 'NOT_INVERT')
	
	polygoncursor = arcpy.SearchCursor(polygonFeature)
	for poly in polygoncursor:
		if(str(poly.getValue(matchField)) == floorID):
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
