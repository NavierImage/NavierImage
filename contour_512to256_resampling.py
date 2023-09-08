import os 
import numpy as np
import SimpleITK as sitk 

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

basepath = r"D:\!JUNG_2nd_data\cutted_save_fol\RTST_nii"
rt_dir_list = os.listdir(basepath)

for i in range(len(rt_dir_list)):
    rt_path = os.path.join(basepath, rt_dir_list[i])
    rt_sitk = sitk.ReadImage(rt_path)
    spacing = np.array([1.4, 1.4, 1.2], dtype=np.double)
    size = np.array([256, 256, rt_sitk.GetSize()[2]], dtype=np.double)
    rt_res_sitk = resample(rt_sitk, spacing, size)
    rt_res_arr =sitk.GetArrayFromImage(rt_res_sitk)
    rt_res_arr[rt_res_arr < 0.5] = 0
    rt_res_arr[rt_res_arr>=0.5] = 1
    rt_res_final_sitk = sitk.GetImageFromArray(rt_res_arr)
    rt_res_final_sitk.SetSpacing(spacing)
    sitk.WriteImage(rt_res_final_sitk, os.path.join(r"D:\!JUNG_2nd_data\cutted_save_fol\RTST_nii_256", rt_dir_list[i]))