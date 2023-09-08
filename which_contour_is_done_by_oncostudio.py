import os 
import numpy as np
import SimpleITK as sitk
la_basepath = r"D:\!JUNG_2nd_data\abdomenCT1_contour"
la_dir_list = os.listdir(la_basepath)

la_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
for idx in range(len(la_dir_list)//8):
    for jdx in range(8):
        la_sitk = sitk.ReadImage(os.path.join(la_basepath, la_dir_list[8*idx+jdx]))
        la_arr = sitk.GetArrayFromImage(la_sitk)
        if np.any(la_arr == 1):
            la_dict[jdx+1] += 1
print(la_dict)