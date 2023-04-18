import json
import pdb
import os
from PIL import Image
import shutil
import numpy as np
import cv2 as cv
from tqdm import tqdm
from collections import Counter
import sys, threading
sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

# label dictionary
color_dict = {'background': (207, 248, 132),
    'shop': (31, 133, 226),
    'column': (170, 252, 0),
    'wall': (183, 244, 155),
    'montainwall': (122, 113, 97),
    'railing': (222, 181, 51),
    'floor': (204, 47, 7),
    'window': (144, 71, 111),
    'base': (46, 229, 72)}

pixel2node = {v:k for k, v in color_dict.items()}

# 寻找和当前像素点最近的label
def align_color(pixel):
    res = 'background'
    res_gap = 100000
    for k, v in color_dict.items():
        curr_gap = abs(v[0] - pixel[0]) + abs(v[1] - pixel[1]) + abs(v[2] - pixel[2])
        if curr_gap < res_gap:
            res_gap = curr_gap
            res = k 
    return res

# 遍历pixel 替换像素点，保证所有像素点都在label范围里
def replace_color(im_array):
    n, m = im_array.shape[0], im_array.shape[1]
    canvas = [[j for j in range(m)] for i in range(n)]
    for i in tqdm(range(n)):
        for j in range(m):
            canvas[i][j] = align_color((im_array[i][j][0],im_array[i][j][1],im_array[i][j][2]))
    return canvas

def get_curr_node(key_, node_set):
    key_lst = [x.split('_')[0] for x in node_set]
    res_lst = [x for x in key_lst if x == key_]
    return '{}_{}'.format(key_, len(res_lst))

def img2graph(file_path):
    # 读取png数据
    im_frame = Image.open(file_path)
    im_array = np.array(im_frame)
    width,height = im_array.shape[0], im_array.shape[1]
    clean_array = replace_color(im_array)
    node_set = set()
    canvas = clean_array.copy()

    def dfs(label, x, y, curr_node):
        if x < 0 or y < 0 or x >= len(canvas) - 1 or y >= len(canvas[0]) - 1 or canvas[x][y] != label:
            return
        canvas[x][y] = curr_node
        dfs(label, x + 1, y, curr_node)
        dfs(label, x - 1, y, curr_node)
        dfs(label, x, y + 1, curr_node)
        dfs(label, x, y - 1, curr_node)
        return

    for i in tqdm(range(width)):
        for j in range(height):
            if canvas[i][j] != 'background' and '_' not in canvas[i][j]:
                curr_pix = canvas[i][j]
                curr_node = get_curr_node(curr_pix, node_set)
                node_set.add(curr_node)
                dfs(curr_pix, i, j, curr_node)
    # pdb.set_trace()
    edge_set = set()
    for i in tqdm(range(width - 1)):
        for j in range(height - 1):
            if canvas[i][j] != 'background':
                if canvas[i][j] != canvas[i + 1][j]:
                    edge_set.add((canvas[i][j], canvas[i + 1][j], 'level'))
                if canvas[i][j] != canvas[i][j - 1]:
                    edge_set.add((canvas[i][j], canvas[i][j + 1], 'horizental'))
    return node_set, edge_set

if __name__ == '__main__':
    # file_dir = 'D:\Code\\facade_seg-main\\04_Code\\tmp'
    # new_path = 'D:\Code\\facade_seg-main\\04_Code\\tmp_json'
    img_path = 'pspnet_2_T006.jpg'
    node_set, edge_set = img2graph(img_path)
