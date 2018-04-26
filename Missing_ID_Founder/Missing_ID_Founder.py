########################################################################################
# Script Name: Missing_ID_Founder
# Description: VLOOKUP in Field table
# Link: https://github.com/sahachandan/ArcPy/tree/master/Missing_ID_Founder
#
# Author: Chandan Saha
# Date Created: 26.04.2018
# Last Date Modified: 26.04.2018
########################################################################################

import arcpy
import random

sourceLayer = ""
targetLayer = ""
fieldName = ""

sourceList = [row[0] for row in arcpy.da.SearchCursor(sourceLayer, fieldName)]
targetList = [row[0] for row in arcpy.da.SearchCursor(targetLayer, fieldName)]

missingList = [c for c in targetList if c not in sourceList]

if len(missingList) != 0:

    commentField = "Com_{}".format(random.randint(1, 99999))
    arcpy.AddField_management(targetLayer, commentField, "TEXT", "", "", "20")

    with arcpy.da.UpdateCursor(targetLayer, ([fieldName, commentField])) as cursor:
        for row in cursor:
            for missing in missingList:
                if row[0] == missing:
                    row[1] = "MISSING"
                cursor.updateRow(row)

else:
    print("Hurrah! All ID mathced, no Missing in Target Layer")

del cursor, sourceList, targetList, missingList

# End of Script