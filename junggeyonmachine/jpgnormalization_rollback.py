import os
import numpy as np
from PIL import Image

original_img_path = r"D:\MRSIM_abdomen_data\jpgnormtest"
destination = r"D:\MRSIM_abdomen_data\jpgnormtest_roll"
slash =r"/" 
ori_img_list = os.listdir(original_img_path)

for i in range(len(ori_img_list)):
    img_arr = np.array(Image.open(original_img_path+slash+ori_img_list[i]))
    img_arr = img_arr.astype("float64")
    max_ = np.max(img_arr)
    min_ = np.min(img_arr)
    
    img_arr -= min_
    if max_ - min_ < 1e-4:
        continue
    convert_coeff = 255 / (max_-min_)
    print(np.max(img_arr), np.min(img_arr))
    
    
    img_arr *= convert_coeff
    if np.min(img_arr) != 0:
        print(np.max(img_arr), np.min(img_arr))
        print(ori_img_list[i])
        break
    #print(np.max(img_arr), np.min(img_arr))
    img_arr = img_arr.astype("uint8")
    norm_img = Image.fromarray(img_arr)
    norm_img.save(destination + slash +ori_img_list[i])


