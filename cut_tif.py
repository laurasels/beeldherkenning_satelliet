#script to cut .tif files in smaller .tif files of tile_size_x by tile_size_y

#gdal package can be tricky, if the following returns a number, gdal should be working correctly
#md = gdal.GetDriverByName('GTiff').GetMetadata()
#md['DMD_CREATIONOPTIONLIST'].find('BigTIFF')

import os, gdal

in_path =r"satelliet/Rotterdam/Rotterdam.tif" #the file you want to cut
out_path = r"satelliet/Rotterdam/tile_" #output folder of the cutted tif files

tile_size_x = 1000 #size of pixels x
tile_size_y = 1000 #size of pixels y

ds = gdal.Open(in_path)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize

for i in range(0, xsize, tile_size_x):
    for j in range(0, ysize, tile_size_y):
        com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + " " + str(out_path) + str(i) + "_" + str(j) + ".tif"
        os.system(com_string)
       