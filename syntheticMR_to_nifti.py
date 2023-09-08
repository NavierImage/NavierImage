import os 
import SimpleITK as sitk
import torch 
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
fakeMR_path = r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_swinunetr_nomind_v2\test_latest\fakeMR_fortrain"
fakeMR_dir_list = os.listdir(fakeMR_path)

pivot_num = int(fakeMR_dir_list[0][1:4])
nii_3d_stack_list = []

for i in range(len(fakeMR_dir_list)):
    patient_num = int(fakeMR_dir_list[i][1:4])
    if pivot_num != patient_num:
        nii_3d_stack_arr = np.array(nii_3d_stack_list).astype("float32")
        mr_sitk = sitk.GetImageFromArray(nii_3d_stack_arr)
        mr_sitk.SetSpacing(np.array([0.7, 0.7, 1.2], dtype=np.double))
        sitk.WriteImage(mr_sitk, os.path.join(r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_swinunetr_nomind_v2\test_latest\fakeMR_nii_train", "P%03d_sMR.nii.gz" %(pivot_num)))
        pivot_num = patient_num
        nii_3d_stack_list = []
    
    fake_mr_tensor = torch.load(os.path.join(fakeMR_path, fakeMR_dir_list[i]),map_location=torch.device("cpu"))
    fake_mr_arr = fake_mr_tensor.detach().clone().cpu().numpy()
    fake_mr_arr = np.squeeze(fake_mr_arr)
    nii_3d_stack_list.append(fake_mr_arr)
    
    # fake_mr_arr = np.squeeze(fake_mr_arr)
    # fake_mr_arr = 255 * (fake_mr_arr - np.min(fake_mr_arr))/(np.max(fake_mr_arr) - np.min(fake_mr_arr))
    # fake_mr_arr = fake_mr_arr.astype("uint8")

    # img = Image.fromarray(fake_mr_arr)
    # img.save(os.path.join(r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_swinunetr_nomind_v2\test_latest\fake_MR_img", fakeMR_dir_list[i][:-3] + ".png"))
nii_3d_stack_arr = np.array(nii_3d_stack_list).astype("float32")
mr_sitk = sitk.GetImageFromArray(nii_3d_stack_arr)
mr_sitk.SetSpacing(np.array([0.7, 0.7, 1.2], dtype=np.double))
sitk.WriteImage(mr_sitk, os.path.join(r"D:\AAAAmrsim\results\!!!!!KSMP_ADD_swinunetr_nomind_v2\test_latest\fakeMR_nii_train", "P%03d_sMR.nii.gz" %(pivot_num+1)))
