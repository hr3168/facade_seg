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
    print("canvas shape:", canvas.shape)        

    pdb.set_trace()
    # 遍历标注区域
    for label in json_data['shapes']:
        label_tag = label["label"]
        points = label["points"]
        # canvas = cv2.fillConvexPoly(canvas, points, label2num[label_tag])
        points = np.array(points, dtype=np.int32) # 将 "points" 转换为numpy数组类型
        canvas = cv2.fillConvexPoly(canvas, [points], label2num[label_tag])


        

    # np array和Image读取的长宽定义不一样，做个转置
    im = Image.fromarray(canvas.T).convert("L")
    im.save('{}.png'.format(out_file_name))
    
# 主函数，调用json2png函数, give a test
json2png('Snipaste_2023-02-21_12-59-54.png', 'Snipaste_2023-02-21_12-59-54.json', 'test')
# g = os.walk("D:\\HKUST\\00_Work\\04_Facade\\03_Database\\test")

# new_path_image = "D:\HKUST\00_Work\04_Facade\facade_seg\04_Code\qilou_dataset\image2"
# new_path_anote = "D:\HKUST\00_Work\04_Facade\facade_seg\04_Code\qilou_dataset\anote2"

# for path, dir_list, file_list in g:
#     for file_name in tqdm(file_list):
#         file_path = os.path.join(path,file_name)
#         # pdb.set_trace()
#         if file_name[-4:] == 'json':
#             json2png(file_path[:-4] + 'png', file_path, os.path.join(new_path_anote, file_name[:-5]))
#             shutil.copy(file_path[:-4] + 'png', os.path.join(new_path_image, file_name[:-4] + 'jpg'))
            
