import os 
import SimpleITK as sitk
import numpy as np

mr_path = r"D:\!JUNG_2nd_data\abdomenMr1xT_regi_hist_denoise_2"
rt_path = r"D:\!JUNG_2nd_data\abdomenCT1_contour"

mr_savepath = r"D:\!JUNG_2nd_data\cutted_save_fol\MR_nii"
rt_savepath = r"D:\!JUNG_2nd_data\cutted_save_fol\RTST_nii"

os.makedirs(rt_savepath, exist_ok=True)


mr_dir_list = os.listdir(mr_path)
rt_dir_list = os.listdir(rt_path)


for idx in range(len(mr_dir_list)):

    mr_sitk = sitk.ReadImage(os.path.join(mr_path, mr_dir_list[idx]))
    mr_arr = sitk.GetArrayFromImage(mr_sitk)
    
    mr_coord = np.where(mr_arr >= 3) # z y x
    mr_z_coord_sort = np.sort(mr_coord[0])
    
    Z1 = mr_z_coord_sort[0]
    Z2 = mr_z_coord_sort[-1]
    Z1 += 30
    Z2 -= 100
    for jdx in range(8):
        rt_sitk = sitk.ReadImage(os.path.join(rt_path, rt_dir_list[8*idx + jdx]))
        rt_arr = sitk.GetArrayFromImage(rt_sitk)
        rt_crop_arr = rt_arr[Z1:Z2+1, ...]

        rt_crop_sitk = sitk.GetImageFromArray(rt_crop_arr)

        rt_crop_sitk.SetSpacing(rt_sitk.GetSpacing())
        rt_crop_sitk.SetOrigin(rt_sitk.GetOrigin())

        sitk.WriteImage(rt_crop_sitk, os.path.join(rt_savepath, rt_dir_list[8*idx+jdx]))

    
    