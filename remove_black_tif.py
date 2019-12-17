#script to removes totally black .tif files

import os, gdal   
import numpy as np

#end with /
path = r"satelliet/Rotterdam/" 

for file in os.listdir(path):
    if file.startswith('tile') and file.endswith('.tif'):
        ds = gdal.Open(os.path.join(path+file))
        band = ds.GetRasterBand(1)
        xsize = band.XSize
        ysize = band.YSize

        rgb = np.stack([ds.GetRasterBand(b).ReadAsArray() for b in (1,2,3)])
        rgb = np.reshape(rgb,(xsize,ysize,3))

        #delete if max pixel color code is 0 (black)
        if rgb.max()==0:
            print("delete black picture ", file)
            ds = None
            os.remove(os.path.join(path+file))
            
            
    