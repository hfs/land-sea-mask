#!/bin/sh
BASEDIR=$(dirname "$0")

# Use 254, because 255 is the default value for NaN
gdal_rasterize -te -180.05 -90.05 180.05 90.05 -tr 0.1 0.1 -burn 254 -ot Byte -init 0 -at -i -a_srs "$(cat $BASEDIR/EPSG32663.wkt)" GSHHS_shp/i/GSHHS_i_L1.shp lsm_L1.geotiff

$BASEDIR/buffer.py GSHHS_shp/i/GSHHS_i_L2.shp GSHHS_i_L2_-buffer.shp -0.05

gdal_rasterize -te -180.05 -90.05 180.05 90.05 -tr 0.1 0.1 -burn 254 -ot Byte -at -a_srs "$(cat $BASEDIR/EPSG32663.wkt)" GSHHS_i_L2_-buffer.shp lsm_L2.geotiff

gdal_calc.py --calc 'A+B' -A lsm_L1.geotiff -B lsm_L2.geotiff --overwrite --outfile=lsm.geotiff
