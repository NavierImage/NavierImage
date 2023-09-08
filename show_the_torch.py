import os 
import torch 
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
fakeMR_path = r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_resnet_nomind_v1\test_latest\realMR_pt"
fakeMR_dir_list = os.listdir(fakeMR_path)

for i in range(len(fakeMR_dir_list)):

    fake_mr_tensor = torch.load(os.path.join(fakeMR_path, fakeMR_dir_list[i]),map_location=torch.device("cpu"))
    fake_mr_arr = fake_mr_tensor.detach().clone().cpu().numpy()
    fake_mr_arr = np.squeeze(fake_mr_arr)
    fake_mr_arr = 255 * (fake_mr_arr - np.min(fake_mr_arr))/(np.max(fake_mr_arr) - np.min(fake_mr_arr))
    fake_mr_arr = fake_mr_arr.astype("uint8")

    img = Image.fromarray(fake_mr_arr)
    img.save(os.path.join(r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_resnet_nomind_v1\test_latest\realMR_img", fakeMR_dir_list[i][:-3] + ".png"))
