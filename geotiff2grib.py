#!/usr/bin/env python
import sys
import traceback

from grib_api import *

import gdal
from gdalconst import *

import numpy

def convert(in_file, out_file):
    template = grib_new_from_samples("regular_ll_sfc_grib2")
    fout = open(out_file, 'w')

    keys = {
        'dataDate': 20140130, # Last changed date from GSHHG
        'dataTime': 0000,
        'discipline': 2, # Land Surface products
        'parameterCategory': 0, # Vegetation/Biomass
        'parameterNumber': 0, # Land Cover (0=sea, 1=land)
        'significanceOfReferenceTime': 0, # Analysis
        'productionStatusOfProcessedData': 0, # Operational Products
        'typeOfProcessedData': 0, # Analysis
        'typeOfGeneratingProcess': 0, # Analysis
        'centre': 78, # DWD Offenbach
        'subCentre': 0, # Official... is that ok?
        'bitsPerValue': 1, # Only 0/1 possible
        'packingType': 'grid_simple',
    }

    dataset = gdal.Open(in_file, GA_ReadOnly)
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    geotransform = dataset.GetGeoTransform()
    # Assuming Plate Carree
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    # Assuming single band
    band = dataset.GetRasterBand(1)
    values = band.ReadAsArray(0, 0, cols, rows).astype(numpy.uint8)
    values = numpy.greater(values, 0)
    # Flatten the array into 1D, row-major mode ("C-like")
    values = values.flatten()

    keys.update({
        'Ni': cols,
        'Nj': rows,
        'latitudeOfFirstGridPointInDegrees': originY + pixelHeight/2,
        'longitudeOfFirstGridPointInDegrees': originX + pixelWidth/2,
        'latitudeOfLastGridPointInDegrees': originY + pixelHeight * rows - pixelHeight/2,
        'longitudeOfLastGridPointInDegrees': originX + pixelWidth * cols - pixelWidth/2,
        'iDirectionIncrementInDegrees': pixelWidth,
        'jDirectionIncrementInDegrees': pixelHeight,
    })

    out_grib = grib_clone(template)

    for key in keys:
        grib_set(out_grib, key, keys[key])

    grib_set_values(out_grib, values)
    grib_write(out_grib, fout)
    fout.close()

def main():
    if len(sys.argv) < 3:
        print >>sys.stderr, "Usage: {0} input.geotiff output.grib".format(sys.argv[0])
        return 1
    try:
        convert(sys.argv[1], sys.argv[2])
    except GribInternalError:
        traceback.print_exc(file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
