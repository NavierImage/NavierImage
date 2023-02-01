import os
import numpy as np
import pydicom
from numpngw import write_png
from PIL import Image

#from PIL import Image #PIL은 8bit image만 다룰수 있음.
#https://stackoverflow.com/questions/62739851/convert-rgb-arrays-to-pil-image
#CT폴더 불러오기
#Contour파일 불러오기
basepath = 'D:\junggeyon\Patient_data/'
dir_list = os.listdir(basepath)
for i in range(1, 48):    
    if i < 10:number_str = '00' + str(i)
    else: number_str = '0' + str(i)
    
    for patient in dir_list:
        
        if number_str == patient[:3]:
            print(patient)
            sub_dir_list = os.listdir(basepath + patient)
            
            for modality in sub_dir_list:
                if 'CT_aligned' == modality:
                    sub_sub_dir_list = os.listdir(basepath + patient +'/' + modality)
                    for destination in sub_sub_dir_list:
                        CT_folder_path = basepath + patient + '/' + modality +'/'+destination
                        if 'npy' in CT_folder_path:
                            continue
                        break

                if 'MR' == modality:
                    sub_sub_dir_list = os.listdir(basepath + patient +'/' + modality)
                    for destination in sub_sub_dir_list:
                        if destination[-3:] != 'npy':
                            MR_folder_path = basepath + patient + '/' + modality +'/'+destination
                            break
            break

    def GetCTinfo(CT_folder_path):
            CT_dcm_files = []
            fileidx = []
            for top, dir, file in os.walk(CT_folder_path):
                for filename in file:
                    if filename[-3:] != 'dcm':
                        continue
                    temp_ct_slice = pydicom.dcmread(CT_folder_path + '/' + filename)
                    CT_dcm_files.append(temp_ct_slice)
                    idxnum = temp_ct_slice.InstanceNumber
                    fileidx.append(idxnum)
                break

            fileidx = np.array(fileidx)
            fileorder = np.argsort(fileidx)

            sorted_CT_file = []

            for i in range(len(fileidx)):
                sorted_CT_file.append(CT_dcm_files[fileorder[i]])

            return sorted_CT_file, len(fileidx)

    sorted_CT_file, zsize = GetCTinfo(CT_folder_path)

    def GetMRinfo(MR_folder_path):
            MR_dcm_files = []
            fileidx = []
            for top, dir, file in os.walk(MR_folder_path):
                for filename in file:
                    if filename[-3:] != 'dcm':
                        continue
                    temp_mr_slice = pydicom.dcmread(MR_folder_path + '/' + filename)
                    MR_dcm_files.append(temp_mr_slice)
                    idxnum = temp_mr_slice.InstanceNumber
                    fileidx.append(idxnum)
                break

            fileidx = np.array(fileidx)
            fileorder = np.argsort(fileidx)

            sorted_MR_file = []

            for i in range(len(fileidx)):
                sorted_MR_file.append(MR_dcm_files[fileorder[i]])

            return sorted_MR_file, len(fileidx)

    sorted_MR_file, zsize = GetMRinfo(MR_folder_path)

    assert len(sorted_CT_file) == len(sorted_MR_file), 'check file nums'

    ct_inferior = sorted_CT_file[-1]
    mr_inferior = sorted_MR_file[-1]
    x_std_ct, y_std_ct, z_std_ct = ct_inferior.ImagePositionPatient
    x_std_mr, y_std_mr, z_std_mr = mr_inferior.ImagePositionPatient

    
    for idx in range(len(sorted_MR_file)):
        ct = sorted_CT_file[idx]
        mr = sorted_MR_file[idx]
        #ct_z = ct.ImagePositionPatient[2]/ct.SliceThickness + abs(z_std_ct/ct_inferior.SliceThickness)
        #mr_z = mr.ImagePositionPatient[2]/mr.SliceThickness + abs(z_std_mr/mr_inferior.SliceThickness)
        print(ct.ImagePositionPatient[2], mr.ImagePositionPatient[2])
        if ct.ImagePositionPatient[2] - mr.ImagePositionPatient[2] > 1:
            
            print('error....')
    

    
