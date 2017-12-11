# Coal Ash Environmental Impact Model
# Imports
import arcpy

# Parameters

AOI = arcpy.GetParameterAsText(0)
HUC12 = arcpy.GetParameterAsText(1)
Rivers = arcpy.GetParameterAsText(2)
SoilData = arcpy.GetParameterAsText(3)
LandUse = arcpy.GetParameterAsText(4)
DEM = arcpy.GetParameterAsText(5)
output_folder = arcpy.GetParameterAsText(6)
species_attribute = arcpy.GetParameterAsText(2)
attribute_name = arcpy.GetParameterAsText(3)
presence_value = arcpy.GetParameterAsText(4)

#Outputfiles
AOIHUC12_shp = output_folder + "\\AOIHUC12.shp"

# Set Geoprocessing environments
arcpy.env.scratchWorkspace = arcpy.GetParameterAsText(5)
arcpy.env.workspace = arcpy.GetParameterAsText(6)

# Process: Clip HUC12 to AOI
arcpy.Clip_analysis(HUC12, AOI, arcpy.GetParameterAsText(3), "")
