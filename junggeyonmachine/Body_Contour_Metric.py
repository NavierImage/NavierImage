import os
import math
from PIL import Image
import numpy as np

def compute_psnr(img1, img2):
    img1 = img1.astype(np.float64) / 255.
    img2 = img2.astype(np.float64) / 255.
    mse = np.mean((img1 - img2) ** 2)
    print(mse)
    if mse == 0:
        return "Same Image"
    return 10 * math.log10(1. / mse)
    
#mask_path = r'D:\AAAAmrsim\results\!!!npy_com'
rct_path = r"C:\plastimatch_npy2\def_npy_slice"
sct_path = r"D:\AAAAmrsim\results\!swinUnetr_who_v4\test_latest\fakeCT_npy_com"

rctpath_list = os.listdir(rct_path)
sctpath_list = os.listdir(sct_path)
#maskpath_list = os.listdir(mask_path)

assert len(rctpath_list) == len(sctpath_list)

rct_list = []; sct_list = []
for i in range(len(rctpath_list)):
    rct_list.append(np.load(os.path.join(rct_path, rctpath_list[i])))
    sct_list.append(np.load(os.path.join(sct_path, sctpath_list[i])))
    #mask_list.append(np.load(os.path.join(mask_path, maskpath_list[i])))

mae_t = []
for i in range(len(rct_list)):
    rct = rct_list[i].astype("float32") #range: [-1000, 4500]
    sct = sct_list[i].astype("float32") #range: [-1, 1] 
    rct += 1000
    sct = (sct+1) * (4500/2)

    mask = np.zeros_like(rct, "uint8")
    mask = np.where(rct>1, 1, 0)
    
    
    mae_map = rct-sct
    mae_map[mae_map<0] *= -1

    sums = np.sum(mae_map)
    a = np.where(mask==1)
    MAE = sums/len(a[0])
    mae_t.append(MAE)

    #mask *= 255
    #mask = mask.astype("uint8")
    #mim = Image.fromarray(mask)
    #mim.save(r"D:\AAAAmrsim\results\!111\%d.jpg" %i)

print(np.mean(mae_t), np.std(mae_t))
    

