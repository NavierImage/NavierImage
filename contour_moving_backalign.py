import os 
import SimpleITK as sitk 
import numpy as np 
def moving_to_backalign_by_padding(modal_sitk, mask_sitk, whatis="CT"):
    modal_arr = sitk.GetArrayFromImage(modal_sitk)
    mask_arr = sitk.GetArrayFromImage(mask_sitk)
    mask_coord = np.where(mask_arr != 0)
    z_center = np.sum(mask_coord[0])/len(mask_coord[0])
    y_center = np.sum(mask_coord[1])/len(mask_coord[1])
    x_center = np.sum(mask_coord[2])/len(mask_coord[2])
    
    
    y_below = np.max(mask_coord[1])
    
    target_y = 420
    target_x = 255
    
    moving_y = int(target_y - y_below)
    moving_x = int(target_x - x_center)

    new_modal_arr = np.copy(modal_arr)
    
    if whatis == "CT":
        new_modal_arr = np.pad(new_modal_arr, ((0, 0), (200, 200), (200, 200)), "constant", constant_values=-1024)
    elif whatis == "MR":
        
        new_modal_arr = np.pad(new_modal_arr, ((0, 0), (200, 200), (200, 200)), "constant", constant_values=0)
    
    new_modal_arr = new_modal_arr[:, 200-moving_y:512+200-moving_y, 200-moving_x:512+200-moving_x]
    
    new_modal_sitk = sitk.GetImageFromArray(new_modal_arr)
    new_modal_sitk.SetSpacing(modal_sitk.GetSpacing())
    new_modal_sitk.SetOrigin(modal_sitk.GetOrigin())
    return new_modal_sitk
ct_path = r"D:\!JUNG_2nd_data\cutted_save_fol\CT_nii"
ct_dir_list = os.listdir(ct_path)
rt_path = r"D:\!JUNG_2nd_data\cutted_save_fol\RTST_nii"
ma_path = r"D:\!JUNG_2nd_data\cutted_save_fol\MA_nii"

rt_dir_list = os.listdir(rt_path)
ma_dir_list = os.listdir(ma_path)
ct_savepath = r"D:\!JUNG_2nd_data\cutted_save_fol\CT_moved_nii"

rt_savepath = r"D:\!JUNG_2nd_data\cutted_save_fol\RTST_moved_nii"
os.makedirs(rt_savepath, exist_ok=True)

for idx in range(len(ma_dir_list)):
    ct_sitk = sitk.ReadImage(os.path.join(ct_path, ct_dir_list[idx]))
    
    ma_sitk = sitk.ReadImage(os.path.join(ma_path, ma_dir_list[idx]))
    ct_sitk = moving_to_backalign_by_padding(ct_sitk, ma_sitk, "CT")
    sitk.WriteImage(ct_sitk, os.path.join(ct_savepath, ct_dir_list[idx]))
    for jdx in range(8):
        rt_sitk = sitk.ReadImage(os.path.join(rt_path, rt_dir_list[8*idx + jdx]))
        rt_arr = sitk.GetArrayFromImage(rt_sitk)
        
        rt_sitk = moving_to_backalign_by_padding(rt_sitk, ma_sitk, "MR")
        sitk.WriteImage(rt_sitk, os.path.join(rt_savepath, rt_dir_list[8*idx + jdx]))