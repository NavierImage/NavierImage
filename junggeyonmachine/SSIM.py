import os
import numpy as np
import sklearn
import skimage
from scipy import signal
from PIL import Image
import matplotlib.pyplot as plt

image1_path = r"D:\unity_256_data\results\fakeCT"
image2_path = r"D:\unity_256_data\results\realCT"

ct_img_list = os.listdir(image1_path)
mr_img_list = os.listdir(image2_path)

assert len(ct_img_list) == len(mr_img_list), '파일 숫자 똑같아야'

ssim_val_arr = np.zeros((len(ct_img_list), ))
for idx in range(len(ct_img_list)):
    image1 = Image.open(image1_path + '/' + ct_img_list[idx])
    image2 = Image.open(image2_path + '/' + mr_img_list[idx])
    imarr1 = np.array(image1)
    #imarr1_gray = imarr1[:, :, 0]
    #imarr1_gray = np.squeeze(imarr1_gray)
    imarr2 = np.array(image2)
    
    ssim_val = skimage.metrics.structural_similarity(imarr1, imarr2,
                                        win_size = 11,
                                        channel_axis = None, 
                                        gaussian_weights=True, 
                                        sigma=1.0, 
                                        use_sample_covariance=False, 
                                        data_range=255)
    ssim_val_arr[idx] = ssim_val
print(ssim_val_arr[0])
print("mean ssim:", np.mean(ssim_val_arr))
print("std ssim:", np.std(ssim_val_arr))
print("median ssim:", np.median(ssim_val_arr))

#plt.hist(ssim_val_arr, len(ssim_val_arr))
#plt.show()



    
    #if ssim_val < 0.65:
    #    image1.save(r'D:\ssimclassification_edge\garbage\CT/' + ct_img_list[idx])
    #    image2.save(r'D:\ssimclassification_edge\garbage\MR/' + mr_img_list[idx])
    #else:
    #    image1.save(r'D:\ssimclassification_edge\good\CT/' + ct_img_list[idx])
    #    image2.save(r'D:\ssimclassification_edge\good\MR/' + mr_img_list[idx])
    