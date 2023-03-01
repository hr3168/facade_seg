import json
import pdb
from PIL import Image
import numpy as np

def json2png(png_file_name, json_file_name, out_file_name):
    # 读取json文件
    with open(json_file_name) as f:
        json_data = json.load(f) # 这里的json_data是一个列表，每个元素是一个字典，包含标注的区域信息
    
    # 获取png格式
    im_frame = Image.open(png_file_name)
    
    # 根据png的尺寸创建画布，默认label为0
    canvas = np.zeros(im_frame.size)
    # 遍历标注区域
    for label in json_data:
        # label的keys:['content', 'rectMask', 'labels', 'labelLocation', 'contentType']
        # 获取标注区域的起点与长宽，由于json文件的区域是float类型，但是下标只支持int类型，所以做类型转化（会影响精度）
        x_min = int(label['rectMask']['xMin'])
        y_min = int(label['rectMask']['yMin'])
        width = int(label['rectMask']['width'])
        height = int(label['rectMask']['height'])
        # pdb.set_trace()
        # 根据起点、长宽信息对区域做打标，默认打标为100，后面可以改
        for i in range(width):
            for j in range(height):
                canvas[x_min + i][y_min + j] = 100
    
    # np array和Image读取的长宽定义不一样，做个转置（试出来的）
    im = Image.fromarray(canvas.T).convert("L")
    im.save('{}.png'.format(out_file_name))
    
# 主函数，调用json2png函数
json2png('Snipaste_2023-02-21_12-13-00.png', 'Snipaste_2023-02-21_12-13-00.json', 'test')
