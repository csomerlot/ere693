#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

__copyright__ = "Copyright 2016, Chris Somerlot"
__credits__ = [""]
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Chris Somerlot"
__email__ = "csomerlot@gmail.com"
__status__ = "Testing"

import os, sys, shutil, arcpy
import traceback, time
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")

DEBUGGING = False

def log(message):
    arcpy.AddMessage(message)
    with file(sys.argv[0]+".log", 'a') as logFile:
        logFile.write("%s:\t%s\n" % (time.asctime(), message))
    
class Toolbox(object):
    def __init__(self):
        self.label = "WIP tools"
        self.alias = ""
        self.tools = [TopoHydro, ImpCov, Runoff, GetNEXRAD, ScenarioAnalysis]
        
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
            
        param3 = arcpy.Parameter(
            displayName="Existing vector stream to use to modify drainage",
            name="ExistingStreams",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)
        
        params = [ param0, param1, param2, param3 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            demPath = parameters[0].valueAsText
            
            arcpy.env.extent = demPath
            arcpy.env.snapRaster = parameters[1].valueAsText
            arcpy.env.cellSize = demPath

            dem = Raster(demPath)
            fill = Fill(dem)
            flowDirection = FlowDirection(fill)
            flowAccumulation = FlowAccumulation(flowDirection, "INTEGER")
            
            ## should set the workspace first, as geoprocessing env variable
            if DEBUGGING: flowAccumulation.save("flowaccumulation.tif") 

			
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
			
            # Local variables: define these by finding them in your workspace or getting them as tool parameters

            ## this code from Tom Arcuri
			arcpy.CalculateField_management(Impervious, "LENGTH", "1", "VB", "")
            arcpy.FeatureToRaster_conversion(Impervious__3_, "LENGTH", Imper_rast, "4")
            BlockStatistics(Imper_rast, block_rast, "Rectangle 10 10 CELL", "SUM", "DATA")
            Aggregate(block_rast, agg_rast, "10", "MEAN", "EXPAND", "DATA")
            FlowAccumulation(fllowd, imper_accum, agg_rast, "FLOAT")
            Divide(imper_accum, flowaccum, Divide__2_)
            Reclassify(Divide__2_, "Value", "0 10 1;10 20 2;20 30 3;30 40 4;40 50 5;50 60 6;60 70 7;70 80 8;80 90 9;90 100 10", reclass_imperv, "DATA")
            Times(reclass_imperv, reclass, imper_mult1)
            StreamToFeature(imper_mult1, fllowd, imperv_stream, "SIMPLIFY")
            RasterCalculator("\"%fa_acre%\"*0.0015625", flowaccum_sqmi)
            Divide(DIV_accum, Input_raster_or_constant_value_2, Div01)
            RasterCalculator("(\"%flowaccum_sqmi%\"**0.691)*144", recur_2)
			RasterCalculator("7.87*(\"%flowaccum_sqmi%\"**.539)*(\"%Div01%\"**.686)*(\"%recur_2%\"**.290)", recur_2I)
			Reclassify(recur_2I, "Value", "0 40 NODATA;40 146 1", reclass_2I, "DATA")
			StreamToFeature(reclass_2I, fllowd, stream_2V, "SIMPLIFY")
			RasterCalculator("(\"%flowaccum_sqmi%\"**.665)*334", recur_10)
			RasterCalculator("22.7*(\"%flowaccum_sqmi%\"**.463)*(\"%Div01%\"**0.515)*(\"%recur_10%\"**0.289)", recur_10I)
			Reclassify(recur_10I, "Value", "0 40 NODATA;40 527 1", relcass_10I, "DATA")
			StreamToFeature(relcass_10I, fllowd, stream_10V, "SIMPLIFY")
			RasterCalculator("(\"%flowaccum_sqmi%\"**.655)*467", recur_25)
			RasterCalculator("28.5*(\"%flowaccum_sqmi%\"**0.390)*(\"%Div01%\"**.436)*(\"%recur_25%\"**0.338)", recur_25I)
			Reclassify(recur_25I, "Value", "0 40 NODATA;40 963 1", reclass_25I, "DATA")
			StreamToFeature(reclass_25I, fllowd, stream_25V, "SIMPLIFY")
			RasterCalculator("(\"%flowaccum_sqmi%\"**.65)*581", recur_50)
			RasterCalculator("37.4*(\"%flowaccum_sqmi%\"**0.391)*(\"%Div01%\"**0.396)*(\"%recur_50%\"**0.325)", recur_50I)
			Reclassify(recur_50I, "Value", "0 40 NODATA;40 1297 1", reclass_50I, "DATA")
            StreamToFeature(reclass_50I, fllowd, streams_50V, "SIMPLIFY")
			RasterCalculator("(\"%flowaccum_sqmi%\"**.643)*719", recur_100)
			RasterCalculator("48*(\"%flowaccum_sqmi%\"**0.392)*(\"%Div01%\"**0.358)*(\"%recur_100%\"**0.312)", recur_100I)
			Reclassify(recur_100I, "Value", "0 40 NODATA;40 1687 1", reclass_100I, "DATA")
			StreamToFeature(reclass_100I, fllowd, streams_100V, "SIMPLIFY")
			RasterCalculator("(248*(\"%flowaccum_sqmi%\"**0.670))", recur_5_5)
			RasterCalculator("16.3*(\"%flowaccum_sqmi%\"**.489)*(\"%Div01%\"**0.572)*(\"%recur_5_5%\"**0.286)", recur_5I)
			Reclassify(recur_5I, "Value", "0 40 NODATA;40 340 1", reclass_5I, "DATA")
			StreamToFeature(reclass_5I, fllowd, streams_5V, "SIMPLIFY")
			
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

class GetNEXRAD(object):
    def __init__(self):
        self.label = "Get NEXRAD rainfall"
        self.description = "Get a raster of rainfall for a specific rain event from NEXRAD weather radar"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Start Date",
            name="startDate",
            datatype="GPDate",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        param1 = arcpy.Parameter(
            displayName="End Date",
            name="endDate",
            datatype="GPDate",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        param2 = arcpy.Parameter(
            displayName="Radar Station ID",
            name="radarID",
            datatype="DEString",
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
            log("Parameter is %s" % (parameters[0].valueAsText))
            
            # code for vector -> raster from Tyler Pitts
            lie=arcpy.CheckOutExtension ('Spatial')
            log ( lie )
            shapefiles=[]
            stormfolder=1
            while stormfolder<=4:
                log ( 'checking folder',stormfolder )
                shapefiles=[]
                for root, dirs, files in os.walk('storm'+str(stormfolder)):
                    for file in files:
                        if file.endswith('.shp'):
                                shapefiles.append('storm'+str(stormfolder)+'/'+file)
                log ( 'done creating an array of the shapefiles' )
                log ( 'converting to rasters' )
                rasters=[]
                for x in range(len(shapefiles)):
                    log ( 'converting',shapefiles[x] )
                    raster=arcpy.PolygonToRaster_conversion(shapefiles[x], 'value', 'storm'+str(stormfolder)+'/raster'+str(x), 'CELL_CENTER', 'NONE',0.00012196015)
                    rasters.append(raster)
                log ( 'completed raster conversion' )
                log ( 'calculating cell statistics' )
                maxreflect=CellStatistics (rasters, 'MAXIMUM', 'DATA')
                maxreflect.save('storm'+str(stormfolder)+'/reflect'+str(stormfolder)+'.tif')
                lowerLeft = arcpy.Point(maxreflect.extent.XMin,maxreflect.extent.YMin)
                cellSize = maxreflect.meanCellWidth
                reflectence=arcpy.RasterToNumPyArray(maxreflect)
                rows=len(reflectence)
                cols=len(reflectence[0])
                rainfallraster=numpy.zeros((rows,cols))
                for row in range(rows):
                    for col in range(cols):
                        if reflectence[row][col]<0:
                            rainfallraster[row][col]=0
                        rainfallraster[row][col]=(reflectence[row][col]/300)**(1/1.4)
                where_are_NaNs = numpy.isnan(rainfallraster)
                rainfallraster[where_are_NaNs]=0
                newraster=arcpy.NumPyArrayToRaster(rainfallraster,lowerLeft,cellSize)
                newraster.save('storm'+str(stormfolder)+'/rainfall'+str(stormfolder)+'.tif')
                stormfolder=stormfolder+1
                log ( 'completed rainfall calc' )
                log ( 'complete with folder',stormfolder )
            log ( 'finished making max reflectance rasters' )

        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
        
class ScenarioAnalysis(object):
    def __init__(self):
        self.label = "Scenario Analysis"
        self.description = "Compute a quantification of Watershed-wide Improvement based on BMP Buildout Scenario"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="BMP Points",
            name="bmppts",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        param1 = arcpy.Parameter(
            displayName="Status Field",
            name="statusField",
            datatype="Field",
            parameterType="Required",
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
            log("Parameter is %s" % (parameters[0].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
		
