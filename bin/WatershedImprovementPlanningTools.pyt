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
		
