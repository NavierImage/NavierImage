import os
import nibabel as nib
import numpy as np
from PIL import Image
bp = r"D:\!JUNG_newdata\!nii_fol"

ct_p = os.path.join(bp, "CTnii")
mr_p = os.path.join(bp, "MRnii")

ct_path_list = os.listdir(ct_p)
mr_path_list = os.listdir(mr_p)
for idx in range(len(ct_path_list)):
    ct_nif = nib.load(os.path.join(ct_p, ct_path_list[idx]))
    mr_nif = nib.load(os.path.join(mr_p, mr_path_list[idx]))
    ct_arr = ct_nif.get_fdata()
    mr_arr = mr_nif.get_fdata()
    ct_arr = np.flip(ct_arr, axis=1)
    mr_arr = np.flip(mr_arr, axis=1)
    ct_arr = np.transpose(ct_arr,(2, 1, 0))
    mr_arr = np.transpose(mr_arr, (2, 1, 0))
    
    
    # for i in range(len(ct_arr)):
        # if i+1 > 36:
            # continue
        # np.save(r"D:\!JUNG_newdata\!npy_fol\first_processed/ct/P%03d_%03d.npy" %(idx+1, i+1), ct_arr[i])
    # for i in range(len(mr_arr)):
        # if i+1 > 36:
            # continue
        # np.save(r"D:\!JUNG_newdata\!npy_fol\first_processed/mr/P%03d_%03d.npy" %(idx+1, i+1), mr_arr[i])
        
    max_ = 360
    min_ = -170
    ct_arr[ct_arr > max_] = max_
    ct_arr[ct_arr < min_] = min_
    ct_arr = 255 * (ct_arr - min_)/ (max_ - min_)
    for i in range(len(ct_arr)):
        if i+1 > 36:
            continue
        arr_slice = ct_arr[i].astype("uint8")
        img = Image.fromarray(arr_slice)
        img.save(r"D:\!JUNG_newdata\!img_fol\first_processed/ct/P%03d_%03d.png" %(idx+1, i+1))
    mr_max = np.max(mr_arr)
    mr_min = np.min(mr_arr)
    mr_arr = 255 * (mr_arr - mr_min)/(mr_max-mr_min)
    for i in range(len(mr_arr)):
        if i+1 > 36:
            continue
        arr_slice = mr_arr[i].astype("uint8")
        img = Image.fromarray(arr_slice)
        img.save(r"D:\!JUNG_newdata\!img_fol\first_processed/mr/P%03d_%03d.png" %(idx+1, i+1))