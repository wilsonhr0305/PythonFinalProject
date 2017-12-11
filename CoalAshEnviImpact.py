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
input_folder = arcpy.GetParameterAsText(6)
output_folder = arcpy.GetParameterAsText(7)

# Set Geoprocessing environments
arcpy.env.scratchWorkspace = input_folder
arcpy.env.workspace = output_folder

#Outputfiles
AOIHUC12_shp = input_folder + "\\AOIHUC12.shp"
AOIStreams_shp = input_folder + "\\AOIStreams.shp"
AOISoil_shp = input_folder + "\\AOISoil.shp"
AOIHUC12_shp = input_folder + "\\AOIHUC12.shp"
AOIStreams_shp = input_folder + "\\AOIStreams.shp"
AOISoil_shp = input_folder + "\\AOISoil.shp"
AOILU2011 = input_folder + "\\AOILU2011"
AOIDEM10m = input_folder + "\\AOIDEM10m"
AOIStreamDis = output_folder + "\\AOIStreamDis"
AOISlope = output_folder + "\\AOISlope"
AOIDrainage_tif = output_folder + "\\AOIDrainage.tif"
AOIPerm_tif = output_folder + "\\AOIPerm.tif"
AOIDrnWt_tif = output_folder + "\\AOIDrnWt.tif"
Extract_AOIStre1_tif = output_folder + "\\Extract_AOIStre1.tif"
CoalAshSever = output_folder + "\\CoalAshSever"
AOIPermWt_tif = output_folder + "\\AOIPermWt.tif"
Reclass_Extract1_tif = output_folder + "\\Reclass_Extract1.tif"
AOILUReclass = output_folder + "\\AOILUReclass"
AOISlopRecl = output_folder + "\\AOISlopRecl"
CoalAshImpact = output_folder + "\\CoalAshImpact"

# Process: Initial Clip and Extract
arcpy.Clip_analysis(HUC12, AOI, AOIHUC12_shp, "")
arcpy.Clip_analysis(Rivers, AOI, AOIStreams_shp, "")
arcpy.Clip_analysis(SoilData, AOI, AOISoil_shp, "")
arcpy.gp.ExtractByMask_sa(LandUse, AOI, AOILU2011)
arcpy.gp.ExtractByMask_sa(DEM, AOI, AOIDEM10m)

# Process: Polygon to Raster
arcpy.PolygonToRaster_conversion(AOISoil_shp, "DRAINAGE", AOIDrainage_tif, "CELL_CENTER", "NONE", "10")
arcpy.PolygonToRaster_conversion(AOISoil_shp, "PERML", AOIPerm_tif, "CELL_CENTER", "NONE", "10")

# Process: Euclidean Distance
arcpy.gp.EucDistance_sa(AOIStreams_shp, AOIStreamDis, "", "10", "")

# Process: Slope
arcpy.gp.Slope_sa(AOIDEM10m, AOISlope, "DEGREE", "1", "PLANAR", "METER")

#Process: Extract
arcpy.gp.ExtractByMask_sa(AOIStreamDis, AOI, Extract_AOIStre1_tif)

# Process: Reclassify (5)
arcpy.gp.Reclassify_sa(AOIDrainage_tif, "DRAINAGE", "W 6;' ' 3;MW 4;E 8;SP 7", AOIDrnWt_tif, "DATA")
arcpy.gp.Reclassify_sa(AOIPerm_tif, "PERML", "0.60 1;2.00 2;' ' 3", AOIPermWt_tif, "DATA")
arcpy.gp.Reclassify_sa(Extract_AOIStre1_tif, "VALUE", "0 117.046997 8;117.046997 242.074371 7;242.074371 373.630829 6;373.630829 520.384460 5;520.384460 693.757874 4;693.757874 936.482788 3;936.482788 1712.921509 2", Reclass_Extract1_tif, "DATA")
arcpy.gp.Reclassify_sa(AOILU2011, "VALUE", "11 9;21 4;22 5;23 7;24 8;31 6;41 5;42 4;43 5;52 6;71 4;81 8;82 8;90 8;95 9", AOILUReclass, "DATA")
arcpy.gp.Reclassify_sa(AOISlope, "VALUE", "0 2.634370 8;2.634370 5.987205 6;5.987205 10.058504 4;10.058504 14.608779 3;14.608779 19.877519 4;19.877519 26.583188 6;26.583188 61.308975 8", AOISlopRecl, "DATA")


# Process: Weighted Sum
arcpy.gp.WeightedSum_sa("AOILUReclass VALUE 1; AOISlopRecl VALUE 1;AOIDrnWt.tif Value 1;AOIPermWt.tif VALUE 1;Reclass_Extract1.tif VALUE 1", CoalAshImpact)





