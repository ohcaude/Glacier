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
import os

directory_name = './rec_images/'
snow_area = []
datetime = []
for filename in os.listdir(directory_name):
    im = imread(directory_name+filename)
    snow = np.zeros(im.shape)
    snow[np.where(im>120)]=1
    area = np.sum(snow)/3
    snow_area.append(area)
    datetime.append(pd.to_datetime(filename[0:15], format='%Y%m%d_%H%M%S') )
    print((filename[0:15],area))
    #plotRGBhistogram(im,bins=256)
    #im_display = rescale_intensity(im,out_range=(0,255),in_range=(10,120)).astype('uint8')
    #plt.figure()
    #plt.imshow(im_display)
    #plt.figure()
    #plt.imshow(snow)
    #plt.show()
#im_display = rescale_intensity(im,out_range=(0,255),in_range=(im.min()*1.4,im.max()*0.6)).astype('uint8')

df = pd.DataFrame({'Datetime':datetime,'snow':snow_area})
print(df)
df.plot()
plt.show()
