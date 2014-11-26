#!/usr/bin/env python
#
# Author: Jose Gomez-Dans, http://jgomezdans.github.io/
# https://gist.github.com/jgomezdans/808194

import sys
import os
from osgeo import ogr
from osgeo import osr

def buffer(infile,outfile,buffdist):
    try:
        ds_in=ogr.Open( infile )
        lyr_in=ds_in.GetLayer( 0 )
        drv=ds_in.GetDriver()
        if os.path.exists( outfile ):
            drv.DeleteDataSource(outfile)
        ds_out = drv.CreateDataSource( outfile )
    
        layer = ds_out.CreateLayer( lyr_in.GetLayerDefn().GetName(), \
            lyr_in.GetSpatialRef(), ogr.wkbPolygon)
        n_fields = lyr_in.GetLayerDefn().GetFieldCount()
        for i in xrange ( lyr_in.GetLayerDefn().GetFieldCount() ):
            field_in = lyr_in.GetLayerDefn().GetFieldDefn( i )
            fielddef = ogr.FieldDefn( field_in.GetName(), field_in.GetType() )   
            layer.CreateField ( fielddef )
        
        featuredefn = layer.GetLayerDefn()
        
        for feat in lyr_in:
            geom = feat.GetGeometryRef()
            #feature = ogr.Feature(featuredefn)
            #pdb.set_trace()
            feature = feat.Clone()
            feature.SetGeometry(geom.Buffer(float(buffdist)))
            #for in in xrange ( n_fields ):
                #feature.SetField ( 
            layer.CreateFeature(feature)
            del geom
        ds_out.Destroy()
    except:
        return False
    return True

if __name__=='__main__':
    usage='usage: buffer <infile> <outfile> <distance>'
    if len(sys.argv) == 4:
        if buffer(sys.argv[1],sys.argv[2],sys.argv[3]):
            print 'Buffer succeeded!'
            sys.exit(0)
        else:
            print 'Buffer failed!'
            sys.exit(1)
    else:
        print usage
        sys.exit(1)
