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

def plotRGBhistogram(im,bins,ranges=False):
    if not ranges:
        ranges = [(np.min(im[:,:,0].flatten()),np.max(im[:,:,0].flatten())),(np.min(im[:,:,1].flatten()),np.max(im[:,:,1].flatten())),(np.min(im[:,:,2].flatten()),np.max(im[:,:,2].flatten()))]
    colors = ['red','green','blue']
    for ch in range(3):
        h,b = np.histogram(im[:,:,ch].flatten(),bins=bins,range=ranges[ch])
        plt.plot(b[0:-1],h,color=colors[ch])

def dec2DMS(DMSstr):
    data1 = DMSstr.split('d')
    val = float(data1[0])
    data2 = data1[1].split('\'')
    val += float(data2[0])/60.0
    data3 = data2[1].split('\"')
    val += float(data3[0])/3600.0
    if data3[1]=='W' or data3[1]=='S':
        val = -val
    return val

def GetCornerCoordinates(FileName):
    GdalInfo = subprocess.check_output(['gdalinfo',FileName])
    tokens = GdalInfo.decode().split('\n')
    CornerLats, CornerLons = [[]]*5,[[]]*5
    GotUL, GotUR, GotLL, GotLR, GotC = False, False, False, False, False
    for c,line in zip(range(len(tokens)),tokens):
        if line[:10] == 'Upper Left':
            CornerLons[0], CornerLats[0] = line.split('(')[2].split(')')[0].split(', ') 
            GotUL = True
        if line[:10] == 'Lower Left':
            CornerLons[1], CornerLats[1] = line.split('(')[2].split(')')[0].split(', ') 
            GotLL = True
        if line[:11] == 'Upper Right':
            CornerLons[2], CornerLats[2] = line.split('(')[2].split(')')[0].split(', ') 
            GotUR = True
        if line[:11] == 'Lower Right':
            CornerLons[3], CornerLats[3] = line.split('(')[2].split(')')[0].split(', ') 
            GotLR = True
        if line[:6] == 'Center':
            CornerLons[4], CornerLats[4] = line.split('(')[2].split(')')[0].split(', ') 
            GotC = True
        if GotUL and GotUR and GotLL and GotLR and GotC:
            break
    dCornerLats = [dec2DMS(d) for d in CornerLats]
    dCornerLons = [dec2DMS(d) for d in CornerLons]
    return dCornerLats, dCornerLons

def getElevation():
    lat,lon = GetCornerCoordinates('/Users/oriol/Downloads/ASTGTM2_N48W114/ASTGTM2_N48W114_dem.tif')
    eldata = imread('/Users/oriol/Downloads/ASTGTM2_N48W114/ASTGTM2_N48W114_dem.tif')
    latp = np.linspace(max(lat),min(lat),eldata.shape[0])
    lonp = np.linspace(min(lon),max(lon),eldata.shape[1])
    f = interp2d(lonp,latp,eldata)
    print(latp)
    print(lonp)
    return f,eldata

def stitchScene(image_files,resolution):
    lats = []
    lons = []
    resolution[0] = resolution[0]*2.869874928436339e-05/3 # conversion meter to deg
    resolution[1] = resolution[1]*4.157787785588867e-05/3 # conversion meter to deg
    for f in image_files:
        lat, lon = GetCornerCoordinates(f)
        lats += lat
        lons += lon
    lat_grid = np.mgrid[max(lats):min(lats):-resolution[0]]
    lon_grid = np.mgrid[min(lons):max(lons):resolution[1]]
    #lat_grid = np.linspace(max(lat),min(lat),resolution)
    #lon_grid = np.linspace(max(lon),min(lon),resolution)
    imnew = np.zeros((lat_grid.size,lon_grid.size,3))
    weights = np.zeros((lat_grid.size,lon_grid.size))
    print(imnew.shape)
    for c,f in zip(range(len(image_files)),image_files):
        print(f)
        lat,lon = GetCornerCoordinates(f)
        imshot = imread(f)
        print(imshot.shape)
        latp = np.linspace(max(lat),min(lat),imshot.shape[0])
        lonp = np.linspace(min(lon),max(lon),imshot.shape[1])
        for ch in range(imshot.shape[-1]):
            f = interp2d(lonp,latp,imshot[:,:,ch])
            aux = f(lon_grid,lat_grid)
            imnew[:,:,ch] += aux
        weights[np.where(aux>0)] += 1
    weights = np.stack((weights,weights,weights),axis=-1)
    weights[np.where(weights==0)]=1
    
    elF,eldata = getElevation()
    elevation = np.flip(elF(lon_grid,lat_grid),axis=0)
    return np.flip(np.divide(imnew,weights),axis=0),elevation,(lat_grid,lon_grid),eldata

def getShade(el,sun_elevation,sun_azimuth):
    gr = np.gradient(gaussian(rotate(el,sun_azimuth),sigma=2),10,axis=0)
    tan_ang = 180*np.arctan(gr)/np.pi
    sun = np.zeros(tan_ang.shape)==0
    sun[np.where(tan_ang<(-sun_elevation))]=False
    for row,elr,tanr in zip(range(sun.shape[0]),el,tan_ang):
        print(row/sun.shape[0])
        cols = np.arange(0,sun.shape[1])
        for col in cols[np.where(np.logical_not(sun[row,:]))]:
            ray = -np.arange(row,sun.shape[0])*10*np.tan(sun_elevation*np.pi/180) + elr[col]
            sun[row:,col]=np.logical_and(ray<el[row:,col],sun[row:,col])
    sun = rotate(sun,-sun_azimuth)
    return sun

