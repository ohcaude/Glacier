import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.exposure import rescale_intensity
from skimage.filters import gaussian
from skimage.transform import rotate
import numpy as np
import subprocess
from scipy.interpolate import interp2d,griddata
from utils import plotRGBhistogram,dec2DMS,GetCornerCoordinates,getElevation,stitchScene,getShade

fname_elevation = '/Users/oriol/Downloads/ASTGTM2_N48W114/ASTGTM2_N48W114_dem.tif'


if True:
    folder = '/Users/oriol/planet_data/129618_scene/'
    fname_image = [folder+'20170928_17542'+str(c)+'_0e2f/20170928_17542'+str(c)+'_0e2f_3B_Analytic.tif' for c in [4,5,6,7,8,9]]
    jsonfile = open('/Users/oriol/planet_data/129618_scene/20170928_175427_0e2f/20170928_175427_0e2f_metadata.json').read()
    dataform = jsonfile.strip("'<>() ").replace('\'', '\"')
    struct = json.loads(dataform)
else:
    folder = '/Users/oriol/planet_data/129627_scene/'
    fname_image = [folder+'20170706_1744'+str(c)+'_103e/20170706_1744'+str(c)+'_103e_3B_Analytic.tif' for c in [45,46,47,48,49,51]]
    jsonfile = open('/Users/oriol/planet_data/129627_scene/20170706_174445_103e/20170706_174445_103e_metadata.json').read()
    dataform = jsonfile.strip("'<>() ").replace('\'', '\"')
    struct = json.loads(dataform)

#elevation = imread(fname_elevation)

im2,el,grid,eldata = stitchScene(fname_image,[10, 10])

sun_el = struct['properties']['sun_elevation']
sun_azimuth = struct['properties']['sun_azimuth']
sun = getShade(el,sun_el,sun_azimuth)

#gr = np.gradient(gaussian(rotate(el,sun_azimuth),sigma=2),10,axis=0)
#tan_ang = 180*np.arctan(gr)/np.pi
#plt.figure()
#plt.imshow(tan_ang)
#print(tan_ang.min())
#sun = np.zeros(tan_ang.shape)==0
#sun[np.where(tan_ang<(-sun_el))]=False
#detp = np.abs(np.gradient(poo,axis=0))
#plt.figure()
#plt.imshow(sun)
#plt.show()
#sun = np.zeros(detp.shape)==0
#for row,elr,tanr in zip(range(sun.shape[0]),el,tan_ang):
#    print(row/sun.shape[0])
#    cols = np.arange(0,sun.shape[1])
#    for col in cols[np.where(np.logical_not(sun[row,:]))]:
        #print(row,col)
        #print(el[row,col],tan_ang[row,col])
#        ray = -np.arange(row,sun.shape[0])*10*np.tan(sun_el*np.pi/180) + elr[col]
        #plt.figure()
        #plt.plot(ray)
        #plt.plot(el[row:,col])
        #plt.show()
        #input()
#        sun[row:,col]=np.logical_and(ray<el[row:,col],sun[row:,col])

#sun = rotate(sun,-sun_azimuth)
#inv rotate

im_display = rescale_intensity(im,out_range=(0,255),in_range=(im.min()*1.4,im.max()*0.6)).astype('uint8')
el_display = rescale_intensity(el,out_range=(0,255)).astype('uint8')




#mask = im_display
#for i in range(3):
#    aux = mask[:,:,i]
#    aux[np.where(sun)]=0

#print(lat_el,lon_el)
#print(lat_im,lon_im)
#plt.figure()
#plt.imshow(im_display)
#plt.figure()
#plt.imshow(sun)
#plt.figure()
#plt.imshow(mask)
#plt.show()



# remember 46 70 90
