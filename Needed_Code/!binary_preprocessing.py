import os
import nibabel as nib
import numpy as np
from scipy import ndimage
import cc3d
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

    
    ct_arr = np.transpose(ct_arr,(2, 1, 0))
    ct_arr = np.flip(ct_arr, axis=1)
    ct_arr = np.flip(ct_arr, axis=2)
    
    mr_arr = mr_nif.get_fdata()
    mr_arr = np.transpose(mr_arr, (2, 1, 0))
    mr_arr = np.flip(mr_arr, axis=1)
    mr_arr = np.flip(ct_arr, axis=2)
    binary_ct_arr = np.copy(ct_arr)
    
    max_ = 360
    min_ = -170
    
    binary_ct_arr[binary_ct_arr > max_] = max_
    binary_ct_arr[binary_ct_arr < min_] = min_
    binary_ct_arr = 255 * (binary_ct_arr - min_)/ (max_ - min_)
    
    binary_ct_arr = binary_ct_arr.astype("uint8")
    binary_ct_arr[binary_ct_arr != 0] = 1
    
    # COUNTING METHOD
    # labels_out = cc3d.connected_components(binary_ct_arr)
    # label_list = [0]
    # for label in range(1, 300):
        # a = np.where(labels_out == label)
        # label_list.append(len(a[0]))
    # print(label_list)
    
    #DUST OUT METHOD
    binary_ct_arr = cc3d.dust(binary_ct_arr, threshold=1000000)

    #DEBUGGING CODE
    
    binary_ct_arr *= 255
    # for i in range(len(binary_ct_arr)):
        
        # if i+1 > 36:
            # continue
        # arr_slice = binary_ct_arr[i].astype("uint8")
        # mask = ndimage.binary_closing(arr_slice, iterations=50)
        # mask = mask.astype("uint8")
        # mask *= 255
        # img = Image.fromarray(mask)
        # img.save(r"D:\!JUNG_newdata\!img_fol\first_processed/bct/P%03d_%03d.png" %(idx+1, i+1))
    
    for i in range(len(ct_arr)):
        if i+1 > 36:
            continue
        arr = ct_arr[i]
        mask1 = binary_ct_arr[i].astype("uint8")
        mask1 = ndimage.binary_closing(mask1, iterations=50).astype(int)
        mask2 = binary_ct_arr[i].astype("uint8")
        mask = mask1 + mask2
        arr = np.where(mask != 0, arr, 0)
        np.save(r"D:\!JUNG_newdata\!npy_fol\first_processed/ct/P%03d_%03d.npy" %(idx+1, i+1), ct_arr[i])
    for i in range(len(mr_arr)):
        if i+1 > 36:
            continue
        np.save(r"D:\!JUNG_newdata\!npy_fol\first_processed/mr/P%03d_%03d.npy" %(idx+1, i+1), mr_arr[i])
    
    max_ = 360
    min_ = -170
    ct_arr[ct_arr > max_] = max_
    ct_arr[ct_arr < min_] = min_
    ct_arr = 255 * (ct_arr - min_)/ (max_ - min_)
    print(idx+1)
    for i in range(len(ct_arr)):
        if i+1 > 36:
            continue
        arr_slice = ct_arr[i].astype("uint8")
        mask1 = binary_ct_arr[i].astype("uint8")
        mask1 = ndimage.binary_closing(mask1, iterations=50).astype(int)
        mask2 = binary_ct_arr[i].astype("uint8")
        mask = mask1 + mask2
        arr_slice = np.where(mask != 0, arr_slice, 0)
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