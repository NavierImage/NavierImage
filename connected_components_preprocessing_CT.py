import os 
import numpy as np
import SimpleITK as sitk
import cc3d 
import matplotlib.pyplot as plt
from scipy import ndimage
from PIL import Image
basepath = r"D:\!JUNG_2nd_data\abdomenCT1_regi"
savepath = r"D:\!JUNG_2nd_data\abdomenCT1_regi_cc"
maskpath = r"D:\!JUNG_2nd_data\abdomenCt1_regi_ccmask"
ct_dir_list = os.listdir(basepath)

for idx in range(len(ct_dir_list)):
    print(ct_dir_list[idx])
    ct_path = os.path.join(basepath, ct_dir_list[idx])
    ct_sitk = sitk.ReadImage(ct_path)
    ct_arr = sitk.GetArrayFromImage(ct_sitk)
    
    win_min = -160
    win_max = 350
    win_ct_arr = np.copy(ct_arr).astype("float32")
    win_ct_arr[win_ct_arr > win_max] = win_max
    win_ct_arr[win_ct_arr < win_min] = win_min
    
    win_ct_arr = 255 * (win_ct_arr - win_min)/(win_max - win_min)
    win_ct_arr = win_ct_arr.astype("uint8")
    
    binary_ct = np.where(win_ct_arr != 0, 255, 0)
    binary = cc3d.dust(binary_ct, threshold=5*(10**6))
    
    binary = binary.astype("uint8")
    for i in range(len(binary)):
        binary[i] = cc3d.dust(binary_ct[i], threshold=10000)
        # if i == len(binary) - 25:
        #     plt.imshow(binary[i])   
        #     plt.show() 
        binary[i] = ndimage.binary_fill_holes(binary[i])
        # if i == len(binary) - 25:
        #     plt.imshow(binary[i])   
        #     plt.show()  
        binary_2d_1 = np.copy(binary[i])
        binary_2d_2 = np.copy(binary[i])
        binary_2d_1 = ndimage.binary_closing(binary_2d_1, iterations=20).astype("uint8")
        binary_2d_2 = ndimage.binary_closing(binary_2d_2, iterations=30).astype("uint8")
        
        last_binary = binary[i] + binary_2d_1 + binary_2d_2
        last_binary[last_binary != 0] = 255
        last_binary = ndimage.binary_fill_holes(last_binary)
        
        binary[i] = np.copy(last_binary)

        
    binary = binary.astype(np.uint16)
    mask_sitk = sitk.GetImageFromArray(binary)
    mask_sitk.SetSpacing(ct_sitk.GetSpacing())
    mask_sitk.SetOrigin(ct_sitk.GetOrigin())
    
    ct_min = np.min(ct_arr)
    ct_arr = np.where(binary != 0, ct_arr, -1024).astype("float32")
    
    
    
    
    new_ct_sitk = sitk.GetImageFromArray(ct_arr)
    new_ct_sitk.SetSpacing(ct_sitk.GetSpacing())
    new_ct_sitk.SetOrigin(ct_sitk.GetOrigin())
    
    sitk.WriteImage(new_ct_sitk, os.path.join(savepath, ct_dir_list[idx]))
    sitk.WriteImage(mask_sitk, os.path.join(maskpath, ct_dir_list[idx].split("_")[0] + "_mask.nii.gz"))
    # visualization
    # ct_arr[ct_arr < win_min] = win_min
    # ct_arr[ct_arr > win_max] = win_max 
    # ct_arr = 255 * (ct_arr - win_min)/(win_max - win_min)
    # ct_arr = ct_arr.astype("uint8")
    
    # for i in range(len(ct_arr)):
    #     img = Image.fromarray(ct_arr[i])
        
    #     img.save(os.path.join(r"D:\!JUNG_2nd_data\act_cc_img", "P%03d_%03d.png" %(idx, i)))
    
    