import json
import pdb
from PIL import Image
import numpy as np

im_frame = Image.open(path_to_file + 'file.png')
np_frame = np.array(im_frame.getdata())
  
# Opening JSON file
with open('Snipaste_2023-02-21_12-13-00.json') as f:
    data = json.load(f) # list of dictionary

# keys:['content', 'rectMask', 'labels', 'labelLocation', 'contentType']
pdb.set_trace()

def json2png(png_file_name, json_file_name):
    with open(json_file_name) as f:
        json_data = json.load(f)
    im_frame = Image.open(png_file_name)
    np_frame = np.array(im_frame.getdata())
    pdb.set_trace()

json2png()