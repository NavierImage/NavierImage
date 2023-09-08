import os 
import numpy as np
from PIL import Image

ct_im_path = r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_resnet_nomind_v1\test_latest\fakeCT_gray"
mr_im_path = r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_resnet_nomind_v1\test_latest\realMR_img"

ct_im_dir_list = os.listdir(ct_im_path)
mr_im_dir_list = os.listdir(mr_im_path)

for i in range(len(ct_im_dir_list)):
    ct_arr = np.array(Image.open(os.path.join(ct_im_path, ct_im_dir_list[i])))
    mr_arr = np.array(Image.open(os.path.join(mr_im_path, mr_im_dir_list[i])))
    
    ct_arr = np.stack((ct_arr, ) * 3, axis = -1)
    mr_arr = np.stack((mr_arr, )* 3, axis = -1)
    
    ct_arr[..., 0] = 0
    ct_arr[..., 2] = 0
    mr_arr[..., 1] = 0
    
    fusion_arr = ct_arr + mr_arr 
    fusion_arr = fusion_arr.astype("uint8")
    
    fusion_img = Image.fromarray(fusion_arr)
    fusion_img.save(os.path.join(r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_resnet_nomind_v1\test_latest\fusion_img", mr_im_dir_list[i]))

    