# A script to rasterise a shapefile to the same projection & pixel resolution as a reference image.
# Reference image is a satellite tile (.tif) we want to link to a NWB and the InputVector is a NWB shapefile

from osgeo import ogr, gdal
import os
import subprocess
import numpy as np

def rasterize(InputVector, InputVectorRB, RefImage, OutputImage):   
    gdalformat = 'GTiff'
    datatype = gdal.GDT_Byte
	##########################################################
	# Get projection info from reference image
    Image = gdal.Open(RefImage, gdal.GA_ReadOnly)
    #get rgb array of RefImage
    band = Image.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize
    rgb = np.dstack([Image.GetRasterBand(b).ReadAsArray() for b in (1,2,3)])
    x,y,z = rgb.shape    
	# Open Shapefile
    Shapefile = ogr.Open(InputVector)
    Shapefile_layer = Shapefile.GetLayer()
    burnVal = 200 #value for the output image pixels
    #Open RB Shapefile
    ShapefileRB = ogr.Open(InputVectorRB)
    ShapefileRB_layer = ShapefileRB.GetLayer()
    burnValRB = 1 #value for the output image pixels
	# Rasterise
    print("Rasterising shapefile...")
    Output = gdal.GetDriverByName(gdalformat).Create(OutputImage, Image.RasterXSize, Image.RasterYSize, 1, datatype, options=['COMPRESS=DEFLATE'])
    Output.SetProjection(Image.GetProjectionRef())
    Output.SetGeoTransform(Image.GetGeoTransform()) 
	# Write data to band 1
    Band = Output.GetRasterBand(1)
    Band.SetNoDataValue(255)
    gdal.RasterizeLayer(Output, [1], Shapefile_layer, burn_values=[burnVal])
    gdal.RasterizeLayer(Output, [1], ShapefileRB_layer, burn_values=[burnValRB])
	#if more than 7% of the RefImage is black, make same part of OutputImage black as well
    a = np.count_nonzero(rgb==0)
    if a >= (rgb.size*0.07):
        bw = Output.GetRasterBand(1).ReadAsArray()
    	#compare
        for i in range(x):
            for j in range(y):
                if max(rgb[i,j,:])==0:
                    bw[i,j]=0       
        Output.GetRasterBand(1).WriteArray(bw)	
	# Close datasets
    Band = None
    Output = None
    Image = None
    Shapefile = None
    # Build image overviews
    subprocess.call("gdaladdo --config COMPRESS_OVERVIEW DEFLATE "+OutputImage+" 2 4 8 16 32 64", shell=True)
    print("Done.")
 

#%% rasterize single file RefImage
    
#InputVector = r"NWB/ZuidHolland/ZuidHolland.shp"
#InputVectorRB = r"NWB/ZuidHolland/RB.shp"
#RefImage = r"satelliet/Rotterdam/tile_0_0.tif"
#OutputImage = r"os.path.join("NWB/NWB_"+RefImage.rsplit('/')[-1])"
#rasterize(InputVector, InputVectorRB, RefImage, OutputImage)
    
#%% rasterize multiple files in folder RefPath

InputVector = r"NWB/ZuidHolland/ZuidHolland.shp"
InputVectorRB = r"NWB/ZuidHolland/RB.shp"
RefPath = r"satelliet/Rotterdam"
for subdir, dirs, files in os.walk(RefPath):
  for name in files:
    if name.startswith('tile') and name.endswith('.tif'):
        RefImage = os.path.join(subdir+"/"+name)
        os.makedirs(r"NWB/"+RefPath.rsplit('/')[-1],exist_ok=True) #creates new folder for outputimages
        OutputImage = os.path.join("NWB/"+RefPath.rsplit('/')[-1]+"/NWB_"+name) #creates outputimage in new folder with same tile name
        rasterize(InputVector,InputVectorRB,RefImage,OutputImage)
           
print("All done.")
            
