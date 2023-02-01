import os
import numpy as np
from scipy.spatial.distance import directed_hausdorff
import skimage
from scipy import signal
from PIL import Image


ct_img_path = r'D:\CT_norm_im'
mr_img_path = r'D:\MR_norm_im'

ct_img_list = os.listdir(ct_img_path)
mr_img_list = os.listdir(mr_img_path)

assert len(ct_img_list) == len(mr_img_list), '파일 숫자 똑같아야'

for idx in range(len(ct_img_list)):
    image1 = Image.open(ct_img_path + '/' + ct_img_list[idx])
    image2 = Image.open(mr_img_path + '/' + mr_img_list[idx])
    imarr1 = np.array(image1)
    imarr2 = np.array(image2)
    
    hd_distance = skimage.metrics.hausdorff_distance(imarr1, imarr2)
    
    if hd_distance > 100:
        image1.save(r'D:\hdclassification\garbage\CT/' + ct_img_list[idx])
        image2.save(r'D:\hdclassification\garbage\MR/' + mr_img_list[idx])
    else:
        image1.save(r'D:\hdclassification\good\CT/' + ct_img_list[idx])
        image2.save(r'D:\hdclassification\good\MR/' + mr_img_list[idx])