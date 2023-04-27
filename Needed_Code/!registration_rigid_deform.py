# for registration MR and CT
# MR -> CT registration, deformable

import os
import numpy as np
import SimpleITK as sitk
import nibabel as nib
import matplotlib.pyplot as plt
def convert_to_sitk(img_volume, spacing, origin, direction=None):
    """convert numpy volume to sitk image"""
    # numpy [z, y, x] -> sitk [x, y, z]
    sitk_volume = sitk.GetImageFromArray(img_volume.astype(np.float64))
    sitk_volume.SetOrigin(origin)
    sitk_volume.SetSpacing(spacing)
    if direction:
        sitk_volume.SetDirection(direction)
    return sitk_volume

def convert_to_numpy(sitk_volume):
    """convert sitk image to numpy volume"""
    img_volume = sitk.GetArrayFromImage(sitk_volume)
    
    return img_volume

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

def registration(fixed_sitk, moving_sitk, save_path = None, ind = 0):
    """1) Set ElastixImageFilter"""
    elastixImageFilter = sitk.ElastixImageFilter()
    """2) Set Parameters"""
    elastixImageFilter.SetFixedImage(fixed_sitk)
    elastixImageFilter.SetMovingImage(moving_sitk)

    
    parameterMapVector = sitk.VectorOfParameterMap()
    translation_map = sitk.GetDefaultParameterMap('translation')
    translation_map['MaximumNumberOfIterations'] = ['2000']
    parameterMapVector.append(translation_map)
    rigid_map = sitk.GetDefaultParameterMap("rigid")
    rigid_map['MaximumNumberOfIterations'] = ["50"]
    parameterMapVector.append(rigid_map)
    bspline_map = sitk.GetDefaultParameterMap("bspline")
    bspline_map["FinalGridSpacingInPhysicalUnits"] = ["40"]
    bspline_map['MaximumNumberOfIterations'] = ['33']
    parameterMapVector.append(bspline_map)
    bspline2_map = sitk.GetDefaultParameterMap("bspline")
    bspline2_map["FinalGridSpacingInPhysicalUnits"] = ["20"]
    bspline2_map['MaximumNumberOfIterations'] = ['5']
    parameterMapVector.append(bspline2_map)
    # parametermap = sitk.GetDefaultParameterMap('translation')
    
    # parametermap['MaximumNumberOfSamplingAttempts'] = ['16']
    elastixImageFilter.SetParameterMap(parameterMapVector) #method
    # elastixImageFilter.SetInitialTransform(initial_transform, inPlace=True)
    """3) Execute"""
    elastixImageFilter.Execute()
    resultimage = elastixImageFilter.GetResultImage()
    
    #save parameter map
    temp_idx = 0
    while True:
        try:
            sitk.WriteParameterFile(elastixImageFilter.GetTransformParameterMap()[temp_idx], os.path.join(save_path, "P%03d_%03d_param.txt" %(ind, temp_idx)))
        except:
            break
        temp_idx += 1

    return resultimage

def rigid_registration(fixed_sitk, moving_sitk, save_path = None, ind = 0):
    """1) Set ElastixImageFilter"""
    elastixImageFilter = sitk.ElastixImageFilter()
    """2) Set Parameters"""
    elastixImageFilter.SetFixedImage(fixed_sitk)
    elastixImageFilter.SetMovingImage(moving_sitk)

    
    parameterMapVector = sitk.VectorOfParameterMap()
    translation_map = sitk.GetDefaultParameterMap('translation')
    translation_map['MaximumNumberOfIterations'] = ['4000']
    translation_map['DefaultPixelValue'] = ["-1000"]
    
    parameterMapVector.append(translation_map)
    rigid_map = sitk.GetDefaultParameterMap("rigid")
    rigid_map['MaximumNumberOfIterations'] = ["50"]
    rigid_map['DefaultPixelValue'] = ["-1000"]
    parameterMapVector.append(rigid_map)
    
    # parametermap['MaximumNumberOfSamplingAttempts'] = ['16']
    elastixImageFilter.SetParameterMap(parameterMapVector) #method

    """3) Execute"""
    elastixImageFilter.Execute()
    resultimage = elastixImageFilter.GetResultImage()
    
    #save parameter map
    temp_idx = 0
    while True:
        try:
            sitk.WriteParameterFile(elastixImageFilter.GetTransformParameterMap()[temp_idx], os.path.join(save_path, "P%03d_%03d_param.txt" %(ind, temp_idx)))
        except:
            break
        temp_idx += 1

    return resultimage

bp = r"D:\!JUNG_newdata"
ct_path = os.path.join(bp, "!!!JG_new_CT_3.0_nifti")
mr_path = os.path.join(bp, "!!!JG_new_MR_3.0_nifti")
ct_path_list = os.listdir(ct_path)
mr_path_list = os.listdir(mr_path)
print(len(ct_path_list))
for idx in range(39):
    t1 = os.path.join(ct_path, ct_path_list[idx])
    t2 = os.path.join(mr_path, mr_path_list[idx])
    ct_nif = nib.load(os.path.join(t1, os.listdir(t1)[0]))
    mr_nif = nib.load(os.path.join(t2, os.listdir(t2)[0]))
    
    ct_header = ct_nif.header
    ct_data = ct_nif.get_fdata()
    mr_header = mr_nif.header
    mr_data = mr_nif.get_fdata()
    
    print(ct_header)
    print(mr_header)

    #to recover, save the spacing, size and origin
    # x y z spacing
    
    ct_spacing = list(ct_nif.header["pixdim"][1:4])
    ct_sizes = ct_header["dim"][1:4]
    mr_spacing = list(mr_nif.header["pixdim"][1:4])
    mr_sizes = mr_header["dim"][1:4]
    
    for s in range(len(ct_spacing)):
        ct_spacing[s] = float(ct_spacing[s])
    for s in range(len(mr_spacing)):
        mr_spacing[s] = float(mr_spacing[s])

    
    ct_data = np.transpose(ct_data, (2, 1, 0))
    mr_data = np.transpose(mr_data, (2, 1, 0))
    #ct preprocessing
    min_ = -1000
    max_ = 3500
    ct_data[ct_data < min_] = min_
    ct_data[ct_data > max_] = max_
    
    print("original data MR:", np.max(mr_data), np.min(mr_data))
    print(ct_data.shape, mr_data.shape)
    min_pixel_value = np.min(mr_data)
    
    ct_origin = [float(ct_header["qoffset_x"]), float(ct_header["qoffset_y"]), float(ct_header["qoffset_z"])]
    mr_origin = [float(mr_header["qoffset_x"]), float(mr_header["qoffset_y"]), float(mr_header["qoffset_z"])]

    ct_sitk = convert_to_sitk(ct_data, ct_spacing, ct_origin)
    mr_sitk = convert_to_sitk(mr_data, mr_spacing, mr_origin)
    
    ct_res_sitk = resample(ct_sitk, mr_spacing, (512, 512, int(ct_sizes[2] * (ct_spacing[2]/mr_spacing[2]))), idx+1)
    
    mr_npy = convert_to_numpy(mr_sitk)
     #####normalization#####
    mr_one_dim = np.ravel(mr_npy)
    
    
    mr_npy = mr_npy.astype("int32")
    max_pixel_value = np.max(mr_npy)
    mrnorm_hyperparam = 1000
    counts_list, bin_locations, patches = plt.hist(mr_one_dim, max_pixel_value, (0, max_pixel_value))

    
    for idx_val in range(max_pixel_value-1, -1, -1):
        if counts_list[idx_val] > mrnorm_hyperparam:
            val_norm = idx_val+1
            
            # norm_val_list.append(val_norm)
            break
    print("valnorm:", val_norm)
    mr_npy = np.where(mr_npy > val_norm, val_norm, mr_npy)
    mr_npy = np.where(mr_npy < min_pixel_value, min_pixel_value, mr_npy)
    mr_npy -= min_pixel_value
    print(np.max(mr_npy), np.min(mr_npy))
    mr_final_sitk = convert_to_sitk(mr_npy, mr_spacing, mr_origin)
    
    result_ct_sitk = rigid_registration(mr_final_sitk, ct_res_sitk, r"D:\!JUNG_newdata\param_txt_fol2", idx+1)

    sitk.WriteImage(result_ct_sitk, r"D:\!JUNG_newdata\CTnii/P%03d_CT_ori_norm.nii.gz" %(idx+1))
    sitk.WriteImage(mr_final_sitk, r"D:\!JUNG_newdata\MRnii/P%03d_MR_ori_norm.nii.gz" %(idx+1))
 
    