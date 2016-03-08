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
			
			##### Flow accumulation tool!#####
			# Local variables:
			# DEM = "E:\\GIS\\Lab6\\Lab06Data.gdb\\DEM"
			# fill2 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fill2"
			# AnalysisMask = "E:\\GIS\\Lab6\\Lab06Data.gdb\\AnalysisMask"
			#mask_dem = "E:\\GIS\\Lab6\\Lab06Data.gdb\\mask_dem"
			Output_drop_raster = ""
			#fllowd = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fllowd"
			#flowaccum = "E:\\GIS\\Lab6\\Lab06Data.gdb\\flowaccum"
			#flowaccum_acre2 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\flowaccum_acre2"
			#fa_acre = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fa_acre"
			#reclass = "E:\\GIS\\Lab6\\Lab06Data.gdb\\reclass"
			#streams = "E:\\GIS\\Lab6\\Lab06Data.gdb\\streams"
			
			DEM =parameters[0].valueAsText
			AnalysisMask = parameters[1].valueAsText
			
			# Set Geoprocessing environments
			arcpy.env.snapRaster = "DEM"

			# Process: Fill
			# arcpy.gp.Fill_sa(DEM, fill2, "")
			fill2 = arcpy.sa.Fill(DEM)

			# Process: Polygon to Raster
			# arcpy.PolygonToRaster_conversion(AnalysisMask, "OBJECTID", mask_dem, "CELL_CENTER", "NONE", "40")
			mask_dem = arcpy.PolygonToRaster(AnalysisMask)
			
			# Process: Flow Direction
			tempEnvironment0 = arcpy.env.cellSize
			arcpy.env.cellSize = mask_dem
			tempEnvironment1 = arcpy.env.mask
			arcpy.env.mask = mask_dem
			fllowd = FlowDirection(fill2)
			arcpy.env.cellSize = tempEnvironment0
			arcpy.env.mask = tempEnvironment1

			# Process: Flow Accumulation
			flowaccum = FlowAccumulation(fllowd)

			# Process: Raster Calculator
			fa_acre = flowaccum * 40*40/43560


			# Process: Reclassify
			reclass = Reclassify(fa_acre, "Value", "0 785.63818370000001 NODATA;785.63818500000002 22533 1")

			# Process: Stream to Feature
			streams = StreamToFeature(reclass, fllowd, streams, "SIMPLIFY")
			
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
			######Impervious Areas Tool
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
			
			#####Impervious Regression Tool For NC
						
			# Local variables:
			fa_acre = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fa_acre"
			flowaccum_sqmi = "E:\\GIS\\Lab6\\Lab06Data.gdb\\flowaccum_sqmi"
			DIV_accum = "E:\\GIS\\Lab6\\Lab06Data.gdb\\DIV_accum"
			Input_raster_or_constant_value_2 = "100"
			Div01 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\Div01"
			recur_2 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_2"
			recur_2I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_2I"
			reclass_2I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\reclass_2I"
			fllowd = "E:\\GIS\\Lab6\\Lab06Data.gdb\\fllowd"
			stream_2V = "E:\\GIS\\Lab6\\Lab06Data.gdb\\stream_2V"
			recur_10 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_10"
			recur_10I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_10I"
			relcass_10I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\relcass_10I"
			stream_10V = "E:\\GIS\\Lab6\\Lab06Data.gdb\\stream_10V"
			recur_25 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_25"
			recur_25I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_25I"
			reclass_25I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\reclass_25I"
			stream_25V = "E:\\GIS\\Lab6\\Lab06Data.gdb\\stream_25V"
			recur_50 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_50"
			recur_50I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_50I"
			reclass_50I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\reclass_50I"
			streams_50V = "E:\\GIS\\Lab6\\Lab06Data.gdb\\streams_50V"
			recur_100 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_100"
			recur_100I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_100I"
			reclass_100I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\reclass_100I"
			streams_100V = "E:\\GIS\\Lab6\\Lab06Data.gdb\\streams_100V"
			recur_5_5 = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_5_5"
			recur_5I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\recur_5I"
			reclass_5I = "E:\\GIS\\Lab6\\Lab06Data.gdb\\reclass_5I"
			streams_5V = "E:\\GIS\\Lab6\\Lab06Data.gdb\\streams_5V"

			# Process: Raster Calculator
			arcpy.gp.RasterCalculator_sa("\"%fa_acre%\"*0.0015625", flowaccum_sqmi)

			# Process: Divide
			arcpy.gp.Divide_sa(DIV_accum, Input_raster_or_constant_value_2, Div01)

			# Process: Raster Calculator (7)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"**0.691)*144", recur_2)

			# Process: Raster Calculator (8)
			arcpy.gp.RasterCalculator_sa("7.87*(\"%flowaccum_sqmi%\"**.539)*(\"%Div01%\"**.686)*(\"%recur_2%\"**.290)", recur_2I)

			# Process: Reclassify
			arcpy.gp.Reclassify_sa(recur_2I, "Value", "0 40 NODATA;40 146 1", reclass_2I, "DATA")

			# Process: Stream to Feature
			arcpy.gp.StreamToFeature_sa(reclass_2I, fllowd, stream_2V, "SIMPLIFY")

			# Process: Raster Calculator (3)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"**.665)*334", recur_10)

			# Process: Raster Calculator (10)
			arcpy.gp.RasterCalculator_sa("22.7*(\"%flowaccum_sqmi%\"**.463)*(\"%Div01%\"**0.515)*(\"%recur_10%\"**0.289)", recur_10I)

			# Process: Reclassify (3)
			arcpy.gp.Reclassify_sa(recur_10I, "Value", "0 40 NODATA;40 527 1", relcass_10I, "DATA")

			# Process: Stream to Feature (2)
			arcpy.gp.StreamToFeature_sa(relcass_10I, fllowd, stream_10V, "SIMPLIFY")

			# Process: Raster Calculator (4)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"**.655)*467", recur_25)

			# Process: Raster Calculator (11)
			arcpy.gp.RasterCalculator_sa("28.5*(\"%flowaccum_sqmi%\"**0.390)*(\"%Div01%\"**.436)*(\"%recur_25%\"**0.338)", recur_25I)

			# Process: Reclassify (4)
			arcpy.gp.Reclassify_sa(recur_25I, "Value", "0 40 NODATA;40 963 1", reclass_25I, "DATA")

			# Process: Stream to Feature (3)
			arcpy.gp.StreamToFeature_sa(reclass_25I, fllowd, stream_25V, "SIMPLIFY")

			# Process: Raster Calculator (5)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"**.65)*581", recur_50)

			# Process: Raster Calculator (12)
			arcpy.gp.RasterCalculator_sa("37.4*(\"%flowaccum_sqmi%\"**0.391)*(\"%Div01%\"**0.396)*(\"%recur_50%\"**0.325)", recur_50I)

			# Process: Reclassify (5)
			arcpy.gp.Reclassify_sa(recur_50I, "Value", "0 40 NODATA;40 1297 1", reclass_50I, "DATA")

			# Process: Stream to Feature (4)
			arcpy.gp.StreamToFeature_sa(reclass_50I, fllowd, streams_50V, "SIMPLIFY")

			# Process: Raster Calculator (6)
			arcpy.gp.RasterCalculator_sa("(\"%flowaccum_sqmi%\"**.643)*719", recur_100)

			# Process: Raster Calculator (13)
			arcpy.gp.RasterCalculator_sa("48*(\"%flowaccum_sqmi%\"**0.392)*(\"%Div01%\"**0.358)*(\"%recur_100%\"**0.312)", recur_100I)

			# Process: Reclassify (6)
			arcpy.gp.Reclassify_sa(recur_100I, "Value", "0 40 NODATA;40 1687 1", reclass_100I, "DATA")

			# Process: Stream to Feature (5)
			arcpy.gp.StreamToFeature_sa(reclass_100I, fllowd, streams_100V, "SIMPLIFY")

			# Process: Raster Calculator (2)
			arcpy.gp.RasterCalculator_sa("(248*(\"%flowaccum_sqmi%\"**0.670))", recur_5_5)

			# Process: Raster Calculator (9)
			arcpy.gp.RasterCalculator_sa("16.3*(\"%flowaccum_sqmi%\"**.489)*(\"%Div01%\"**0.572)*(\"%recur_5_5%\"**0.286)", recur_5I)

			# Process: Reclassify (2)
			arcpy.gp.Reclassify_sa(recur_5I, "Value", "0 40 NODATA;40 340 1", reclass_5I, "DATA")

			# Process: Stream to Feature (6)
			arcpy.gp.StreamToFeature_sa(reclass_5I, fllowd, streams_5V, "SIMPLIFY")



			
			
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
		
