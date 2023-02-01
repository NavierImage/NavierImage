import os
import numpy as np
from PIL import Image

original_img_path = r"D:\DLnetwork\traindata_MRSIM_CECT_MR_jpg\testB_origin"
destination = r"D:\DLnetwork\traindata_MRSIM_CECT_MR_jpg\testB"
slash =r"/" 
ori_img_list = os.listdir(original_img_path)

for i in range(len(ori_img_list)):
    img_arr = np.array(Image.open(original_img_path+slash+ori_img_list[i]))

    img_arr[img_arr > 220] = 220
    img_arr[img_arr < 30] = 30
    
    
    norm_img = Image.fromarray(img_arr)
    norm_img.save(destination + slash +ori_img_list[i])


