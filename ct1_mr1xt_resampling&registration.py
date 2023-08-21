import os 
import SimpleITK as sitk
import numpy as np
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

def registration(fixed_sitk, moving_sitk, param_save_path = None, ind = 0):
    """1) Set ElastixImageFilter"""
    elastixImageFilter = sitk.ElastixImageFilter()
    """2) Set Parameters"""
    elastixImageFilter.SetFixedImage(fixed_sitk)
    elastixImageFilter.SetMovingImage(moving_sitk)

    
    parameterMapVector = sitk.VectorOfParameterMap()
    translation_map = sitk.GetDefaultParameterMap('translation')
    translation_map['MaximumNumberOfIterations'] = ['6000']
    translation_map['DefaultPixelValue'] = ["-1000"]
    parameterMapVector.append(translation_map)
    rigid_map = sitk.GetDefaultParameterMap("rigid")
    rigid_map['MaximumNumberOfIterations'] = ["3000"]
    rigid_map['DefaultPixelValue'] = ["-1000"]
    parameterMapVector.append(rigid_map)
    # bspline_map = sitk.GetDefaultParameterMap("bspline")
    # bspline_map["FinalGridSpacingInPhysicalUnits"] = ["50"]
    # bspline_map['MaximumNumberOfIterations'] = ['10']
    # bspline_map['DefaultPixelValue'] = ["-1000"]
    # parameterMapVector.append(bspline_map)
    # bspline2_map = sitk.GetDefaultParameterMap("bspline")
    # bspline2_map["FinalGridSpacingInPhysicalUnits"] = ["20"]
    # bspline2_map['MaximumNumberOfIterations'] = ['3']
    # bspline2_map['DefaultPixelValue'] = ["-1000"]
    # parameterMapVector.append(bspline2_map)
    
    
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
            sitk.WriteParameterFile(elastixImageFilter.GetTransformParameterMap()[temp_idx], os.path.join(param_save_path, "P%03d_%03d_param.txt" %(ind, temp_idx)))
        except:
            break
        temp_idx += 1

    return resultimage
def registration_for_mr(fixed_sitk, moving_sitk, min_val, param_save_path = None, ind = 0):
    """1) Set ElastixImageFilter"""
    elastixImageFilter = sitk.ElastixImageFilter()
    """2) Set Parameters"""
    elastixImageFilter.SetFixedImage(fixed_sitk)
    elastixImageFilter.SetMovingImage(moving_sitk)
    
    
    parameterMapVector = sitk.VectorOfParameterMap()
    translation_map = sitk.GetDefaultParameterMap('translation')
    translation_map['MaximumNumberOfIterations'] = ['6000']
    translation_map['DefaultPixelValue'] = [str(min_val)]
    parameterMapVector.append(translation_map)
    rigid_map = sitk.GetDefaultParameterMap("rigid")
    rigid_map['MaximumNumberOfIterations'] = ["3000"]
    rigid_map['DefaultPixelValue'] = [str(min_val)]
    parameterMapVector.append(rigid_map)
    # bspline_map = sitk.GetDefaultParameterMap("bspline")
    # bspline_map["FinalGridSpacingInPhysicalUnits"] = ["50"]
    # bspline_map['MaximumNumberOfIterations'] = ['10']
    # bspline_map['DefaultPixelValue'] = ["-1000"]
    # parameterMapVector.append(bspline_map)
    # bspline2_map = sitk.GetDefaultParameterMap("bspline")
    # bspline2_map["FinalGridSpacingInPhysicalUnits"] = ["20"]
    # bspline2_map['MaximumNumberOfIterations'] = ['3']
    # bspline2_map['DefaultPixelValue'] = ["-1000"]
    # parameterMapVector.append(bspline2_map)
    
    
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
            sitk.WriteParameterFile(elastixImageFilter.GetTransformParameterMap()[temp_idx], os.path.join(param_save_path, "P%03d_%03d_param.txt" %(ind, temp_idx)))
        except:
            break
        temp_idx += 1

    return resultimage
ct_basepath = r"D:\!JUNG_newdata_T23D_mr\abdomenCT1_sitk"
mr_basepath = r"D:\!JUNG_newdata_T23D_mr\abdomenMR1xT_sitk"

ct_dir_list = os.listdir(ct_basepath)
mr_dir_list = os.listdir(mr_basepath)

assert len(ct_dir_list) == len(mr_dir_list)

for i in range(len(ct_dir_list)):
    ct_sitk_path = os.path.join(ct_basepath, ct_dir_list[i])
    mr_sitk_path = os.path.join(mr_basepath, mr_dir_list[i])
    ct_sitk = sitk.ReadImage(ct_sitk_path)
    mr_sitk = sitk.ReadImage(mr_sitk_path)
    
    mr_arr = sitk.GetArrayFromImage(mr_sitk)
    mr_min_val = np.min(mr_arr).astype("double")
    
    target_spacing = np.array([0.7, 0.7, 1.20],dtype=np.double)
    original_ct_size = ct_sitk.GetSize()
    original_mr_size = mr_sitk.GetSize()
    original_ct_spacing = ct_sitk.GetSpacing()
    original_mr_spacing = mr_sitk.GetSpacing()
    
    # z_size setting
    
    new_ct_z_size = original_ct_size[2] * (original_ct_spacing[2] / target_spacing[2])
    new_mr_z_size = original_mr_size[2] * (original_mr_spacing[2] / target_spacing[2])
    
    new_ct_z_size_int = int(new_ct_z_size)
    new_mr_z_size_int = int(new_mr_z_size)
    
    zero_one_decimal_num_ct = new_ct_z_size - float(new_ct_z_size_int)
    zero_one_decimal_num_mr = new_mr_z_size - float(new_mr_z_size_int)
    
    if zero_one_decimal_num_ct >= 0.5: new_ct_z_size_int += 1
    if zero_one_decimal_num_mr >= 0.5: new_mr_z_size_int += 1
    
    target_ct_size = np.array([512, 512, new_ct_z_size], dtype=np.double)
    target_mr_size = np.array([512, 512, new_mr_z_size], dtype=np.double)
    ct_resampled_sitk = resample(ct_sitk, target_spacing, target_ct_size, default_value=-1024)
    mr_resampled_sitk = resample(mr_sitk, target_spacing, target_mr_size, default_value=mr_min_val)
    
    mr_moving_sitk = registration_for_mr(ct_resampled_sitk, mr_resampled_sitk, mr_min_val, r"D:\!JUNG_newdata_T23D_mr\abdomen_param_savepath", i)
    
    sitk.WriteImage(ct_resampled_sitk, os.path.join(r"D:\!JUNG_2nd_data\abdomenCT1_regi", ct_dir_list[i]))
    sitk.WriteImage(mr_moving_sitk, os.path.join(r"D:\!JUNG_2nd_data\abdomenMR1xT_regi", mr_dir_list[i]))
    
    
    
    
    