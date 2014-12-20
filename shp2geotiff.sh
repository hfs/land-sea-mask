#!/bin/sh
BASEDIR=$(dirname "$0")

gdal_rasterize -te -0.05 -90.05 360.05 90.05 -tr 0.1 0.1 -burn 1 -ot Byte -init 0 -at -i -a_srs "$(cat $BASEDIR/EPSG32663.wkt)" -co NBITS=1 -co COMPRESS=LZW GSHHS_shp/i/GSHHS_i_L1.shp lsm_L1_east.geotiff
gdal_rasterize -te -360.05 -90.05 0.05 90.05 -tr 0.1 0.1 -burn 1 -ot Byte -init 0 -at -i -a_srs "$(cat $BASEDIR/EPSG32663.wkt)" -co NBITS=1 -co COMPRESS=LZW GSHHS_shp/i/GSHHS_i_L1.shp lsm_L1_west.geotiff

$BASEDIR/buffer.py GSHHS_shp/i/GSHHS_i_L2.shp GSHHS_i_L2_-buffer.shp -0.05

gdal_rasterize -te -0.05 -90.05 360.05 90.05 -tr 0.1 0.1 -burn 1 -ot Byte -at -a_srs "$(cat $BASEDIR/EPSG32663.wkt)" -co NBITS=1 -co COMPRESS=LZW GSHHS_i_L2_-buffer.shp lsm_L2_east.geotiff
gdal_rasterize -te -360.05 -90.05 0.05 90.05 -tr 0.1 0.1 -burn 1 -ot Byte -at -a_srs "$(cat $BASEDIR/EPSG32663.wkt)" -co NBITS=1 -co COMPRESS=LZW GSHHS_i_L2_-buffer.shp lsm_L2_west.geotiff

gdal_calc.py --calc 'logical_or(logical_and(A, B), logical_or(C, D))' -A lsm_L1_west.geotiff -B lsm_L1_east.geotiff -C lsm_L2_west.geotiff -D lsm_L2_east.geotiff --creation-option='NBITS=1' --creation-option='COMPRESS=LZW' --overwrite --outfile=lsm.geotiff
