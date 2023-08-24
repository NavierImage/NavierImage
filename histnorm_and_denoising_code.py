import os
import nibabel as nib
import numpy as np
import matlab.engine
import SimpleITK as sitk
import multiprocessing
import gc
import matplotlib.pyplot as plt

# arr = np.zeros((15, 512, 512), dtype="uint8")
# arr[43:643, 56] = 100
# a = matlab.uint8(arr.tolist())
# 3d를 patch로 끊어서 denoising 
# [90, 512, 512] - > [3, 512, 512]이런식으로 ㅋㅋ
# b = eng.bm4d(a)

def memory_shit_process(mr_arr):
    mr_arr = HistogramNorm(mr_arr)
    eng = matlab.engine.start_matlab()
    denoised_mr_arr = denoising(mr_arr, eng)
    eng.eval("clear", nargout=0)
    eng.eval("pack", nargout=0)
    eng.quit()
    return denoised_mr_arr

def HistogramNorm(mr_volume):
    mr_one_dim = np.ravel(mr_volume)
    print(np.max(mr_volume), np.min(mr_volume))
    if np.min(mr_volume) < 0:
        mr_volume += np.min(mr_volume)
    
    #####normalization#####
    max_pixel_value = 2500
    mrnorm_hyperparam = 1000
    counts_list, bin_locations, patches = plt.hist(mr_one_dim, max_pixel_value, (0, max_pixel_value))
    plt.ylim((0, 1e5))
    plt.xlim((0, 2500))
    plt.xlabel("Pixel Value")
    plt.ylabel("Number of Pixels")
    # plt.show()
    
    for idx_val in range(max_pixel_value-1, -1, -1):
        if counts_list[idx_val] > mrnorm_hyperparam:
            val_norm = idx_val+1
            break
        
    mr_volume = np.where(mr_volume > val_norm, val_norm, mr_volume)
    return mr_volume

def denoising(mr_arr, eng): # mr_arr -> z y x form

    nii_arr = np.copy(mr_arr) # x y z -> z y x
    temp_nii_arr = np.copy(mr_arr)
    
    
    mr_max = np.max(temp_nii_arr)
    mr_min = np.min(temp_nii_arr)
    temp_nii_arr = (temp_nii_arr - mr_min)/(mr_max - mr_min)
    
    nii_arr = (nii_arr - mr_min)/(mr_max - mr_min)
    
    maxv= max(mr_max, 255)
    
    nii_denoised_arr = np.zeros_like(nii_arr)
    denoise_iter = 1
    for i in range(0, len(nii_arr), 2):
        
        if i+2 >= len(nii_arr):
            patch = nii_arr[i:len(nii_arr), :, :]
        else:
            patch = nii_arr[i:i+2, :, :]
        patch_mat = matlab.double(patch.tolist())
        
        for j in range(denoise_iter):
            patch_mat = eng.bm4d(patch_mat, "Rice", 0.065)
            
        de_patch = np.array(patch_mat)
        if i+2 >= len(nii_arr):
            nii_denoised_arr[i:len(nii_arr), :, :] = de_patch
        else:
            nii_denoised_arr[i:i+2, :, :] = de_patch
    eng.eval("clear", nargout=0)
    eng.eval("pack", nargout=0)
    
    del de_patch
    del patch_mat
    gc.collect()
   
    nii_denoised_arr *= (mr_max - mr_min)
    return nii_denoised_arr

if __name__ == "__main__":
    basepath = r"D:\!JUNG_2nd_data\abdomenMR1xT_regi"
    savepath = r"D:\!JUNG_2nd_data\abdomenMR1xT_regi_hist_denoise"
    mr_dir_list = os.listdir(basepath)

    for idx in range(9, len(mr_dir_list)):
        mr_sitk = sitk.ReadImage(os.path.join(basepath, mr_dir_list[idx]))
        mr_arr = sitk.GetArrayFromImage(mr_sitk)
        mr_min = np.min(mr_arr)
        mr_max = np.max(mr_arr)
        print(mr_min)
        if mr_min < 0:
            mr_arr += abs(mr_min)
        
        pool = multiprocessing.Pool(processes=1)
        
        mr_arr = pool.apply(memory_shit_process, args=(mr_arr,))
        mr_arr = mr_arr.astype("uint16")
        denoised_mr_sitk = sitk.GetImageFromArray(mr_arr)
        denoised_mr_sitk.SetSpacing(mr_sitk.GetSpacing())
        denoised_mr_sitk.SetOrigin(mr_sitk.GetOrigin())
        
        
        sitk.WriteImage(denoised_mr_sitk, os.path.join(savepath, mr_dir_list[idx]))
        # del mr_sitk
        # del mr_arr
        # del denoised_mr_arr
        # del denoised_mr_sitk
        # del eng
        
        gc.collect()