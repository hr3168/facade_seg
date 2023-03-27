import json
import pdb
import os
from PIL import Image
import shutil
import numpy as np
from tqdm import tqdm
import cv2 
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
    
    # 获取png格式
    # im_frame = Image.open(png_file_name)
    img = cv2.imread(png_file_name)
    
    # 根据png的尺寸创建画布，默认label为1
    # canvas = np.ones(im_frame.size)
    canvas = np.ones((img.shape[0], img.shape[1]))
    pdb.set_trace()
    # 遍历标注区域
    for label in json_data['shapes']:
        # label的keys:['content', 'rectMask', 'labels', 'labelLocation', 'contentType']
        # 获取标注区域的起点与长宽，由于json文件的区域是float类型，但是下标只支持int类型，所以做类型转化（会影响精度）
        # x_min = int(label['rectMask']['xMin'])
        # y_min = int(label['rectMask']['yMin'])
        # width = int(label['rectMask']['width'])
        # height = int(label['rectMask']['height'])
        label_tag = label["label"]
        points = label["points"]
        canvas = cv2.fillConvexPoly(canvas, points, label2num[label_tag])
        # pdb.set_trace()
        # 根据起点、长宽信息对区域做打标，默认打标为100，可改
        # label_tag = label['shapes']['label']
        # # pdb.set_trace()
        # for i in range(width):
        #     for j in range(height):
        #         canvas[x_min + i][y_min + j] = label2num[label_tag]
    
    # np array和Image读取的长宽定义不一样，做个转置
    im = Image.fromarray(canvas.T).convert("L")
    im.save('{}.png'.format(out_file_name))
    
# 主函数，调用json2png函数, give a test
json2png('Snipaste_2023-02-21_12-13-00.png', 'Snipaste_2023-02-21_12-13-00.json', 'test')
# g = os.walk("D:\\HKUST\\00_Work\\04_Facade\\03_Database\\test")

# new_path_image = "D:\\HKUST\\00_Work\\04_Facade\\03_Database\\test"
# new_path_anote = "D:\\HKUST\\00_Work\\04_Facade\\03_Database\\test\\a"

# for path, dir_list, file_list in g:
#     for file_name in tqdm(file_list):
#         file_path = os.path.join(path,file_name)
#         # pdb.set_trace()
#         if file_name[-4:] == 'json':
#             json2png(file_path[:-4] + 'png', file_path, os.path.join(new_path_anote, file_name[:-5]))
#             shutil.copy(file_path[:-4] + 'png', os.path.join(new_path_image, file_name[:-4] + 'jpg'))
            
