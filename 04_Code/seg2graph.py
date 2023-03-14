import json
import pdb
import os
from PIL import Image
import shutil
import numpy as np
import cv2 as cv
from tqdm import tqdm
from collections import Counter

def check_border(grid, x, y):
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]) or grid[x][y] == 1:
        return False
    return True

def dfs(grid, x, y):
    pass 

def gray_area_clean(img, thres=0.05):
    print(img.shape)
    height = img.shape[0]
    width = img.shape[1]
    # channels = img.shape[2]
    print('height:{}, width:{}'.format(height, width))
    print(img.size)
    lst = []
    for row in tqdm(range(height)):
        for col in range(width):
            lst.append(img[row][col])
    # counter = sorted(dict(Counter(lst)).items(), key = lambda kv:(kv[1], kv[0]))
    counter = Counter(lst)
    dic = {x: y / img.size for x, y in counter.items()}
    cc=sorted(dic.items(),key=lambda x:x[1],reverse=True)
    print(cc[0])
    new_lst = []
    for element in cc:
        if element[1] > thres:
            new_lst.append(element[0])
    cc = new_lst
    
    new_img = np.ones((height, width))
    for row in tqdm(range(height)):
        for col in range(width):
            curr_tuple = img[row][col]
            if curr_tuple in cc:
                new_img[row][col] = img[row][col]
            else:
                new_img[row][col] = 255
    return np.array(new_img).astype(np.uint8)
  # cv2_imshow(img)

def img2graph(file_path):
    im_frame = Image.open(file_path).convert("L")
    im_array = np.array(im_frame)
    clean_array = gray_area_clean(im_array)
    cv.imshow('img', clean_array)
    cv.waitKey()
    pdb.set_trace()


if __name__ == '__main__':
    file_dir = 'D:\Code\\facade_seg-main\\04_Code\\tmp'
    new_path = 'D:\Code\\facade_seg-main\\04_Code\\tmp_json'
    g = os.walk(file_dir)
    for path, dir_list, file_list in g:
        for file_name in tqdm(file_list):
            if 'png' not in file_name:
                continue
            file_path = os.path.join(path,file_name)
            graph_tuple = img2graph(file_path)
            with open(os.path.join(new_path, file_name[:-4] + '.json'), 'w') as f:
                json.dump(graph_tuple, f)
