import json
import requests 
from skimage.io import imsave
from skimage.exposure import rescale_intensity
from utils import stitchScene
from os.path import isfile
import pickle as pkl

url = 'https://api.planet.com/v0/orders/'
usr = '69c1c54d10324eb58c5677cc8737fc0c'
pss = 'ocbiYWN5S6D2'
r = requests.get(url, auth=(usr,pss))

print(r.headers)
#print(r.text) # or r.json()

data = json.loads(r.text)
#print(data)
for order in data:
    if not 'RapidEye' in order['products'][0]['item_id']:
        if order['name']=='ReferenceJul6':
            continue
        im_id = order['products'][0]['item_id'][0:15]
        if im_id=='20170929_175008':
            continue
        out_file = './rec_images/'+im_id+'.png'
        out_el = './elevation/'+im_id+'.pckl'
        out_info = './info/'+im_id+'.pckl'
        if isfile(out_file):
            continue 
        print(im_id)
        file_list = []
        for shot in order['products']:
            file_list.append('data/'+shot['item_id']+'/'+shot['item_id']+'_3B_Analytic.tif')
        im,grid,el,eldata = stitchScene(file_list,[10, 10]) 
        jsonfile = open('data/'+shot['item_id']+'/'+shot['item_id']+'_metadata.json').read()
        dataform = jsonfile.strip("'<>() ").replace('\'', '\"')
        struct = json.loads(dataform)
        pkl.dump(struct,open(out_info,"wb"))
        print(shot['item_id']+'/'+shot['item_id']+'_metadata.json')
        im_display = rescale_intensity(im,out_range=(0,255)).astype('uint8')
        imsave(out_file,im_display)
        pkl.dump(el, open( out_el, "wb" ) )
        print('Image saved in ' + out_file)
        print('Elevation data saved in ' + out_el)
