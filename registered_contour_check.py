import os
import numpy as np
import SimpleITK as sitk 
from PIL import Image 

ct_basepath =r"D:\!JUNG_2nd_data\cutted_save_fol\CT_nii"
rt_basepath = r"D:\!JUNG_2nd_data\cutted_save_fol\RTST_nii"

ct_dir_list = os.listdir(ct_basepath)
rt_dir_list = os.listdir(rt_basepath)

for idx in range(3, len(ct_dir_list)):
    
    for jdx in range(8):
        ct_sitk = sitk.ReadImage(os.path.join(ct_basepath, ct_dir_list[idx]))
        rt_sitk = sitk.ReadImage(os.path.join(rt_basepath, rt_dir_list[8*idx+jdx]))
        
        # for j in range(8):
        #     print(rt_dir_list[8*idx+j])
        # quit()
        ct_arr = sitk.GetArrayFromImage(ct_sitk).astype("float32")
        rt_arr = sitk.GetArrayFromImage(rt_sitk)
        print(np.any(rt_arr) == 1)
        win_min = -160
        win_max = 350

        ct_arr[ct_arr < win_min] = win_min
        ct_arr[ct_arr > win_max] = win_max 

        ct_arr = 255 * (ct_arr - win_min)/(win_max - win_min)
        ct_arr = np.stack((ct_arr, )*3 , axis =-1)
        rt_coord = np.where(rt_arr == 1)

        ct_arr[rt_coord[0], rt_coord[1], rt_coord[2], :] = [255, 0, 0]
        ct_arr = ct_arr.astype("uint8")

        for i in range(len(ct_arr)):
            img = Image.fromarray(ct_arr[i])
            img.save(os.path.join(r"D:\!JUNG_2nd_data\cutted_save_fol\img_check", "P%03d_%03d_%03d.png" %(idx, jdx, i)))
        