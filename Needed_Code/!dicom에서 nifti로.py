import os
import dicom2nifti
import dicom2nifti.settings as settings

ct_bp = r"D:\junggeyon\!!!JG_new_CT_3.0"
mr_bp = r"D:\junggeyon\!!!JG_new_MR_3.0"

ct_dest = r"D:\junggeyon\!!!JG_new_CT_3.0_nifti"
mr_dest = r"D:\junggeyon\!!!JG_new_MR_3.0_nifti"

ct_folder_path_list = os.listdir(ct_bp)
mr_folder_path_list = os.listdir(mr_bp)

for i in range(len(ct_folder_path_list)):
    try:
        os.mkdir(os.path.join(ct_dest, ct_folder_path_list[i].split("_")[1]))
    except:
        pass
    
    dicom2nifti.convert_directory(dicom_directory=os.path.join(ct_bp, ct_folder_path_list[i]), 
                                  output_folder=os.path.join(ct_dest, ct_folder_path_list[i].split("_")[1]),
                                  reorient=True)
print("CT완료")
for i in range(len(mr_folder_path_list)):
    try:
        os.mkdir(os.path.join(mr_dest, mr_folder_path_list[i].split("_")[1]))
    except:
        pass
    
    dicom2nifti.convert_directory(dicom_directory=os.path.join(mr_bp, mr_folder_path_list[i]), 
                                  output_folder=os.path.join(mr_dest, mr_folder_path_list[i].split("_")[1]),
                                  reorient=True)
print("MR완료")