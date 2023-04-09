import json
import pdb
import os
from PIL import Image
import cv2
import shutil
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
'''
window -- window
Molding -- floor
shop -- shop
Balcony -- railing
facade -- wall
facade -- mountainwall
pillar -- column
pillar -- base
'''

label2num = {
    'window': 3,
    'floor': 10,
    'shop': 9,
    'railing': 7,
    'wall': 2,
    'mountainwall': 13,
    'column': 11,
    'base':14
}


def json2png(png_file_name, json_file_name, out_file_name):
    # 读取json文件
    with open(json_file_name) as f:
        json_data = json.load(f) # 这里的json_data是一个列表，每个元素是一个字典，包含标注的区域信息
    
    # 获取png格式文件，根据新的json格式改了
    img = cv2.imread(png_file_name)
    
    # 根据png的尺寸创建画布，默认label为1
    # canvas = np.ones(im_frame.size)
    # pdb.set_trace()
    img = np.ones((img.shape[0], img.shape[1]))
    # 遍历标注区域
    for label in json_data['shapes']:
        # label的keys:['content', 'rectMask', 'labels', 'labelLocation', 'contentType']
        ## label改变了，变成【‘label'，’points'】了
        # 获取标注区域的起点与长宽，由于json文件的区域是float类型，但是下标只支持int类型，所以做类型转化（会影响精度）

        # *********************************** highly matters!! *****************************
        # pdb.set_trace()
        points = [[int(x[1]), int(x[0])] for x in label["points"]]
        # pdb.set_trace()
        # 根据起点、长宽信息对区域做打标，默认打标为100，可改
        label_tag = label['label']
        # pdb.set_trace()
        img = cv2.fillConvexPoly(img, np.array(points), label2num[label_tag]) 
        # pdb.set_trace()
        # *********************************** highly matters!! *****************************
    
    # np array和Image读取的长宽定义不一样，做个转置
    im = Image.fromarray(img.T).convert("L")
    im.save('{}.png'.format(out_file_name))
    
# 主函数，调用json2png函数
### 用这个测试一下子，把下面的注释了
# json2png('Snipaste_2023-02-21_12-59-54.png', 'Snipaste_2023-02-21_12-59-54.json', 'test')
g = os.walk("D:\Code\\facade_seg-main\\04_Code\original")

new_path_image = "D:\Code\\facade_seg-main\\04_Code\original_img"
new_path_anote = "D:\Code\\facade_seg-main\\04_Code\original_anote"

for path, dir_list, file_list in g:
    for file_name in tqdm(file_list):
        file_path = os.path.join(path,file_name)
        # pdb.set_trace()
        if file_name[-4:] == 'json':
            json2png(file_path[:-4] + 'png', file_path, os.path.join(new_path_anote, file_name[:-5]))
            shutil.copy(file_path[:-4] + 'png', os.path.join(new_path_image, file_name[:-4] + 'jpg'))
            
