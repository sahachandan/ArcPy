# Name: GUIDGenerator
# Description: Generate GUID using method "SHA-1" hash of namespace OID from 3D Polyline feature
# Link: https://github.com/sahachandan/ArcPy/tree/master/GUID_Generator
# Date Created: 08.05.2018
# Last Date Modified: 13.05.2018
# Author: Chandan Saha

# Importing modules
import arcpy
import uuid

# Name of the feature present in Table of Content
featureName = arcpy.GetParameterAsText(0)

# Name of the GUID Field
guidFieldName = arcpy.GetParameterAsText(1)

# Defining method
method = arcpy.GetParameterAsText(2)

# Decimal Precision for X,y and Z value
precision = arcpy.GetParameterAsText(3)

# Converting precision variable value to int
intPrecision = int(precision)

# Field list
allField = ["Root_Str", guidFieldName]

# Creating Field
for i in allField:
	if(i == "Root_Str"):
		arcpy.AddField_management(featureName, i, 'TEXT', '#', '#', '75')
	else:
		arcpy.AddField_management(featureName, i, 'TEXT', '#', '#', '50')

# Generating Shape object
cursorXYZ = arcpy.da.SearchCursor(featureName, ["SHAPE@"])

xList = []
yList = []
zList = []
xyzList = []

# Appending X, y and Z value in respective list
for cord in cursorXYZ:
	if(method == "End Point"):
		listPoint = cord[0].lastPoint
	elif(method == "Start Point"):
		listPoint = cord[0].firstPoint
	xList.append(round(listPoint.X, intPrecision))
	yList.append(round(listPoint.Y, intPrecision))
	zList.append(round(listPoint.Z, intPrecision))

for x,y,z in zip(xList,yList,zList):
	xyz = ("{},{},{}".format(repr(x), repr(y), repr(z)))
	xyzList.append(xyz)

i = 0

# Writing values in attribute table
with arcpy.da.UpdateCursor(featureName, allField) as cursor:
	for row in cursor:
		guid = uuid.uuid5(uuid.NAMESPACE_OID, xyzList[i])
		row[0] = xyzList[i]
		row[1] = guid
		i += 1
		cursor.updateRow(row)

del cursor, listPoint, xList, yList, zList, xyzList, cursorXYZ
# End of Script
