import arcpy
from arcpy.sa import *
import time
import os


arcpy.env.workspace = r"C:\Users\lenovo\Documents\ArcGIS"
database = "Default2.gdb"
folder_path = r'C:\Users\lenovo\Desktop\cleaned-ipl-data\cleaned-batsman'

bowler_names = os.listdir(folder_path)

for bowler_name in bowler_names:

	input_file = folder_path + '\\' + bowler_name

	pointinfo = (bowler_name.split('.')[0]).replace(" ", "")


	arcpy.PointFileInformation_3d(input = input_file, out_feature_class = database + "/" + pointinfo, in_file_type="XYZ", file_suffix="xyz", decimal_separator="DECIMAL_POINT", summarize_by_class_code = True)

	time.sleep(1.5)

	pointspacing = arcpy.SearchCursor (pointinfo)
	for row in pointspacing:
		avg_space = (row.getValue("Pt_Spacing"))
	print avg_space

	time.sleep(1.5)

	arcpy.ASCII3DToFeatureClass_3d(input = input_file, in_file_type = "XYZ", out_feature_class = database + "/" + pointinfo + "_feature", out_geometry_type = "MULTIPOINT", average_point_spacing = avg_space)

	time.sleep(1.5)

	outIDW = arcpy.sa.Idw(database + "/" + pointinfo + "_feature", "Shape.Z", 0.15, 2, arcpy.sa.RadiusVariable(12))

	time.sleep(1.5)

	inRaster = database + "/" + pointinfo + "_feature"

	outputDir = r"C:\Users\lenovo\Desktop\rasters-batsmen" 
	outputFile = pointinfo + ".asc"
	outASCII = outputDir + "\\" + outputFile
	arcpy.RasterToASCII_conversion(outIDW, outASCII)
	
	time.sleep(1.5)
	print bowler_name
	
test = os.listdir(outputDir)

for item in test:
    if item.endswith(".xml"):
        os.remove(os.path.join(outputDir, item))