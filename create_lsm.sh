#!/bin/sh
BASEDIR=$(dirname "$0")
unzip -o gshhg-shp-2.3.0.zip "GSHHS_shp/i/GSHHS_i_L1.*" "GSHHS_shp/i/GSHHS_i_L2.*"
$BASEDIR/shp2geotiff.sh
$BASEDIR/geotiff2grib.py lsm.geotiff lsm.grib2
