import os
import SimpleITK as sitk
import numpy as np

basepath = r"D:\!JUNG_2nd_data\abdomenMR1xT_regi_hist_denoise"
savepath = r"D:\!JUNG_2nd_data\abdomenMr1xT_regi_hist_denoise_2"
nii_dir_list = os.listdir(basepath)
for i in range(len(nii_dir_list)):
    nii_path = os.path.join(basepath, nii_dir_list[i])
    mr_sitk = sitk.ReadImage(nii_path)
    mr_arr = sitk.GetArrayFromImage(mr_sitk)
    if np.min(mr_arr) < 0:
        mr_arr += abs(np.min(mr_arr))
    
    mr_arr = mr_arr.astype("uint16")
    mr_new_sitk = sitk.GetImageFromArray(mr_arr)
    mr_new_sitk.SetSpacing(mr_sitk.GetSpacing())
    mr_new_sitk.SetOrigin(mr_sitk.GetOrigin())
    sitk.WriteImage(mr_new_sitk, os.path.join(savepath, nii_dir_list[i]))

    