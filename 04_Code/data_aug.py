import os 
import numpy as np 
from tqdm import tqdm
import pdb
from PIL import Image
from skimage.util import random_noise
from skimage.filters import gaussian
from skimage.exposure import rescale_intensity

# 翻转
def fliph(img):
    return np.fliplr(img)

# 加噪声
def noise(img, var=0.1):
    return random_noise(img, mode='gaussian', var=var)

# 高斯模糊
def blur(img, sigma=0.1):
    is_colour = len(img.shape)==3
    return rescale_intensity(gaussian(img, sigma=sigma, multichannel=is_colour))

# 对图像做处理
def img_aug(file_dir, process='fliph'):
    # 获取文件夹位置
    g = os.walk(file_dir)
    for path, dir_list, file_list in g:
        # 建立新的文件夹，如果没有就新建，有就算了
        new_path = path + '_aug'
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        for file_name in tqdm(file_list):
            file_path = os.path.join(path,file_name)
            # 防止有的图片是RGBA的形式，就是加了一个透明度维度
            im_frame = Image.open(file_path).convert('RGB')
            # 将图片转为np.ndarray
            im_array = np.array(im_frame)
            # 调用增强函数
            if process == 'fliph':
                aug_img = fliph(im_array)
            elif process == 'blur':
                aug_img = blur(im_array)
            # 存入新的文件夹
            try:
                im = Image.fromarray(aug_img)
            except:
                im = Image.fromarray((aug_img * 255).astype(np.uint8)) # blur报错的补丁
            im.save(os.path.join(new_path, file_name[:-4] + '_' + process + '.jpg'))


if __name__ == '__main__':
    img_aug('qilou_dataset\image', 'fliph')
    img_aug('qilou_dataset\\anote', 'fliph')
    # img_aug('qilou_dataset\image', 'blur')
    # img_aug('qilou_dataset\\anote', 'blur')
