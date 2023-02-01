import os 
import numpy as np
from PIL import Image
from sklearn.metrics import mean_absolute_error

img1_path = r"D:\DLnetwork\MRSIM_checkpoints_2\results\MRSIM_CECT_totalMR_v5\test_latest\fakeCT_gray"
img2_path = r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR\testB"
slash = r'/'
img1_list = os.listdir(img1_path)
img2_list = os.listdir(img2_path)
assert len(img1_list) == len(img2_list)
for i in range(len(img1_list)):
    imarr1 = np.array(Image.open(img1_path + slash + img1_list[i]), 'int16')
    imarr2 = np.array(Image.open(img2_path + slash + img2_list[i]), 'int16')
    mae_arr = imarr1 - imarr2
    mae_arr = np.where(mae_arr < 0, -1 * mae_arr, mae_arr)
    mae_arr = mae_arr.astype('uint8')
    mae_img = Image.fromarray(mae_arr)
    mae_img.save(r"D:\DLnetwork\MRSIM_checkpoints_2\results\MRSIM_CECT_totalMR_v5\test_latest\mae/"+
                    img1_list[i][:4] + 
                    "mae_slice"+
                    img1_list[i][13:16]+
                    '.jpg')

