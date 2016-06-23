import time, os
print os.getcwd()

import numpy, arcpy
arcpy.env.overwriteOutput = True
print "Running"

from bmpFlowModFast import *

flowdir = arcpy.Raster('testFlowdir.tif')
weight = arcpy.Raster('testWght.tif')
lowerLeft = arcpy.Point(flowdir.extent.XMin,flowdir.extent.YMin)
cellSize = flowdir.meanCellWidth

start = time.time()
nflowdir = arcpy.RasterToNumPyArray(flowdir, nodata_to_value=0)
nweight = arcpy.RasterToNumPyArray(weight, nodata_to_value=0)

arr = flowAccumulate(nflowdir.astype(numpy.int), nweight.astype(numpy.double))

newRaster = arcpy.NumPyArrayToRaster(arr, lowerLeft, cellSize, value_to_nodata=0)
newRaster.save(os.path.join(os.getcwd(), "testOutput.tif"))
print "Took %6.2f seconds" % (time.time()-start)
raw_input("Press any key to continue . . . ")