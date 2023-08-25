import os 
import SimpleITK as sitk
import numpy as np
from PIL import Image
def resample(sitk_volume, new_spacing, new_size, default_value=0, is_label=False):
    """1) Create resampler"""
    resample = sitk.ResampleImageFilter() 
    
    """2) Set parameters"""
    #set interpolation method, output direction, default pixel value
    resample.SetInterpolator(sitk.sitkLinear)
    resample.SetOutputDirection(sitk_volume.GetDirection())
    resample.SetDefaultPixelValue(default_value)
    
    #set output spacing
    new_spacing = np.array(new_spacing)
    resample.SetOutputSpacing(new_spacing)
    
    #set output size and origin
    old_size = np.array(sitk_volume.GetSize())
    old_spacing = np.array(sitk_volume.GetSpacing())
    new_size_no_shift = np.int16(np.ceil(old_size*old_spacing/new_spacing))
    old_origin = np.array(sitk_volume.GetOrigin())
    
    shift_amount = np.int16(np.floor((new_size_no_shift - new_size)/2))*new_spacing
    new_origin = old_origin + shift_amount
    
    new_size = [int(s) for s in new_size]
    resample.SetSize(new_size)
    resample.SetOutputOrigin(new_origin)
    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        pass


    """3) execute"""
    new_volume = resample.Execute(sitk_volume)
    return new_volume

def moving_to_G_center(modal_sitk, mask_sitk, whatis="CT"):
    modal_arr = sitk.GetArrayFromImage(modal_sitk)
    mask_arr = sitk.GetArrayFromImage(mask_sitk)
    mask_coord = np.where(mask_arr != 0)
    z_center = np.sum(mask_coord[0])/len(mask_coord[0])
    y_center = np.sum(mask_coord[1])/len(mask_coord[1])
    x_center = np.sum(mask_coord[2])/len(mask_coord[2])
    
    target_y = 255
    target_x = 255
    
    moving_y = int(target_y - y_center)
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

def moving_to_backalign(modal_sitk, ma_sitk, whatis="CT"):
    modal_arr = sitk.GetArrayFromImage(modal_sitk)
    mask_arr = sitk.GetArrayFromImage(ma_sitk)
    mask_coord = np.where(mask_arr != 0)
    # z_center = np.sum(mask_coord[0])/len(mask_coord[0])
    y_center = np.sum(mask_coord[1])/len(mask_coord[1])
    x_center = np.sum(mask_coord[2])/len(mask_coord[2])
    
    target_y = 420
    target_x = 255
    
    moving_y = target_y - y_center
    moving_x = target_x - x_center
    
    mask_coord = list(mask_coord)
    #back align
    y_most_point = np.sort(mask_coord[1])[-1]
    moving_y = target_y - y_most_point
    
    fix_mask_coord = np.copy(mask_coord)
    
    mask_coord[1] += int(moving_y)
    mask_coord[2] += int(moving_x)
    new_modal_arr = np.zeros_like(modal_arr)
    
    if whatis == "CT":
        new_modal_arr[new_modal_arr == 0] = -1024
        new_modal_arr = np.pad(new_modal_arr, ((0, 0), (100, 100), (100, 100)), "constant", constant_values=-1024)
    elif whatis == "MR":
        
        new_modal_arr = np.pad(new_modal_arr, ((0, 0), (100, 100), (100, 100)), "constant", constant_values=0)

    mask_coord[1] += 100
    mask_coord[2] += 100
    
    mask_coord = tuple(mask_coord)
    fix_mask_coord = tuple(fix_mask_coord)
    
    new_modal_arr[mask_coord[0], mask_coord[1], mask_coord[2]] = modal_arr[fix_mask_coord[0], fix_mask_coord[1], fix_mask_coord[2]]
    new_modal_arr = new_modal_arr[:, 100:612, 100:612]
    
    new_modal_sitk = sitk.GetImageFromArray(new_modal_arr)
    new_modal_sitk.SetSpacing(modal_sitk.GetSpacing())
    new_modal_sitk.SetOrigin(modal_sitk.GetOrigin())
    return new_modal_sitk

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
    
    
    
ct_path =r"D:\!JUNG_2nd_data\cutted_save_fol\CT_nii"
mr_path =r"D:\!JUNG_2nd_data\cutted_save_fol\MR_nii"
ma_path =r"D:\!JUNG_2nd_data\cutted_save_fol\MA_nii"

ct_dir_list = os.listdir(ct_path)
mr_dir_list = os.listdir(mr_path)
ma_dir_list = os.listdir(ma_path)

ct_npy_save_path = r"D:\!JUNG_2nd_data\cutted_save_fol\CT_npy_backalign"
mr_npy_save_path = r"D:\!JUNG_2nd_data\cutted_save_fol\MR_npy_backalign"
ct_img_save_path = r"D:\!JUNG_2nd_data\cutted_save_fol\CT_img_backalign"
mr_img_save_path = r"D:\!JUNG_2nd_data\cutted_save_fol\MR_img_backalign"

for idx in range(len(ct_dir_list)):
    ct_sitk = sitk.ReadImage(os.path.join(ct_path, ct_dir_list[idx]))
    mr_sitk = sitk.ReadImage(os.path.join(mr_path, mr_dir_list[idx]))
    ma_sitk = sitk.ReadImage(os.path.join(ma_path, ma_dir_list[idx]))
    
    ct_sitk = moving_to_backalign_by_padding(ct_sitk, ma_sitk, "CT")
    mr_sitk = moving_to_backalign_by_padding(mr_sitk, ma_sitk, "MR")
    
    new_size = np.array([256, 256, ct_sitk.GetSize()[2]], dtype=np.double)
    new_spacing = np.array(ct_sitk.GetSpacing(), dtype=np.double)
    new_spacing[0] *= 2; new_spacing[1] *= 2
    
    
    
    ct_sitk = resample(ct_sitk, new_spacing, new_size, default_value=-1024)
    mr_sitk = resample(mr_sitk, new_spacing, new_size, default_value=0)
    
    
    
    ct_arr = sitk.GetArrayFromImage(ct_sitk)
    mr_arr = sitk.GetArrayFromImage(mr_sitk)
    
    
    win_min = -160
    win_max = 350
    img_arr = np.copy(ct_arr).astype("float32")
    img_arr[img_arr < win_min] = win_min
    img_arr[img_arr > win_max] = win_max 
    img_arr = 255 * (img_arr - win_min)/(win_max - win_min)
    img_arr = img_arr.astype("uint8")
    for i in range(len(ct_arr)):
        npy_slice = np.copy(ct_arr[i])
        np.save(os.path.join(ct_npy_save_path, "P%03d_%03d_CT.npy" %(idx, i)), npy_slice)
    for i in range(len(img_arr)):
        img = Image.fromarray(img_arr[i])
        img.save(os.path.join(ct_img_save_path, "P%03d_%03d_CT.png" %(idx, i)))
    for i in range(len(mr_arr)):
        npy_slice = np.copy(mr_arr[i])
        np.save(os.path.join(mr_npy_save_path, "P%03d_%03d_MR.npy" %(idx, i)), npy_slice)
    
    mr_max = np.max(mr_arr)
    mr_min = np.min(mr_arr)
    mr_arr = mr_arr.astype("float32")
    mr_arr = 255 * (mr_arr - mr_min)/(mr_max - mr_min)
    mr_arr = mr_arr.astype("uint8")
    for i in range(len(mr_arr)):
        img = Image.fromarray(mr_arr[i])
        img.save(os.path.join(mr_img_save_path, "P%03d_%03d_MR.png" %(idx, i)))
    