import os
import numpy as np
import SimpleITK as sitk
from PIL import Image 

ct_basepath = r"D:\!JUNG_2nd_data\cutted_save_fol\CT_moved_nii"
rt_basepath = r"D:\!JUNG_2nd_data\cutted_save_fol\RTST_moved_nii"

ct_dir_list = os.listdir(ct_basepath)
rt_dir_list = os.listdir(rt_basepath)

for idx in range(len(ct_dir_list)):
    ct_sitk_path = os.path.join(ct_basepath, ct_dir_list[idx])
    rt_sitk_path = os.path.join(rt_basepath, rt_dir_list[8*idx + 5])
    
    ct_sitk = sitk.ReadImage(ct_sitk_path)
    rt_sitk = sitk.ReadImage(rt_sitk_path) 
    
    ct_arr = sitk.GetArrayFromImage(ct_sitk)
    rt_arr = sitk.GetArrayFromImage(rt_sitk) 
    
    img_arr = np.stack((ct_arr, )* 3, axis =-1)
    win_min = -160
    win_max = 350
    
    img_arr[img_arr < win_min] = win_min
    img_arr[img_arr > win_max] = win_max 
    img_arr = 255 * (img_arr - win_min)/(win_max - win_min)
    img_arr = img_arr.astype("uint8")
    
    contour_coord = np.where(rt_arr == 1)
    img_arr[contour_coord[0], contour_coord[1], contour_coord[2], :] = [255, 0 ,0]
    
    for i in range(len(img_arr)):
        img = Image.fromarray(img_arr[i])
        img.save(r"D:\!JUNG_2nd_data\cutted_save_fol\img_check/" + "P%03d_%03d.png" %(idx, i))
    