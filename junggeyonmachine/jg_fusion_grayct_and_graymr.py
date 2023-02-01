import numpy as np
from PIL import Image
from numpngw import write_png
import skimage
import os

basepath = r'D:\junggeyon'

ct_file_list = os.listdir(basepath + '/pelvic_CT_pic_npy')
mr_file_list = os.listdir(basepath + '/pelvic_MR_pic_npy')

assert len(ct_file_list) == len(mr_file_list), "pair 안 맞음"

for i in range(11, 12):
    ctnpy_filename = ct_file_list[i]
    mrnpy_filename = mr_file_list[i]
    ct_vol = np.load(basepath + '/pelvic_CT_pic_npy/' + ctnpy_filename)
    mr_vol = np.load(basepath + '/pelvic_MR_pic_npy/'+ mrnpy_filename)
    ct_vol = ct_vol.astype('float64')
    ct_vol *= 255/65535

    ct_vol_green = np.zeros((3, ct_vol.shape[0], ct_vol.shape[1], ct_vol.shape[2]))
    mr_vol_pink = np.zeros((3, mr_vol.shape[0], mr_vol.shape[1], mr_vol.shape[2]))

    ct_vol_green[1] = ct_vol
    mr_vol_pink[0], mr_vol_pink[2] = mr_vol, mr_vol
    
    mr_vol_pink = mr_vol_pink.astype('int16')
    mr_vol_pink[mr_vol_pink < 0] = 0
    mr_vol_pink = mr_vol_pink.astype('uint8')

    ct_vol_green = np.transpose(ct_vol_green, (1, 2, 3, 0))
    mr_vol_pink = np.transpose(mr_vol_pink, (1, 2, 3, 0))
    print(mr_vol.shape, mr_vol_pink.shape)
    mr_vol_pink_resized = np.zeros((int(mr_vol_pink.shape[0]), 512, 512, 3))

   
    mr_vol_pink_resized = skimage.transform.resize(mr_vol_pink, (int(mr_vol_pink.shape[0]), 512, 512, 3))
    mr_vol_pink_resized *= 255
    mr_vol_pink_resized = mr_vol_pink_resized.astype('uint8')    
    fusion_vol =  ct_vol_green + mr_vol_pink_resized

    #fusion_vol = np.transpose(fusion_vol, (1, 2, 3, 0))
    fusion_vol = fusion_vol.astype('uint8')
    for idx in range(len(fusion_vol)):
        image = Image.fromarray(fusion_vol[idx])
        image.save(r"D:\junggeyon\pelvic_fusion\P%03dfusion_slice%03d.jpg" %(i+1, idx+1))
        if len(fusion_vol) - idx == 31:
            break



