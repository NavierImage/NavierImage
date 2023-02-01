import os
import re
import openpyxl
import shutil
file_path = r"D:\DLnetwork\MRSIM_checkpoints_2\results\CT_[-280, 800]"
dest_path = r"D:\DLnetwork\MRSIM_checkpoints_2\results\sorted"
xlsx_path = r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\data_prop_CECT_totalMR.xlsx"
wb = openpyxl.load_workbook(xlsx_path)
worksheet = wb["Total_data_prop"]
patient_num = worksheet["A2":"A51"]
pa_num = []
for row in patient_num:
    for celldata in row:
        pa_num.append(int(celldata.value))

file_list = os.listdir(file_path)
idx = -1
for row in worksheet["J2":"K51"]:
    idx += 1
    st_end_point = []
    for cell in row:
        st_end_point.append(cell.value)
        print(cell.value)
    for i in range(len(file_list)):
        nums = re.findall(r"\d+", file_list[i])
        patient = int(nums[0])
        slice_idx = int(nums[1])
        if pa_num[idx] == patient and st_end_point[0]<= slice_idx <=st_end_point[1]:
            shutil.copy(file_path+'/'+file_list[i], dest_path+'/'+file_list[i])
    
        
