#!/bin/sh
gdal_rasterize -te -180.05 -90.05 180.05 90.05 -tr 0.1 0.1 -burn 255 -ot Byte -init 0 -at -i -tap -a_srs "$(cat EPSG32663.wkt)" GSHHS_shp/i/GSHHS_i_L1.shp lsm_L1.geotiff

# Manually apply buffer of -0.05° to L2

# TODO: Need to combine separate GeoTIFFs afterwards?
gdal_rasterize -te -180.05 -90.05 180.05 90.05 -tr 0.1 0.1 -burn 255 -ot Byte -at -tap -a_srs "$(cat EPSG32663.wkt)" GSHHS_i_L2_-buffer.shp lsm_L2.geotiff
