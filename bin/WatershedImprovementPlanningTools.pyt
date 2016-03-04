#Tom Arcuri
#Python Tool box

import os, sys, shutil, arcpy
import traceback, time

def log(message):
    arcpy.AddMessage(message)
    with file(sys.argv[0]+".log", 'a') as logFile:
        logFile.write("%s:\t%s\n" % (time.asctime(), message))
    
class Toolbox(object):
    def __init__(self):
        self.label = "WIP tools"
        self.alias = ""
        self.tools = [TopoHydro, ImpCov, Runoff]
        
class TopoHydro(object):
    def __init__(self):
        self.label = "Topography and Hydrology Analysis"
        self.description = "Establishes the watershed and stream network"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Digital Elevation Model",
            name="DEM",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Analysis Mask",
            name="Mask",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        param2 = arcpy.Parameter(
            displayName="Threshold accumulation for Stream formation (acres)",
            name="StreamFormation",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1, param2 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameters are %s, %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText))
			
			# Local variables:
			DEM = "E:\\GIS\\Lab6\\Lab06Data.gdb\\DEM"
			fill2 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fill2"
			AnalysisMask = "E:\\GIS\\Lab6\\Lab06Data.gdb\\AnalysisMask"
			mask_dem = "E:\\GIS\\Lab6\\Lab06Data.gdb\\mask_dem"
			Output_drop_raster = ""
			fllowd = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fllowd"
			flowaccum = "E:\\GIS\\Lab6\\Lab06Data.gdb\\flowaccum"
			flowaccum_acre2 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\flowaccum_acre2"
			fa_acre = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fa_acre"
			reclass = "E:\\GIS\\Lab6\\Lab06Data.gdb\\reclass"
			streams = "E:\\GIS\\Lab6\\Lab06Data.gdb\\streams"

			# Set Geoprocessing environments
			arcpy.env.snapRaster = "DEM"

			# Process: Fill
			arcpy.gp.Fill_sa(DEM, fill2, "")

			# Process: Polygon to Raster
			arcpy.PolygonToRaster_conversion(AnalysisMask, "OBJECTID", mask_dem, "CELL_CENTER", "NONE", "40")

			# Process: Flow Direction
			tempEnvironment0 = arcpy.env.cellSize
			arcpy.env.cellSize = mask_dem
			tempEnvironment1 = arcpy.env.mask
			arcpy.env.mask = mask_dem
			arcpy.gp.FlowDirection_sa(fill2, fllowd, "NORMAL", Output_drop_raster)
			arcpy.env.cellSize = tempEnvironment0
			arcpy.env.mask = tempEnvironment1

			# Process: Flow Accumulation
			arcpy.gp.FlowAccumulation_sa(fllowd, flowaccum, "", "FLOAT")

			# Process: Raster Calculator
			arcpy.gp.RasterCalculator_sa("\"%flowaccum%\"*40*40", flowaccum_acre2)

			# Process: Raster Calculator (2)
			arcpy.gp.RasterCalculator_sa("\"%flowaccum_acre2%\"/43560", fa_acre)

			# Process: Reclassify
			arcpy.gp.Reclassify_sa(fa_acre, "Value", "0 785.63818370000001 NODATA;785.63818500000002 22533 1", reclass, "DATA")

			# Process: Stream to Feature
			arcpy.gp.StreamToFeature_sa(reclass, fllowd, streams, "SIMPLIFY")
					except Exception as err:
						log(traceback.format_exc())
						log(err)
						raise err
					return

class ImpCov(object):
    def __init__(self):
        self.label = "Imperviousness Analysis"
        self.description = "Impervious area contributions"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Impervious Areas",
            name="ImperviousAreas",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Lakes",
            name="Lakes",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameters are %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText))
			
			# Local variables:
			fllowd = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fllowd"
			Impervious = "E:\\GIS\\Lab6\\Lab06Data.gdb\\Impervious"
			Impervious__3_ = Impervious
			Imper_rast = "E:\\GIS\\Lab6\\Lab06Data.gdb\\Imper_rast"
			block_rast = "E:\\GIS\\Lab6\\Lab06Data.gdb\\block_rast"
			agg_rast = "E:\\GIS\\Lab6\\Lab06Data.gdb\\agg_rast"
			imper_accum = "E:\\GIS\\Lab6\\Lab06Data.gdb\\imper_accum"
			flowaccum = "E:\\GIS\\Lab6\\Lab06Data.gdb\\flowaccum"
			Divide__2_ = "\\\\hd.ad.syr.edu\\02\\9b1dc2\\Documents\\ArcGIS\\Default.gdb\\Divide"
			reclass_imperv = "E:\\GIS\\Lab6\\Lab06Data.gdb\\reclass_imperv"
			reclass = "E:\\GIS\\Lab6\\Lab06Data.gdb\\reclass"
			imper_mult1 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\imper_mult1"
			imperv_stream = "E:\\GIS\\Lab6\\Lab06Data.gdb\\imperv_stream"

			# Process: Calculate Field
			arcpy.CalculateField_management(Impervious, "LENGTH", "1", "VB", "")

			# Process: Feature to Raster
			arcpy.FeatureToRaster_conversion(Impervious__3_, "LENGTH", Imper_rast, "4")

			# Process: Block Statistics
			arcpy.gp.BlockStatistics_sa(Imper_rast, block_rast, "Rectangle 10 10 CELL", "SUM", "DATA")

			# Process: Aggregate
			arcpy.gp.Aggregate_sa(block_rast, agg_rast, "10", "MEAN", "EXPAND", "DATA")

			# Process: Flow Accumulation
			arcpy.gp.FlowAccumulation_sa(fllowd, imper_accum, agg_rast, "FLOAT")

			# Process: Divide
			arcpy.gp.Divide_sa(imper_accum, flowaccum, Divide__2_)

			# Process: Reclassify
			arcpy.gp.Reclassify_sa(Divide__2_, "Value", "0 10 1;10 20 2;20 30 3;30 40 4;40 50 5;50 60 6;60 70 7;70 80 8;80 90 9;90 100 10", reclass_imperv, "DATA")

			# Process: Times
			arcpy.gp.Times_sa(reclass_imperv, reclass, imper_mult1)

			# Process: Stream to Feature
			arcpy.gp.StreamToFeature_sa(imper_mult1, fllowd, imperv_stream, "SIMPLIFY")

			# Local variables:
			fa_acre = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fa_acre"
			flowaccum_sqmi = "E:\\GIS\\Lab6\\Lab06Data.gdb\\flowaccum_sqmi"
			imper_accum = "E:\\GIS\\Lab6\\Lab06Data.gdb\\imper_accum"
			recur_2 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_2"
			recur_2I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_2I"
			recur_5 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_5"
			recur_5I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_5I"
			recur_10 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_10"
			recur_10I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_10I"
			recur_25 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_25"
			recur_25I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_25I"
			recur_50 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_50"
			recur_50I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_50I"
			recur_100 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_100"
			recur_100I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_100I"

			# Process: Raster Calculator
			arcpy.gp.RasterCalculator_sa("\"%fa_acre%\"*0.0015625", flowaccum_sqmi)

			# Process: Raster Calculator (7)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"^0.691)*144", recur_2)

			# Process: Raster Calculator (8)
			arcpy.gp.RasterCalculator_sa("7.87*(\"%flowaccum_sqmi%\"^.539)*(\"%imper_accum%\"^.686)*(\"%recur_2%\"^.290)", recur_2I)

			# Process: Raster Calculator (2)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"^.67)*248", recur_5)

			# Process: Raster Calculator (9)
			arcpy.gp.RasterCalculator_sa("16.3*(\"%flowaccum_sqmi%\"^.489)*(\"%imper_accum%\"^0.572)*(\"%recur_5%\"^0.286)", recur_5I)

			# Process: Raster Calculator (3)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"^.665)*334", recur_10)

			# Process: Raster Calculator (10)
			arcpy.gp.RasterCalculator_sa("22.7*(\"%flowaccum_sqmi%\"^.463)*(\"%imper_accum%\"^0.515)*(\"%recur_10%\"^0.289)", recur_10I)

			# Process: Raster Calculator (4)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"^.655)*467", recur_25)

			# Process: Raster Calculator (11)
			arcpy.gp.RasterCalculator_sa("28.5*(\"%flowaccum_sqmi%\"^0.390)*(\"%imper_accum%\"^.436)*(\"%recur_25%\"^0.338)", recur_25I)

			# Process: Raster Calculator (5)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"^.65)*581", recur_50)

			# Process: Raster Calculator (12)
			arcpy.gp.RasterCalculator_sa("37.4*(\"%flowaccum_sqmi%\"^0.391)*(\"%imper_accum%\"^0.396)*(\"%recur_50%\"^0.325)", recur_50I)

			# Process: Raster Calculator (6)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"^.643)*719", recur_100)

			# Process: Raster Calculator (13)
			arcpy.gp.RasterCalculator_sa("48*(\"%flowaccum_sqmi%\"^0.392)*(\"%imper_accum%\"^0.358)*(\"%recur_100%\"^0.312)", recur_100I)



        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
        
class Runoff(object):
    def __init__(self):
        self.label = "Runoff Calculations"
        self.description = "Calculation of standard storm flows via USGS regression equations"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Curve Number",
            name="Landuse",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameter is %s" % (parameters[0].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
		
