import os
import numpy as np
import sklearn
import skimage
import cv2
from scipy import signal
from PIL import Image
from scipy.spatial import distance

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
    imarr1[imarr1 >10] = 255
    imarr2[imarr2 >10] = 255
    imarr1[imarr1<= 10] = 0
    imarr2[imarr2<= 10] = 0
    imarr1_mask = np.zeros_like(imarr1)
    imarr2_mask = np.zeros_like(imarr2)

    imarr1_mask = np.where(imarr1 == 255, 1, 0)
    imarr2_mask = np.where(imarr2 == 255, 1, 0)
    imarr1_mask_one = np.ravel(imarr1_mask)
    imarr2_mask_two = np.ravel(imarr2_mask)
    if distance.dice(imarr1_mask_one, imarr2_mask_two) > 0.08:
        image1.save(r'D:\diceclassification\good\CT/' + ct_img_list[idx])
        image2.save(r'D:\diceclassification\good\MR/' + mr_img_list[idx])
    else:
        image1.save(r'D:\diceclassification\garbage\CT/' + ct_img_list[idx])
        image2.save(r'D:\diceclassification\garbage\MR/' + mr_img_list[idx])


