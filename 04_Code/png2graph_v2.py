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

border_lst = []
# dfs_array = None
# node_dict = None



def img2dic(img):
    height, width = img.shape[0], img.shape[1]
    lst = []
    for row in tqdm(range(height)):
        for col in range(width):
            lst.append(img[row][col])
    # counter = sorted(dict(Counter(lst)).items(), key = lambda kv:(kv[1], kv[0]))
    counter = Counter(lst)
    dic = {x: y / img.size for x, y in counter.items()}
    cc=sorted(dic.items(),key=lambda x:x[1],reverse=True)
    return cc

def gray_area_clean(img, thres=0.001):
    print(img.shape)
    height = img.shape[0]
    width = img.shape[1]
    cc = img2dic(img)
    print(cc[0])
    new_lst = []
    for element in cc:
        if element[1] > thres:
            new_lst.append(element[0])
    cc = new_lst
    
    new_img = np.ones((height, width))
    last_color = 255
    for row in tqdm(range(height)):
        for col in range(width):
            curr_tuple = img[row][col]
            if curr_tuple in cc:
                new_img[row][col] = img[row][col]
                last_color = img[row][col]
            else:
                # new_img[row][col] = 255
                new_img[row][col] = last_color
    return np.array(new_img).astype(np.uint8)
  # cv2_imshow(img)

def check_node_dict(key_, node_dict):
    key_lst = [x.split('_')[0] for x in node_dict.keys()]
    res_lst = [x for x in key_lst if x == key_]
    return len(res_lst)
    
def img2graph(file_path, background_color=200):
    im_frame = Image.open(file_path).convert("L")
    im_array = np.array(im_frame)
    clean_array = gray_area_clean(im_array)
    clean_dic = img2dic(clean_array)
    background_color = 255
    node_dict = {}
    width,height = clean_array.shape[0], clean_array.shape[1]
    dfs_array = clean_array.copy()

    def dfs(pix, x, y, background_color=255):
        if x <= 0 or y <= 0 or x >= len(dfs_array) - 1 or y >= len(dfs_array[0]) - 1 or dfs_array[x][y] == background_color:
            return
        elif dfs_array[x][y] < background_color and dfs_array[x][y] != pix:
            new_idx = check_node_dict(dfs_array[x][y], node_dict)
            ori_idx = check_node_dict(pix, node_dict)
            if new_idx == 0:
                return 
            elif '{}_{}'.format(dfs_array[x][y], new_idx) in node_dict['{}_{}'.format(pix, ori_idx)]:
                return
            else:
                node_dict['{}_{}'.format(pix, ori_idx)].append('{}_{}'.format(dfs_array[x][y], new_idx))
            return
        # print((x, y))
        dfs_array[x][y] = background_color
        dfs(pix, x + 1, y, background_color=background_color)
        dfs(pix, x - 1, y, background_color=background_color)
        dfs(pix, x, y + 1, background_color=background_color)
        dfs(pix, x, y - 1, background_color=background_color)
        return

    for i in tqdm(range(width)):
        for j in range(height):
            if dfs_array[i][j] < background_color:
                curr_pix = dfs_array[i][j]
                dfs(curr_pix, i, j, background_color)
    # cv.imshow('img', clean_array)
    # cv.waitKey()
    pdb.set_trace()


if __name__ == '__main__':
    # file_dir = 'D:\Code\\facade_seg-main\\04_Code\\tmp'
    # new_path = 'D:\Code\\facade_seg-main\\04_Code\\tmp_json'
    file_dir = './tmp'
    new_path = './tmp_json'
    g = os.walk(file_dir)
    for path, dir_list, file_list in g:
        for file_name in tqdm(file_list):
            if 'png' not in file_name:
                continue
            file_path = os.path.join(path,file_name)
            graph_tuple = img2graph(file_path)
            with open(os.path.join(new_path, file_name[:-4] + '.json'), 'w') as f:
                json.dump(graph_tuple, f)
