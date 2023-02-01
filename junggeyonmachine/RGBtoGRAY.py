import os
import numpy as np
from PIL import Image

rgb_path = r"C:\plastimatch_npy2\!!!!pel\realMR_gray"
gray_path = r"C:\plastimatch_npy2\!!!!pel\rm1"


rgb_imgs_list = os.listdir(rgb_path)

for idx in range(len(rgb_imgs_list)):
    rgb_img = Image.open(rgb_path +'/' + rgb_imgs_list[idx])
    rgb_img_arr = np.array(rgb_img)
    
    if len(rgb_img_arr.shape) == 3:
        
        gray_img_arr = rgb_img_arr[:, :, 0]
        gray_img_arr = np.squeeze(gray_img_arr)
        
        gray_img = Image.fromarray(gray_img_arr)
    
        gray_img.save(gray_path +'/'+ rgb_imgs_list[idx][:-4] +'.jpg')

