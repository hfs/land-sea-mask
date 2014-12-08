land-sea-mask
=============

Land sea mask which favors the sea in GeoTIFF and GRIB2 format.

Take coordinates, round them to 0.1°, look them up in the land sea mask and it will indicate whether there’s land or sea at this position. When the point is at the coast, i.e. there’s land *and* sea in the 0.1°×0.1° area, the answer will be *sea*.

The data is in equirectangular projection (“Plate Carrée”) for easy coordinate lookup.

Data Source
-----------

The data is based on [GSHHG – A Global Self-consistent, Hierarchical, High-resolution Geography Database][gshhg] (not included).

 [gshhg]: http://www.soest.hawaii.edu/pwessel/gshhg/

Usage
-----

These are instructions how to regenerate the land-sea-mask files from GSHHG.

Install unzip, [GDAL][gdal], the [GDAL Python bindings][pygdal] and the [GRIB API][grib] including its Python bindings. On Debian-based distributions the packages are called unzip, gdal-bin and python-gdal. The GRIB API has to be installed from source, because the package does not include the Python bindings.

Download the GSHHG .zip file from their website and place it in the same directory as the scripts.

Run the main script, which calls the other scripts

~~~~bash
./create_lsm.sh
~~~~

 [gdal]: http://gdal.org/
 [pygdal]: https://pypi.python.org/pypi/GDAL/
 [grib]: https://software.ecmwf.int/wiki/display/GRIB/
