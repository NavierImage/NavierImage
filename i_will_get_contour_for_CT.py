import os 
import numpy as np
import SimpleITK as sitk
import pydicom 
from skimage import draw
import matplotlib.pyplot as plt 

rtst_basepath = r"D:\!JUNG_newdata_T23D_mr\JUNG_T2MR_CT_contoured"
rtst_dir_list = os.listdir(rtst_basepath)

ct_basepath = r"D:\!JUNG_newdata_T23D_mr\abdomenCT1"
savepath = r"D:\!JUNG_newdata_T23D_mr\abdomenCT1_contour"
ct_dir_list = os.listdir(ct_basepath)

def know_contour_limit(rtst_dcm):
    ctr_idx = 0
    for temp_idx in range(100):
        try:
            temp = rtst_dcm.ROIContourSequence[temp_idx]
        except:
            ctr_idx = temp_idx
            break
    ctr_z_idx_list = []
    for temp_idx in range(ctr_idx):
        for j in range(10**5):
            try:
                rtst_dcm.ROIContourSequence[temp_idx].ContourSequence[j]
            except:
                ctr_z_idx_list.append(j)
                break
    return ctr_idx, ctr_z_idx_list

def contour_name_labeling(rtst_dcm, ctr_idx, ctr_z_idx_list):
    name_dict = {}
    for i in range(ctr_idx):
        name_dict[rtst_dcm.StructureSetROISequence[i].ROIName] = i+1
    return name_dict 

assert rtst_dir_list == ct_dir_list

for file_idx in range(len(ct_dir_list)):
    ct_dcm_path = os.path.join(ct_basepath, ct_dir_list[file_idx], "DCMData")
    ct_dcm_dir_list = os.listdir(ct_dcm_path)
    dcm_list = []
    for j in range(len(ct_dcm_dir_list)):
        dcm = pydicom.dcmread(os.path.join(ct_dcm_path, ct_dcm_dir_list[j]), force=True)
        dcm_list.append((dcm, float(dcm.ImagePositionPatient[2])))
    dcm_list.sort(key=lambda x:x[1])
    
    inf_ct = dcm_list[0][0]
    
    spacing_z = (float(dcm_list[-1][0].ImagePositionPatient[2])-float(dcm_list[0][0].ImagePositionPatient[2]))/float(len(dcm_list))
    spacing_x, spacing_y = float(dcm_list[0][0].PixelSpacing[0]), float(dcm_list[0][0].PixelSpacing[1])
    
    origin = np.array([float(file_idx) for file_idx in inf_ct.ImagePositionPatient], dtype=np.float32)
    spacing = np.array([spacing_x, spacing_y, spacing_z],  dtype=np.float32)
    
    rtst_dcm = pydicom.dcmread(os.path.join(rtst_basepath, rtst_dir_list[file_idx]), force=True)    
    
    ctr_idx, ctr_z_idx_list = know_contour_limit(rtst_dcm)
    name_dict= contour_name_labeling(rtst_dcm, ctr_idx, ctr_z_idx_list)
    name_dict_rev ={v:k for k, v in name_dict.items()}
    
    labeling_dict = {"Liver":1, "Kidney_L":2, "Kidney_R" :3,"Duodenum": 4, "Stomach" :5, "Spleen" :6, "Pancreas" :7, "Gallbladder":8}
    
    
    
    print(file_idx)
    for i in range(ctr_idx):
        target_name = name_dict_rev[i+1]
        try:
            target_label_num = labeling_dict[target_name]
        except:
            continue
        
        
        ctr_arr = np.zeros((len(dcm_list), inf_ct.Rows, inf_ct.Columns), dtype="uint8")
        for j in range(ctr_z_idx_list[i]):
            ctr_raw_data = rtst_dcm.ROIContourSequence[i].ContourSequence[j].ContourData
            poly_r_list = []
            poly_c_list = []
            
            for k in range(0, len(ctr_raw_data), 3):
                co_raw_arr = np.array(ctr_raw_data[k:k+3], np.float32)
                co_con_arr = (co_raw_arr - origin)/spacing
                co_con_arr = co_con_arr.astype("uint16")
                # x2, y2, z2 = ctr_raw_data[k+3:k+6]
                
                poly_r_list.append(co_con_arr[1])
                poly_c_list.append(co_con_arr[0])
            row_poly_coord, col_poly_coord = draw.polygon(poly_r_list, poly_c_list)
            
            ctr_arr[co_con_arr[2], row_poly_coord, col_poly_coord] = 1
        la_sitk = sitk.GetImageFromArray(ctr_arr)
        la_sitk.SetSpacing(spacing.astype(np.double))
        la_sitk.SetOrigin(origin.astype(np.double))
        sitk.WriteImage(la_sitk, os.path.join(savepath, "P%03d_%s.nii.gz" %(file_idx, target_name)))
    
           
    
    
    
    
    
    
    