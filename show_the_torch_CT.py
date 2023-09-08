import os 
import torch 
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
realCT_path = r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_swinunetr_nomind_v2\test_latest\realCT"
realCT_dir_list = os.listdir(realCT_path)

win_max = 350
win_min = -160
for i in range(len(realCT_dir_list)):

    real_ct_tensor = torch.load(os.path.join(realCT_path, realCT_dir_list[i]),map_location=torch.device("cpu"))
    real_ct_arr = real_ct_tensor.detach().clone().cpu().numpy()
    real_ct_arr = np.squeeze(real_ct_arr)
    
    real_ct_arr += 1
    real_ct_arr /= 2
    real_ct_arr *= 4096
    real_ct_arr -= 1024
    
    real_ct_arr[real_ct_arr < win_min] = win_min
    real_ct_arr[real_ct_arr > win_max] = win_max
    
    real_ct_arr = 255 * (real_ct_arr - win_min)/(win_max - win_min)
    real_ct_arr = real_ct_arr.astype("uint8")

    img = Image.fromarray(real_ct_arr)
    img.save(os.path.join(r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_swinunetr_nomind_v2\test_latest\realCT_img", realCT_dir_list[i][:-3] + ".png"))
